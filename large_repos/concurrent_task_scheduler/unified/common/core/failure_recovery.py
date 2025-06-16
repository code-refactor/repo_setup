import time
from typing import Dict, List, Set, Optional
from datetime import datetime, timedelta
from .models import BaseTask, BaseNode, TaskStatus, NodeStatus
from .interfaces import FailureDetectorInterface


class BaseFailureDetector(FailureDetectorInterface):
    """Base failure detector with common failure detection logic"""
    
    def __init__(self, 
                 task_timeout_seconds: int = 3600,
                 node_ping_timeout_seconds: int = 30,
                 max_retry_attempts: int = 3):
        self.task_timeout_seconds = task_timeout_seconds
        self.node_ping_timeout_seconds = node_ping_timeout_seconds
        self.max_retry_attempts = max_retry_attempts
        self.task_start_times: Dict[str, datetime] = {}
        self.task_retry_counts: Dict[str, int] = {}
        self.node_last_seen: Dict[str, datetime] = {}
    
    def detect_failures(self, tasks: List[BaseTask], nodes: List[BaseNode]) -> List[str]:
        """Detect failed tasks or nodes. Returns list of failed entity IDs"""
        failed_entities = []
        
        # Detect failed tasks
        failed_entities.extend(self._detect_failed_tasks(tasks))
        
        # Detect failed nodes
        failed_entities.extend(self._detect_failed_nodes(nodes))
        
        return failed_entities
    
    def should_retry(self, task: BaseTask) -> bool:
        """Determine if a failed task should be retried"""
        retry_count = self.task_retry_counts.get(task.id, 0)
        return retry_count < self.max_retry_attempts
    
    def record_task_start(self, task_id: str) -> None:
        """Record when a task started running"""
        self.task_start_times[task_id] = datetime.now()
    
    def record_task_retry(self, task_id: str) -> None:
        """Record a retry attempt for a task"""
        self.task_retry_counts[task_id] = self.task_retry_counts.get(task_id, 0) + 1
    
    def record_node_heartbeat(self, node_id: str) -> None:
        """Record a heartbeat from a node"""
        self.node_last_seen[node_id] = datetime.now()
    
    def get_task_runtime(self, task_id: str) -> Optional[timedelta]:
        """Get how long a task has been running"""
        if task_id not in self.task_start_times:
            return None
        return datetime.now() - self.task_start_times[task_id]
    
    def _detect_failed_tasks(self, tasks: List[BaseTask]) -> List[str]:
        """Detect tasks that have failed or timed out"""
        failed_tasks = []
        
        for task in tasks:
            # Check for explicitly failed tasks
            if task.status == TaskStatus.FAILED:
                failed_tasks.append(task.id)
                continue
            
            # Check for running tasks that have exceeded timeout
            if task.status == TaskStatus.RUNNING:
                if task.id in self.task_start_times:
                    runtime = self.get_task_runtime(task.id)
                    if runtime and runtime.total_seconds() > self.task_timeout_seconds:
                        failed_tasks.append(task.id)
        
        return failed_tasks
    
    def _detect_failed_nodes(self, nodes: List[BaseNode]) -> List[str]:
        """Detect nodes that have failed or are unresponsive"""
        failed_nodes = []
        
        for node in nodes:
            # Check for explicitly failed nodes
            if node.status == NodeStatus.ERROR:
                failed_nodes.append(node.id)
                continue
            
            # Check for nodes that haven't sent heartbeat recently
            if node.id in self.node_last_seen:
                time_since_heartbeat = datetime.now() - self.node_last_seen[node.id]
                if time_since_heartbeat.total_seconds() > self.node_ping_timeout_seconds:
                    failed_nodes.append(node.id)
        
        return failed_nodes


class RetryPolicy:
    """Manages retry policies for failed tasks"""
    
    def __init__(self, 
                 base_delay_seconds: float = 1.0,
                 max_delay_seconds: float = 300.0,
                 exponential_base: float = 2.0,
                 jitter: bool = True):
        self.base_delay_seconds = base_delay_seconds
        self.max_delay_seconds = max_delay_seconds
        self.exponential_base = exponential_base
        self.jitter = jitter
    
    def calculate_delay(self, retry_count: int) -> float:
        """Calculate delay before next retry attempt"""
        import random
        
        # Exponential backoff
        delay = self.base_delay_seconds * (self.exponential_base ** retry_count)
        delay = min(delay, self.max_delay_seconds)
        
        # Add jitter to prevent thundering herd
        if self.jitter:
            delay *= (0.5 + random.random() * 0.5)  # 50-100% of calculated delay
        
        return delay
    
    def should_retry_now(self, last_failure_time: datetime, retry_count: int) -> bool:
        """Check if enough time has passed to retry"""
        required_delay = self.calculate_delay(retry_count)
        elapsed = (datetime.now() - last_failure_time).total_seconds()
        return elapsed >= required_delay


class CircuitBreaker:
    """Circuit breaker pattern for handling repeated failures"""
    
    def __init__(self, 
                 failure_threshold: int = 5,
                 recovery_timeout_seconds: int = 60,
                 half_open_max_calls: int = 3):
        self.failure_threshold = failure_threshold
        self.recovery_timeout_seconds = recovery_timeout_seconds
        self.half_open_max_calls = half_open_max_calls
        
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = "closed"  # closed, open, half_open
        self.half_open_calls = 0
    
    def call_succeeded(self) -> None:
        """Record a successful call"""
        self.failure_count = 0
        self.state = "closed"
        self.half_open_calls = 0
    
    def call_failed(self) -> None:
        """Record a failed call"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "open"
    
    def can_execute(self) -> bool:
        """Check if calls can be executed through the circuit breaker"""
        if self.state == "closed":
            return True
        
        if self.state == "open":
            # Check if recovery timeout has passed
            if (self.last_failure_time and 
                (datetime.now() - self.last_failure_time).total_seconds() >= self.recovery_timeout_seconds):
                self.state = "half_open"
                self.half_open_calls = 0
                return True
            return False
        
        if self.state == "half_open":
            if self.half_open_calls < self.half_open_max_calls:
                self.half_open_calls += 1
                return True
            return False
        
        return False
    
    def get_state(self) -> str:
        """Get current circuit breaker state"""
        return self.state