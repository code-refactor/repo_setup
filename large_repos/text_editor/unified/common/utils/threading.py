import threading
import time
import queue
from datetime import datetime
from typing import Any, Callable, Optional, Dict, List
from pydantic import BaseModel, Field


class ThreadSafeQueue(BaseModel):
    """Thread-safe queue wrapper with additional functionality."""
    
    max_size: int = 0
    
    def __init__(self, max_size: int = 0, **data):
        super().__init__(**data)
        self._queue = queue.Queue(maxsize=max_size)
        self.max_size = max_size
    
    def put(self, item: Any, block: bool = True, timeout: Optional[float] = None) -> bool:
        """Put an item in the queue."""
        try:
            self._queue.put(item, block=block, timeout=timeout)
            return True
        except queue.Full:
            return False
    
    def get(self, block: bool = True, timeout: Optional[float] = None) -> Any:
        """Get an item from the queue."""
        try:
            return self._queue.get(block=block, timeout=timeout)
        except queue.Empty:
            return None
    
    def task_done(self) -> None:
        """Mark a task as done."""
        self._queue.task_done()
    
    def join(self) -> None:
        """Wait for all tasks to be completed."""
        self._queue.join()
    
    def qsize(self) -> int:
        """Get the approximate queue size."""
        return self._queue.qsize()
    
    def empty(self) -> bool:
        """Check if the queue is empty."""
        return self._queue.empty()
    
    def full(self) -> bool:
        """Check if the queue is full."""
        return self._queue.full()


class BackgroundTask(BaseModel):
    """Represents a background task."""
    task_id: str
    function: Callable = Field(exclude=True)
    args: tuple = Field(default_factory=tuple)
    kwargs: Dict[str, Any] = Field(default_factory=dict)
    priority: int = 0
    created_at: datetime = Field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Any = None
    error: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True


class BackgroundProcessor(BaseModel):
    """Manages background task processing."""
    
    max_workers: int = 2
    queue: ThreadSafeQueue = Field(default_factory=ThreadSafeQueue)
    running: bool = False
    tasks: Dict[str, BackgroundTask] = Field(default_factory=dict)
    shutdown_timeout: float = 5.0
    
    def __init__(self, **data):
        super().__init__(**data)
        self.workers = []
        self._shutdown_event = threading.Event()
        self._lock = threading.Lock()
    
    def start(self) -> None:
        """Start the background processor."""
        if self.running:
            return
        
        self.running = True
        self._shutdown_event.clear()
        
        # Start worker threads
        for i in range(self.max_workers):
            worker = threading.Thread(
                target=self._worker_loop,
                name=f"BackgroundWorker-{i}",
                daemon=True
            )
            worker.start()
            self.workers.append(worker)
    
    def stop(self) -> None:
        """Stop the background processor."""
        if not self.running:
            return
        
        self.running = False
        self._shutdown_event.set()
        
        # Signal all workers to stop
        for _ in range(self.max_workers):
            self.queue.put(None)  # Poison pill
        
        # Wait for workers to finish
        for worker in self.workers:
            worker.join(timeout=self.shutdown_timeout)
        
        self.workers.clear()
    
    def submit_task(self, task_id: str, function: Callable, 
                   args: tuple = (), kwargs: Optional[Dict[str, Any]] = None,
                   priority: int = 0) -> str:
        """Submit a task for background processing."""
        if not self.running:
            raise RuntimeError("Background processor is not running")
        
        task = BackgroundTask(
            task_id=task_id,
            function=function,
            args=args,
            kwargs=kwargs or {},
            priority=priority
        )
        
        with self._lock:
            self.tasks[task_id] = task
        
        self.queue.put(task)
        return task_id
    
    def get_task_result(self, task_id: str) -> Optional[Any]:
        """Get the result of a completed task."""
        with self._lock:
            task = self.tasks.get(task_id)
            if task and task.completed_at:
                return task.result
        return None
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get the status of a task."""
        with self._lock:
            task = self.tasks.get(task_id)
            if not task:
                return {"status": "not_found"}
            
            if task.error:
                return {
                    "status": "error",
                    "error": task.error,
                    "created_at": task.created_at,
                    "started_at": task.started_at,
                    "completed_at": task.completed_at
                }
            elif task.completed_at:
                return {
                    "status": "completed",
                    "result": task.result,
                    "created_at": task.created_at,
                    "started_at": task.started_at,
                    "completed_at": task.completed_at
                }
            elif task.started_at:
                return {
                    "status": "running",
                    "created_at": task.created_at,
                    "started_at": task.started_at
                }
            else:
                return {
                    "status": "queued",
                    "created_at": task.created_at
                }
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a queued task (cannot cancel running tasks)."""
        with self._lock:
            task = self.tasks.get(task_id)
            if task and not task.started_at:
                # Mark as cancelled by setting error
                task.error = "cancelled"
                task.completed_at = datetime.now()
                return True
        return False
    
    def get_queue_size(self) -> int:
        """Get the current queue size."""
        return self.queue.qsize()
    
    def get_active_tasks(self) -> List[str]:
        """Get list of currently active task IDs."""
        with self._lock:
            return [
                task_id for task_id, task in self.tasks.items()
                if task.started_at and not task.completed_at and not task.error
            ]
    
    def get_completed_tasks(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get list of recently completed tasks."""
        with self._lock:
            completed = [
                {
                    "task_id": task_id,
                    "completed_at": task.completed_at,
                    "duration": (task.completed_at - task.started_at).total_seconds()
                    if task.started_at and task.completed_at else 0,
                    "success": task.error is None
                }
                for task_id, task in self.tasks.items()
                if task.completed_at
            ]
            
            # Sort by completion time (most recent first)
            completed.sort(key=lambda x: x["completed_at"], reverse=True)
            return completed[:limit]
    
    def cleanup_old_tasks(self, max_age_hours: int = 24) -> int:
        """Clean up old completed tasks."""
        cutoff_time = datetime.now() - threading.timedelta(hours=max_age_hours)
        
        with self._lock:
            old_task_ids = [
                task_id for task_id, task in self.tasks.items()
                if task.completed_at and task.completed_at < cutoff_time
            ]
            
            for task_id in old_task_ids:
                del self.tasks[task_id]
            
            return len(old_task_ids)
    
    def _worker_loop(self) -> None:
        """Main worker loop."""
        while self.running and not self._shutdown_event.is_set():
            try:
                # Get next task (with timeout to check shutdown)
                task = self.queue.get(timeout=1.0)
                
                if task is None:  # Poison pill
                    break
                
                # Execute task
                self._execute_task(task)
                self.queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                # Log error but continue processing
                print(f"Worker error: {e}")
                continue
    
    def _execute_task(self, task: BackgroundTask) -> None:
        """Execute a single task."""
        task.started_at = datetime.now()
        
        try:
            # Check if task was cancelled
            if task.error == "cancelled":
                return
            
            # Execute the function
            result = task.function(*task.args, **task.kwargs)
            task.result = result
            task.completed_at = datetime.now()
            
        except Exception as e:
            task.error = str(e)
            task.completed_at = datetime.now()
    
    def __enter__(self) -> 'BackgroundProcessor':
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.stop()


def run_in_background(processor: BackgroundProcessor, task_id: Optional[str] = None):
    """Decorator to run functions in background."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            nonlocal task_id
            if task_id is None:
                task_id = f"{func.__name__}_{datetime.now().timestamp()}"
            
            return processor.submit_task(task_id, func, args, kwargs)
        
        return wrapper
    return decorator


class PeriodicTask(BaseModel):
    """Represents a periodic background task."""
    name: str
    function: Callable = Field(exclude=True)
    interval_seconds: float
    args: tuple = Field(default_factory=tuple)
    kwargs: Dict[str, Any] = Field(default_factory=dict)
    next_run: datetime = Field(default_factory=datetime.now)
    last_run: Optional[datetime] = None
    enabled: bool = True
    
    class Config:
        arbitrary_types_allowed = True


class PeriodicTaskScheduler(BaseModel):
    """Scheduler for periodic background tasks."""
    
    tasks: Dict[str, PeriodicTask] = Field(default_factory=dict)
    processor: BackgroundProcessor = Field(default_factory=BackgroundProcessor)
    running: bool = False
    check_interval: float = 1.0
    
    def __init__(self, **data):
        super().__init__(**data)
        self.scheduler_thread = None
        self._shutdown_event = threading.Event()
    
    def start(self) -> None:
        """Start the periodic task scheduler."""
        if self.running:
            return
        
        self.processor.start()
        self.running = True
        self._shutdown_event.clear()
        
        self.scheduler_thread = threading.Thread(
            target=self._scheduler_loop,
            name="PeriodicTaskScheduler",
            daemon=True
        )
        self.scheduler_thread.start()
    
    def stop(self) -> None:
        """Stop the periodic task scheduler."""
        if not self.running:
            return
        
        self.running = False
        self._shutdown_event.set()
        
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5.0)
            self.scheduler_thread = None
        
        self.processor.stop()
    
    def add_task(self, name: str, function: Callable, interval_seconds: float,
                args: tuple = (), kwargs: Optional[Dict[str, Any]] = None) -> None:
        """Add a periodic task."""
        task = PeriodicTask(
            name=name,
            function=function,
            interval_seconds=interval_seconds,
            args=args,
            kwargs=kwargs or {}
        )
        self.tasks[name] = task
    
    def remove_task(self, name: str) -> bool:
        """Remove a periodic task."""
        return self.tasks.pop(name, None) is not None
    
    def enable_task(self, name: str) -> bool:
        """Enable a periodic task."""
        task = self.tasks.get(name)
        if task:
            task.enabled = True
            return True
        return False
    
    def disable_task(self, name: str) -> bool:
        """Disable a periodic task."""
        task = self.tasks.get(name)
        if task:
            task.enabled = False
            return True
        return False
    
    def _scheduler_loop(self) -> None:
        """Main scheduler loop."""
        while self.running and not self._shutdown_event.is_set():
            try:
                now = datetime.now()
                
                for task in self.tasks.values():
                    if task.enabled and now >= task.next_run:
                        self._schedule_task(task, now)
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                print(f"Scheduler error: {e}")
                time.sleep(self.check_interval)
    
    def _schedule_task(self, task: PeriodicTask, now: datetime) -> None:
        """Schedule a periodic task for execution."""
        try:
            task_id = f"{task.name}_{now.timestamp()}"
            self.processor.submit_task(task_id, task.function, task.args, task.kwargs)
            
            task.last_run = now
            task.next_run = now + threading.timedelta(seconds=task.interval_seconds)
            
        except Exception as e:
            print(f"Error scheduling task {task.name}: {e}")
    
    def __enter__(self) -> 'PeriodicTaskScheduler':
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.stop()