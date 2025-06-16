"""
Core functionality for the unified concurrent task scheduler library.

This module provides the base classes, interfaces, and utilities that are shared
across all persona implementations.
"""

from .models import (
    TaskStatus, NodeStatus, Priority, ResourceType,
    BaseTask, BaseNode, ResourceRequirement, ResourceCapability,
    BaseCheckpoint, CheckpointMetadata, TimeRange,
    PerformanceMetric, SystemEvent
)

from .interfaces import (
    SchedulerInterface, ResourceManagerInterface, CheckpointManagerInterface,
    AuditLogInterface, FailureDetectorInterface, MetricsCollectorInterface
)

from .scheduler import BaseScheduler
from .resource_manager import BaseResourceManager
from .dependency import DependencyResolver
from .checkpoint import BaseCheckpointManager
from .failure_recovery import BaseFailureDetector, RetryPolicy, CircuitBreaker
from .utils import (
    generate_id, datetime_parser, DateTimeEncoder, calculate_checksum,
    Result, safe_divide, safe_percentage, clamp, deep_merge_dicts,
    flatten_dict, Timer, retry_with_backoff, validate_config
)

__all__ = [
    # Enums
    'TaskStatus', 'NodeStatus', 'Priority', 'ResourceType',
    
    # Models
    'BaseTask', 'BaseNode', 'ResourceRequirement', 'ResourceCapability',
    'BaseCheckpoint', 'CheckpointMetadata', 'TimeRange',
    'PerformanceMetric', 'SystemEvent',
    
    # Interfaces
    'SchedulerInterface', 'ResourceManagerInterface', 'CheckpointManagerInterface',
    'AuditLogInterface', 'FailureDetectorInterface', 'MetricsCollectorInterface',
    
    # Core implementations
    'BaseScheduler', 'BaseResourceManager', 'DependencyResolver',
    'BaseCheckpointManager', 'BaseFailureDetector',
    
    # Utilities
    'RetryPolicy', 'CircuitBreaker', 'Result', 'Timer',
    'generate_id', 'datetime_parser', 'DateTimeEncoder', 'calculate_checksum',
    'safe_divide', 'safe_percentage', 'clamp', 'deep_merge_dicts',
    'flatten_dict', 'retry_with_backoff', 'validate_config'
]
