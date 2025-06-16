"""Core models for the Render Farm Manager."""

from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Union
from pydantic import BaseModel, Field
from common.core.models import BaseTask, BaseNode, TaskStatus, NodeStatus, Priority


class JobPriority(str, Enum):
    """Priority levels for render jobs."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ServiceTier(str, Enum):
    """Service tiers for clients."""
    
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"


class NodeType(str, Enum):
    """Types of render nodes."""
    
    CPU = "cpu"
    GPU = "gpu"
    HYBRID = "hybrid"
    SPECIALIZED = "specialized"


class LogLevel(str, Enum):
    """Log levels for the audit logger."""
    
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class RenderJobStatus(str, Enum):
    """Status values for render jobs."""
    
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class NodeStatus(str, Enum):
    """Status values for render nodes."""
    
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"
    ERROR = "error"
    STARTING = "starting"
    STOPPING = "stopping"


class EnergyMode(str, Enum):
    """Energy usage modes for the render farm."""
    
    PERFORMANCE = "performance"  # Maximum performance, disregard energy usage
    BALANCED = "balanced"  # Balance between performance and energy efficiency
    EFFICIENCY = "efficiency"  # Optimize for energy efficiency, may impact performance
    NIGHT_SAVINGS = "night_savings"  # Special mode for overnight operations


class NodeCapabilities(BaseModel):
    """Capabilities and specifications of a render node."""
    
    cpu_cores: int = Field(..., gt=0)
    memory_gb: int = Field(..., gt=0)
    gpu_model: Optional[str] = None
    gpu_count: int = Field(default=0, ge=0)
    gpu_memory_gb: float = Field(default=0, ge=0)
    gpu_compute_capability: float = Field(default=0, ge=0)
    storage_gb: int = Field(..., gt=0)
    specialized_for: List[str] = Field(default_factory=list)


class RenderNode(BaseNode):
    """A node in the render farm capable of executing render jobs."""
    
    capabilities: NodeCapabilities
    power_efficiency_rating: float = Field(..., ge=0, le=100)
    current_job_id: Optional[str] = None
    performance_history: Dict[str, float] = Field(default_factory=dict)
    last_error: Optional[str] = None
    uptime_hours: float = Field(default=0, ge=0)
    
    def __init__(self, **data):
        # Convert capabilities to base node format
        if 'capabilities' in data:
            caps = data['capabilities']
            if isinstance(caps, NodeCapabilities):
                data['cpu_cores'] = caps.cpu_cores
                data['memory_gb'] = caps.memory_gb
                data['gpu_count'] = caps.gpu_count
            elif isinstance(caps, dict):
                data['cpu_cores'] = caps.get('cpu_cores', 1)
                data['memory_gb'] = caps.get('memory_gb', 1)
                data['gpu_count'] = caps.get('gpu_count', 0)
        
        # Convert status if needed
        if 'status' in data and isinstance(data['status'], str):
            try:
                node_status = NodeStatus(data['status'])
                data['status'] = node_status
            except ValueError:
                # Keep original status if not recognized
                pass
        
        super().__init__(**data)
    
    def model_copy(self, **kwargs):
        """Create a copy of the model."""
        return self.__class__(**{**self.model_dump(), **kwargs})
    
    def copy(self, **kwargs):
        """Deprecated copy method."""
        return self.model_copy(**kwargs)


class RenderJob(BaseTask):
    """A rendering job submitted to the farm."""
    
    client_id: str
    job_type: str
    deadline: datetime
    requires_gpu: bool = False
    memory_requirements_gb: int = Field(..., gt=0)
    cpu_requirements: int = Field(..., gt=0)
    scene_complexity: int = Field(..., ge=1, le=10)
    assigned_node_id: Optional[str] = None
    output_path: str
    error_count: int = Field(default=0, ge=0)
    can_be_preempted: bool = True
    supports_progressive_output: bool = False
    supports_checkpoint: bool = False
    last_checkpoint_time: Optional[datetime] = None
    last_progressive_output_time: Optional[datetime] = None
    energy_intensive: bool = False
    
    def __init__(self, **data):
        # Convert render-specific fields to base task format
        if 'estimated_duration_hours' in data:
            data['estimated_duration'] = timedelta(hours=data.pop('estimated_duration_hours'))
        if 'priority' in data and isinstance(data['priority'], JobPriority):
            priority_map = {
                JobPriority.LOW: Priority.LOW,
                JobPriority.MEDIUM: Priority.MEDIUM,
                JobPriority.HIGH: Priority.HIGH,
                JobPriority.CRITICAL: Priority.CRITICAL
            }
            data['priority'] = priority_map[data['priority']]
        if 'status' in data and isinstance(data['status'], RenderJobStatus):
            status_map = {
                RenderJobStatus.PENDING: TaskStatus.PENDING,
                RenderJobStatus.QUEUED: TaskStatus.QUEUED,
                RenderJobStatus.RUNNING: TaskStatus.RUNNING,
                RenderJobStatus.PAUSED: TaskStatus.PAUSED,
                RenderJobStatus.COMPLETED: TaskStatus.COMPLETED,
                RenderJobStatus.FAILED: TaskStatus.FAILED,
                RenderJobStatus.CANCELLED: TaskStatus.CANCELLED
            }
            data['status'] = status_map[data['status']]
        
        # Store render-specific requirements in metadata
        resource_requirements = {}
        if 'cpu_requirements' in data:
            resource_requirements['cpu'] = data['cpu_requirements']
        if 'memory_requirements_gb' in data:
            resource_requirements['memory'] = data['memory_requirements_gb']
        if 'requires_gpu' in data and data['requires_gpu']:
            resource_requirements['gpu'] = 1
        
        if 'metadata' not in data:
            data['metadata'] = {}
        data['metadata']['resource_requirements'] = resource_requirements
        data['metadata']['deadline'] = data['deadline'].isoformat() if 'deadline' in data else None
        
        super().__init__(**data)
    
    @property
    def estimated_duration_hours(self) -> float:
        """Get estimated duration in hours for backward compatibility."""
        return self.estimated_duration.total_seconds() / 3600
    
    @property
    def render_priority(self) -> JobPriority:
        """Get render-specific priority for backward compatibility."""
        priority_map = {
            Priority.LOW: JobPriority.LOW,
            Priority.MEDIUM: JobPriority.MEDIUM,
            Priority.HIGH: JobPriority.HIGH,
            Priority.CRITICAL: JobPriority.CRITICAL
        }
        return priority_map[self.priority]
    
    @property
    def render_status(self) -> RenderJobStatus:
        """Get render-specific status for backward compatibility."""
        status_map = {
            TaskStatus.PENDING: RenderJobStatus.PENDING,
            TaskStatus.QUEUED: RenderJobStatus.QUEUED,
            TaskStatus.RUNNING: RenderJobStatus.RUNNING,
            TaskStatus.PAUSED: RenderJobStatus.PAUSED,
            TaskStatus.COMPLETED: RenderJobStatus.COMPLETED,
            TaskStatus.FAILED: RenderJobStatus.FAILED,
            TaskStatus.CANCELLED: RenderJobStatus.CANCELLED
        }
        return status_map[self.status]
    
    def model_copy(self, **kwargs):
        """Create a copy of the model."""
        return self.__class__(**{**self.model_dump(), **kwargs})
    
    def copy(self, **kwargs):
        """Deprecated copy method."""
        return self.model_copy(**kwargs)


class Client(BaseModel):
    """A client organization that submits render jobs to the farm."""
    
    id: str
    name: str
    sla_tier: str  # premium, standard, basic
    guaranteed_resources: int = Field(..., ge=0)  # Percentage of resources guaranteed
    max_resources: int = Field(..., ge=0)  # Maximum percentage of resources allowed


class RenderClient(BaseModel):
    """A client organization that submits render jobs to the farm."""
    
    client_id: str
    name: str
    service_tier: ServiceTier
    guaranteed_resources: int = Field(default=0, ge=0)  # Percentage of resources guaranteed
    max_resources: int = Field(default=100, ge=0)  # Maximum percentage of resources allowed
    
    @property
    def id(self) -> str:
        """Get the client ID (alias for client_id for compatibility)."""
        return self.client_id
    
    @property
    def sla_tier(self) -> str:
        """Get the SLA tier (alias for service_tier for compatibility)."""
        return self.service_tier
    
    def model_copy(self, **kwargs):
        """Create a copy of the model."""
        return self.__class__(**{**self.model_dump(), **kwargs})
    
    def copy(self, **kwargs):
        """Deprecated copy method."""
        return self.model_copy(**kwargs)


class ProgressiveOutputConfig(BaseModel):
    """Configuration for progressive result generation."""
    
    enabled: bool = True
    interval_minutes: int = Field(default=30, gt=0)
    quality_levels: List[int] = Field(default_factory=lambda: [25, 50, 75])
    max_overhead_percentage: float = Field(default=5.0, ge=0.0, le=100.0)


class ResourceAllocation(BaseModel):
    """Resource allocation for a specific client."""
    
    client_id: str
    allocated_percentage: float = Field(..., ge=0, le=100)
    allocated_nodes: List[str] = Field(default_factory=list)
    borrowed_percentage: float = Field(default=0, ge=0)
    borrowed_from: Dict[str, float] = Field(default_factory=dict)
    lent_percentage: float = Field(default=0, ge=0)
    lent_to: Dict[str, float] = Field(default_factory=dict)


class PerformanceMetrics(BaseModel):
    """Performance metrics for the render farm."""
    
    total_jobs_completed: int = 0
    jobs_completed_on_time: int = 0
    average_utilization_percentage: float = 0.0
    average_node_idle_percentage: float = 0.0
    energy_usage_kwh: float = 0.0
    average_job_turnaround_hours: float = 0.0
    preemptions_count: int = 0
    node_failures_count: int = 0
    optimization_improvement_percentage: float = 0.0


class AuditLogEntry(BaseModel):
    """Entry in the audit log for the render farm."""
    
    timestamp: datetime = Field(default_factory=datetime.now)
    event_type: str
    job_id: Optional[str] = None
    node_id: Optional[str] = None
    client_id: Optional[str] = None
    description: str
    details: Dict = Field(default_factory=dict)