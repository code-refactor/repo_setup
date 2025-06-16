"""
Common exceptions for the unified concurrent task scheduler library.
"""


class TaskSchedulerError(Exception):
    """Base exception for task scheduler errors"""
    pass


class TaskNotFoundError(TaskSchedulerError):
    """Raised when a task is not found"""
    pass


class NodeNotFoundError(TaskSchedulerError):
    """Raised when a node is not found"""
    pass


class ResourceAllocationError(TaskSchedulerError):
    """Raised when resource allocation fails"""
    pass


class DependencyError(TaskSchedulerError):
    """Raised when there are dependency issues"""
    pass


class CircularDependencyError(DependencyError):
    """Raised when circular dependencies are detected"""
    pass


class CheckpointError(TaskSchedulerError):
    """Raised when checkpoint operations fail"""
    pass


class CheckpointValidationError(CheckpointError):
    """Raised when checkpoint validation fails"""
    pass


class SchedulingError(TaskSchedulerError):
    """Raised when scheduling operations fail"""
    pass


class ConfigurationError(TaskSchedulerError):
    """Raised when there are configuration issues"""
    pass


class AuthenticationError(TaskSchedulerError):
    """Raised when authentication fails"""
    pass


class AuthorizationError(TaskSchedulerError):
    """Raised when authorization fails"""
    pass


class NetworkError(TaskSchedulerError):
    """Raised when network operations fail"""
    pass


class TimeoutError(TaskSchedulerError):
    """Raised when operations timeout"""
    pass


class RetryExhaustedError(TaskSchedulerError):
    """Raised when retry attempts are exhausted"""
    pass