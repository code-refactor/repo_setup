"""Render Farm Manager package for 3D rendering operations."""

__version__ = "0.1.0"

# Core models and interfaces
from .core.models import (
    RenderJob, RenderNode, RenderClient, JobPriority, RenderJobStatus, NodeStatus,
    NodeCapabilities, EnergyMode, ProgressiveOutputConfig, ResourceAllocation,
    PerformanceMetrics, AuditLogEntry
)

from .core.interfaces import (
    SchedulerInterface, ResourceManagerInterface, NodeSpecializationInterface,
    ProgressiveResultInterface, EnergyOptimizationInterface, AuditInterface
)

# Core components
from .scheduling.deadline_scheduler import DeadlineScheduler
from .resource_management.resource_partitioner import ResourcePartitioner
from .energy_optimization.energy_optimizer import EnergyOptimizer
from .node_specialization.specialization_manager import NodeSpecializationManager
from .progressive_result.progressive_renderer import ProgressiveRenderer

# Common library integration
from .adapters import (
    StatusAdapter, PriorityAdapter, TaskAdapter, NodeAdapter, ResourceAdapter
)

from .integration import (
    RenderFarmSchedulerAdapter, RenderFarmResourceManagerAdapter,
    RenderFarmAuditAdapter, RenderFarmFailureDetector, RenderFarmMetricsCollector,
    UnifiedRenderFarmManager
)

# Alternative common library compatible scheduler
from .scheduling.common_deadline_scheduler import CommonDeadlineScheduler
from .resource_management.common_resource_manager import CommonResourceManager

__all__ = [
    # Core models
    'RenderJob', 'RenderNode', 'RenderClient', 'JobPriority', 'RenderJobStatus', 'NodeStatus',
    'NodeCapabilities', 'EnergyMode', 'ProgressiveOutputConfig', 'ResourceAllocation',
    'PerformanceMetrics', 'AuditLogEntry',
    
    # Core interfaces
    'SchedulerInterface', 'ResourceManagerInterface', 'NodeSpecializationInterface',
    'ProgressiveResultInterface', 'EnergyOptimizationInterface', 'AuditInterface',
    
    # Core components
    'DeadlineScheduler', 'ResourcePartitioner', 'EnergyOptimizer',
    'NodeSpecializationManager', 'ProgressiveRenderer',
    
    # Common library integration
    'StatusAdapter', 'PriorityAdapter', 'TaskAdapter', 'NodeAdapter', 'ResourceAdapter',
    'RenderFarmSchedulerAdapter', 'RenderFarmResourceManagerAdapter',
    'RenderFarmAuditAdapter', 'RenderFarmFailureDetector', 'RenderFarmMetricsCollector',
    'UnifiedRenderFarmManager',
    
    # Common library compatible components
    'CommonDeadlineScheduler', 'CommonResourceManager',
]
