from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pydantic import BaseModel


class TaskStatus(Enum):
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class NodeStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"
    ERROR = "error"


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class ResourceType(Enum):
    CPU = "cpu"
    MEMORY = "memory"
    GPU = "gpu"
    STORAGE = "storage"


class BaseTask(BaseModel):
    """Base task model with common fields across all personas"""
    id: str
    name: str
    status: TaskStatus
    priority: Priority
    submission_time: datetime
    estimated_duration: timedelta
    progress: float = 0.0
    dependencies: List[str] = []
    metadata: Dict[str, Any] = {}
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            timedelta: lambda v: v.total_seconds()
        }


class BaseNode(BaseModel):
    """Base node model with common fields across all personas"""
    id: str
    name: str
    status: NodeStatus
    cpu_cores: int
    memory_gb: float
    gpu_count: int = 0
    current_load: Dict[ResourceType, float] = {}
    

class ResourceRequirement(BaseModel):
    resource_type: ResourceType
    amount: float
    unit: str


class ResourceCapability(BaseModel):
    resource_type: ResourceType
    total_amount: float
    available_amount: float
    unit: str


class CheckpointMetadata(BaseModel):
    creation_time: datetime
    size_bytes: int
    checksum: str
    entity_type: str
    entity_id: str


class BaseCheckpoint(BaseModel):
    id: str
    metadata: CheckpointMetadata
    status: str
    path: str
    data: Dict[str, Any] = {}


class TimeRange(BaseModel):
    """Represents a time range with start and end times"""
    start_time: datetime
    end_time: datetime
    
    def overlaps_with(self, other: 'TimeRange') -> bool:
        """Check if this time range overlaps with another"""
        return (self.start_time < other.end_time and 
                self.end_time > other.start_time)
    
    def duration(self) -> timedelta:
        """Get the duration of this time range"""
        return self.end_time - self.start_time


class PerformanceMetric(BaseModel):
    """Performance monitoring metric"""
    name: str
    value: float
    unit: str
    timestamp: datetime
    tags: Dict[str, str] = {}


class SystemEvent(BaseModel):
    """System event for audit logging"""
    event_type: str
    description: str
    timestamp: datetime
    entity_id: Optional[str] = None
    details: Dict[str, Any] = {}