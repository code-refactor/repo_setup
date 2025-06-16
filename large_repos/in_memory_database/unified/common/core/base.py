"""
Base classes and mixins for the unified in-memory database library.

This module provides common functionality that can be shared across both
vectordb and syncdb implementations.
"""

import json
import time
import threading
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod


class SerializableMixin:
    """Mixin providing serialization functionality for all components."""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert object to dictionary representation."""
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if hasattr(value, 'to_dict'):
                    result[key] = value.to_dict()
                elif isinstance(value, (list, tuple)):
                    result[key] = [
                        item.to_dict() if hasattr(item, 'to_dict') else item
                        for item in value
                    ]
                elif isinstance(value, dict):
                    result[key] = {
                        k: v.to_dict() if hasattr(v, 'to_dict') else v
                        for k, v in value.items()
                    }
                else:
                    result[key] = value
        return result
    
    def to_json(self) -> str:
        """Convert object to JSON string."""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create object from dictionary representation."""
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str):
        """Create object from JSON string."""
        return cls.from_dict(json.loads(json_str))


class TimestampedMixin:
    """Mixin providing timestamp functionality for tracking creation/modification."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._created_at = time.time()
        self._last_modified = self._created_at
    
    @property
    def created_at(self) -> float:
        """Get creation timestamp."""
        return self._created_at
    
    @property
    def last_modified(self) -> float:
        """Get last modification timestamp."""
        return self._last_modified
    
    def _touch(self):
        """Update last modification timestamp."""
        self._last_modified = time.time()
    
    def get_age(self) -> float:
        """Get age of object in seconds."""
        return time.time() - self._created_at


class MetadataMixin:
    """Mixin providing metadata storage and management."""
    
    def __init__(self, metadata: Optional[Dict[str, Any]] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metadata = metadata or {}
    
    def set_metadata(self, key: str, value: Any):
        """Set metadata value."""
        self.metadata[key] = value
        if hasattr(self, '_touch'):
            self._touch()
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value."""
        return self.metadata.get(key, default)
    
    def has_metadata(self, key: str) -> bool:
        """Check if metadata key exists."""
        return key in self.metadata
    
    def remove_metadata(self, key: str):
        """Remove metadata key."""
        if key in self.metadata:
            del self.metadata[key]
            if hasattr(self, '_touch'):
                self._touch()


class ConfigurableMixin:
    """Base class for components with configuration validation."""
    
    def __init__(self, **config):
        self._config = self._validate_config(**config)
        super().__init__()
    
    def _validate_config(self, **config) -> Dict[str, Any]:
        """Validate configuration parameters. Override in subclasses."""
        return config
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration."""
        return self._config.copy()
    
    def update_config(self, **config):
        """Update configuration with validation."""
        new_config = self._config.copy()
        new_config.update(config)
        validated_config = self._validate_config(**new_config)
        self._config = validated_config
        if hasattr(self, '_touch'):
            self._touch()


class ThreadSafeMixin:
    """Mixin providing thread-safe operations with RLock support."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lock = threading.RLock()
    
    def _with_lock(self, func, *args, **kwargs):
        """Execute function with lock held."""
        with self._lock:
            return func(*args, **kwargs)
    
    @property
    def lock(self):
        """Get the lock object for manual locking."""
        return self._lock


class BaseComponent(SerializableMixin, TimestampedMixin, MetadataMixin, 
                   ConfigurableMixin, ThreadSafeMixin):
    """
    Base class combining all common mixins.
    
    This provides a complete foundation for components that need:
    - Serialization support
    - Timestamp tracking
    - Metadata storage
    - Configuration management
    - Thread safety
    """
    
    def __init__(self, metadata: Optional[Dict[str, Any]] = None, **config):
        super().__init__(metadata=metadata, **config)


class VersionedMixin:
    """Mixin providing version tracking functionality."""
    
    def __init__(self, version: int = 1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._version = version
        self._version_history = [version]
    
    @property
    def version(self) -> int:
        """Get current version."""
        return self._version
    
    @property
    def version_history(self) -> list:
        """Get version history."""
        return self._version_history.copy()
    
    def increment_version(self):
        """Increment version number."""
        self._version += 1
        self._version_history.append(self._version)
        if hasattr(self, '_touch'):
            self._touch()
    
    def set_version(self, version: int):
        """Set specific version number."""
        if version > self._version:
            self._version = version
            self._version_history.append(version)
            if hasattr(self, '_touch'):
                self._touch()


class PerformanceTrackingMixin:
    """Mixin providing performance tracking functionality."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._metrics = {}
        self._operation_counts = {}
        self._operation_times = {}
    
    def track_operation(self, operation_name: str, duration: float):
        """Track operation performance."""
        if operation_name not in self._operation_counts:
            self._operation_counts[operation_name] = 0
            self._operation_times[operation_name] = 0.0
        
        self._operation_counts[operation_name] += 1
        self._operation_times[operation_name] += duration
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics."""
        metrics = {}
        for op_name in self._operation_counts:
            count = self._operation_counts[op_name]
            total_time = self._operation_times[op_name]
            metrics[op_name] = {
                'count': count,
                'total_time': total_time,
                'avg_time': total_time / count if count > 0 else 0.0
            }
        return metrics
    
    def reset_metrics(self):
        """Reset all performance metrics."""
        self._metrics.clear()
        self._operation_counts.clear()
        self._operation_times.clear()