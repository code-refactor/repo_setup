from typing import Dict, List, Optional
from datetime import datetime
from .models import BaseTask, BaseNode, Priority, TaskStatus
from .interfaces import SchedulerInterface


class BaseScheduler(SchedulerInterface):
    """Base scheduler implementation with common scheduling logic"""
    
    def __init__(self):
        self.priority_weights = {
            Priority.LOW: 1,
            Priority.MEDIUM: 2,
            Priority.HIGH: 3,
            Priority.CRITICAL: 4
        }
    
    def schedule_tasks(self, tasks: List[BaseTask], nodes: List[BaseNode]) -> Dict[str, str]:
        """Basic priority-based scheduling algorithm"""
        # Filter schedulable tasks
        schedulable_tasks = [t for t in tasks if t.status in [TaskStatus.PENDING, TaskStatus.QUEUED]]
        
        # Sort tasks by priority and submission time
        sorted_tasks = sorted(
            schedulable_tasks, 
            key=lambda t: (self.priority_weights[t.priority], t.submission_time),
            reverse=True
        )
        
        # Simple round-robin assignment to available nodes
        available_nodes = [n for n in nodes if n.status.value == "online"]
        schedule = {}
        
        for i, task in enumerate(sorted_tasks):
            if available_nodes:
                node = available_nodes[i % len(available_nodes)]
                schedule[task.id] = node.id
        
        return schedule
    
    def update_priorities(self, tasks: List[BaseTask]) -> List[BaseTask]:
        """Update task priorities based on aging and dependencies"""
        # Simple aging algorithm - increase priority for waiting tasks
        for task in tasks:
            if task.status == TaskStatus.QUEUED:
                # Age tasks that have been waiting
                wait_time = (datetime.now() - task.submission_time).total_seconds()
                if wait_time > 3600:  # 1 hour
                    if task.priority != Priority.CRITICAL:
                        task.priority = Priority(min(task.priority.value + 1, 4))
        
        return tasks
    
    def can_meet_deadline(self, task: BaseTask, nodes: List[BaseNode]) -> bool:
        """Basic deadline checking"""
        if 'deadline' not in task.metadata:
            return True
        
        deadline = datetime.fromisoformat(task.metadata['deadline'])
        available_time = (deadline - datetime.now()).total_seconds()
        
        return available_time >= task.estimated_duration.total_seconds()
    
    def should_preempt(self, running_task: BaseTask, pending_task: BaseTask) -> bool:
        """Determine if a running task should be preempted by a pending task"""
        return (self.priority_weights[pending_task.priority] > 
                self.priority_weights[running_task.priority])
    
    def calculate_task_score(self, task: BaseTask) -> float:
        """Calculate scheduling score for a task"""
        base_score = self.priority_weights[task.priority]
        
        # Factor in waiting time
        wait_time = (datetime.now() - task.submission_time).total_seconds()
        wait_factor = min(wait_time / 3600, 2.0)  # Cap at 2x multiplier
        
        # Factor in deadline urgency if present
        deadline_factor = 1.0
        if 'deadline' in task.metadata:
            deadline = datetime.fromisoformat(task.metadata['deadline'])
            time_to_deadline = (deadline - datetime.now()).total_seconds()
            if time_to_deadline > 0:
                urgency = task.estimated_duration.total_seconds() / time_to_deadline
                deadline_factor = min(urgency * 2, 3.0)  # Cap at 3x multiplier
        
        return base_score * (1 + wait_factor) * deadline_factor