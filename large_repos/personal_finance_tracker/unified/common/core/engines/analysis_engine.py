from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from contextlib import contextmanager

from ..models.analysis_results import AnalysisResult
from ..models.performance import PerformanceTracker
from .cache_manager import CacheManager


class AnalysisEngine(ABC):
    """Base class for all analysis engines across persona implementations."""
    
    def __init__(self, enable_caching: bool = True, enable_performance_tracking: bool = True):
        self.performance_tracker = PerformanceTracker() if enable_performance_tracking else None
        self.cache = CacheManager() if enable_caching else None
        self._configuration: Dict[str, Any] = {}
    
    @abstractmethod
    def analyze(self, data: Any) -> AnalysisResult:
        """Perform analysis on the provided data."""
        pass
    
    def validate_input(self, data: Any) -> bool:
        """Validate input data before analysis."""
        return data is not None
    
    def get_configuration(self) -> Dict[str, Any]:
        """Get current configuration."""
        return self._configuration.copy()
    
    def set_configuration(self, config: Dict[str, Any]) -> None:
        """Set configuration parameters."""
        self._configuration.update(config)
        if self.cache:
            self.cache.clear()  # Clear cache when configuration changes
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get a specific configuration value."""
        return self._configuration.get(key, default)
    
    def set_config_value(self, key: str, value: Any) -> None:
        """Set a specific configuration value."""
        self._configuration[key] = value
        if self.cache:
            self.cache.clear()  # Clear cache when configuration changes
    
    @contextmanager
    def measure_performance(self, operation_name: str):
        """Context manager for measuring operation performance."""
        if self.performance_tracker:
            with self.performance_tracker.measure_performance(operation_name) as context:
                yield context
        else:
            yield None
    
    def clear_cache(self) -> None:
        """Clear the analysis cache."""
        if self.cache:
            self.cache.clear()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        if self.cache:
            return self.cache.get_stats()
        return {}
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        if self.performance_tracker:
            return self.performance_tracker.get_all_stats()
        return {}
    
    def reset_performance_tracking(self) -> None:
        """Reset performance tracking data."""
        if self.performance_tracker:
            self.performance_tracker.reset_metrics()
    
    def is_cached_result_available(self, cache_key: str) -> bool:
        """Check if cached result is available."""
        if not self.cache:
            return False
        return self.cache.has_key(cache_key)
    
    def get_cached_result(self, cache_key: str) -> Optional[Any]:
        """Get cached result."""
        if not self.cache:
            return None
        return self.cache.get(cache_key)
    
    def set_cached_result(self, cache_key: str, result: Any, ttl_seconds: Optional[int] = None) -> None:
        """Set cached result."""
        if self.cache:
            self.cache.set(cache_key, result, ttl_seconds)
    
    def _generate_cache_key(self, data: Any, operation: str = "analyze") -> str:
        """Generate cache key for data and operation."""
        # Create a simple hash-based cache key
        data_str = str(data) if not hasattr(data, '__dict__') else str(vars(data))
        config_str = str(sorted(self._configuration.items()))
        combined = f"{operation}:{data_str}:{config_str}"
        return str(hash(combined))
    
    def analyze_with_caching(self, data: Any, cache_ttl_seconds: Optional[int] = None) -> AnalysisResult:
        """Perform analysis with automatic caching."""
        if not self.cache:
            return self.analyze(data)
        
        cache_key = self._generate_cache_key(data)
        cached_result = self.get_cached_result(cache_key)
        
        if cached_result is not None:
            return cached_result
        
        result = self.analyze(data)
        self.set_cached_result(cache_key, result, cache_ttl_seconds)
        return result
    
    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        cache_enabled = self.cache is not None
        perf_enabled = self.performance_tracker is not None
        return f"{class_name}(caching={cache_enabled}, performance_tracking={perf_enabled})"