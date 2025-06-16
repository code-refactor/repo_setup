from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from .models import BaseTask, BaseNode, BaseCheckpoint, ResourceRequirement


class SchedulerInterface(ABC):
    """Abstract interface for task scheduling"""
    
    @abstractmethod
    def schedule_tasks(self, tasks: List[BaseTask], nodes: List[BaseNode]) -> Dict[str, str]:
        """Schedule tasks to nodes. Returns mapping of task_id -> node_id"""
        pass
    
    @abstractmethod
    def update_priorities(self, tasks: List[BaseTask]) -> List[BaseTask]:
        """Update task priorities based on scheduling policies"""
        pass
    
    @abstractmethod
    def can_meet_deadline(self, task: BaseTask, nodes: List[BaseNode]) -> bool:
        """Check if task can meet its deadline"""
        pass


class ResourceManagerInterface(ABC):
    """Abstract interface for resource management"""
    
    @abstractmethod
    def allocate_resources(self, entities: List[Any], nodes: List[BaseNode]) -> Dict[str, Dict[str, float]]:
        """Allocate resources to entities"""
        pass
    
    @abstractmethod
    def calculate_resource_usage(self, entity_id: str, tasks: List[BaseTask]) -> Dict[str, float]:
        """Calculate resource usage for an entity"""
        pass


class CheckpointManagerInterface(ABC):
    """Abstract interface for checkpoint management"""
    
    @abstractmethod
    def create_checkpoint(self, entity: Any, checkpoint_type: str) -> BaseCheckpoint:
        """Create a checkpoint for an entity"""
        pass
    
    @abstractmethod
    def validate_checkpoint(self, checkpoint_id: str) -> bool:
        """Validate a checkpoint"""
        pass
    
    @abstractmethod
    def restore_from_checkpoint(self, checkpoint_id: str) -> bool:
        """Restore from a checkpoint"""
        pass


class AuditLogInterface(ABC):
    """Abstract interface for audit logging"""
    
    @abstractmethod
    def log_event(self, event_type: str, description: str, **details) -> None:
        """Log an audit event"""
        pass


class FailureDetectorInterface(ABC):
    """Abstract interface for failure detection"""
    
    @abstractmethod
    def detect_failures(self, tasks: List[BaseTask], nodes: List[BaseNode]) -> List[str]:
        """Detect failed tasks or nodes. Returns list of failed entity IDs"""
        pass
    
    @abstractmethod
    def should_retry(self, task: BaseTask) -> bool:
        """Determine if a failed task should be retried"""
        pass


class MetricsCollectorInterface(ABC):
    """Abstract interface for metrics collection"""
    
    @abstractmethod
    def collect_metrics(self, entities: List[Any]) -> Dict[str, Any]:
        """Collect performance metrics from entities"""
        pass
    
    @abstractmethod
    def record_metric(self, name: str, value: float, tags: Dict[str, str] = None) -> None:
        """Record a single metric"""
        pass