import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from collections import defaultdict


class PerformanceMetric(BaseModel):
    """A single performance measurement."""
    name: str
    value: float
    unit: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class OperationTimer(BaseModel):
    """Times operations for performance measurement."""
    operation_name: str
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    
    def start(self) -> None:
        """Start timing the operation."""
        self.start_time = time.perf_counter()
    
    def stop(self) -> float:
        """Stop timing and return duration in milliseconds."""
        if self.start_time is None:
            return 0.0
        
        self.end_time = time.perf_counter()
        duration_ms = (self.end_time - self.start_time) * 1000
        return duration_ms
    
    def __enter__(self) -> 'OperationTimer':
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.stop()


class PerformanceMetrics(BaseModel):
    """Collection of performance metrics."""
    operation_times: Dict[str, List[float]] = Field(default_factory=lambda: defaultdict(list))
    success_rates: Dict[str, List[bool]] = Field(default_factory=lambda: defaultdict(list))
    memory_usage: List[float] = Field(default_factory=list)
    custom_metrics: List[PerformanceMetric] = Field(default_factory=list)
    
    def get_average_time(self, operation: str) -> float:
        """Get average time for an operation."""
        times = self.operation_times.get(operation, [])
        return sum(times) / len(times) if times else 0.0
    
    def get_success_rate(self, operation: str) -> float:
        """Get success rate for an operation."""
        results = self.success_rates.get(operation, [])
        if not results:
            return 0.0
        return sum(results) / len(results)
    
    def get_percentile(self, operation: str, percentile: float) -> float:
        """Get percentile for operation times."""
        times = sorted(self.operation_times.get(operation, []))
        if not times:
            return 0.0
        
        index = int(len(times) * percentile / 100)
        return times[min(index, len(times) - 1)]


class MetricsCollector(BaseModel):
    """Collects and manages performance metrics."""
    
    metrics: PerformanceMetrics = Field(default_factory=PerformanceMetrics)
    max_samples: int = 1000
    collection_enabled: bool = True
    
    def time_operation(self, operation_name: str) -> OperationTimer:
        """Create a timer for an operation."""
        return OperationTimer(operation_name=operation_name)
    
    def record_operation_time(self, operation_name: str, duration_ms: float) -> None:
        """Record the duration of an operation."""
        if not self.collection_enabled:
            return
        
        times = self.metrics.operation_times[operation_name]
        times.append(duration_ms)
        
        # Limit the number of samples
        if len(times) > self.max_samples:
            times[:] = times[-self.max_samples:]
    
    def record_operation_success(self, operation_name: str, success: bool) -> None:
        """Record whether an operation succeeded."""
        if not self.collection_enabled:
            return
        
        results = self.metrics.success_rates[operation_name]
        results.append(success)
        
        # Limit the number of samples
        if len(results) > self.max_samples:
            results[:] = results[-self.max_samples:]
    
    def record_custom_metric(self, name: str, value: float, unit: str, 
                           metadata: Optional[Dict[str, Any]] = None) -> None:
        """Record a custom metric."""
        if not self.collection_enabled:
            return
        
        metric = PerformanceMetric(
            name=name,
            value=value,
            unit=unit,
            metadata=metadata or {}
        )
        
        self.metrics.custom_metrics.append(metric)
        
        # Limit the number of custom metrics
        if len(self.metrics.custom_metrics) > self.max_samples:
            self.metrics.custom_metrics = self.metrics.custom_metrics[-self.max_samples:]
    
    def get_operation_stats(self, operation_name: str) -> Dict[str, Any]:
        """Get comprehensive statistics for an operation."""
        times = self.metrics.operation_times.get(operation_name, [])
        successes = self.metrics.success_rates.get(operation_name, [])
        
        if not times:
            return {
                "operation": operation_name,
                "sample_count": 0,
                "average_time_ms": 0.0,
                "success_rate": 0.0
            }
        
        stats = {
            "operation": operation_name,
            "sample_count": len(times),
            "average_time_ms": sum(times) / len(times),
            "min_time_ms": min(times),
            "max_time_ms": max(times),
            "median_time_ms": self.metrics.get_percentile(operation_name, 50),
            "p95_time_ms": self.metrics.get_percentile(operation_name, 95),
            "p99_time_ms": self.metrics.get_percentile(operation_name, 99),
            "success_rate": self.metrics.get_success_rate(operation_name) if successes else 1.0,
            "total_successes": sum(successes) if successes else len(times),
            "total_failures": len(successes) - sum(successes) if successes else 0
        }
        
        return stats
    
    def get_all_operation_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all operations."""
        all_stats = {}
        
        for operation_name in self.metrics.operation_times.keys():
            all_stats[operation_name] = self.get_operation_stats(operation_name)
        
        return all_stats
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a summary of overall performance."""
        all_stats = self.get_all_operation_stats()
        
        if not all_stats:
            return {
                "total_operations": 0,
                "overall_success_rate": 0.0,
                "average_operation_time_ms": 0.0,
                "slowest_operation": None,
                "fastest_operation": None
            }
        
        # Calculate overall metrics
        total_samples = sum(stats["sample_count"] for stats in all_stats.values())
        overall_success_rate = sum(
            stats["success_rate"] * stats["sample_count"] 
            for stats in all_stats.values()
        ) / total_samples if total_samples > 0 else 0.0
        
        average_time = sum(
            stats["average_time_ms"] * stats["sample_count"] 
            for stats in all_stats.values()
        ) / total_samples if total_samples > 0 else 0.0
        
        # Find slowest and fastest operations
        slowest_op = max(all_stats.items(), key=lambda x: x[1]["average_time_ms"])
        fastest_op = min(all_stats.items(), key=lambda x: x[1]["average_time_ms"])
        
        return {
            "total_operations": len(all_stats),
            "total_samples": total_samples,
            "overall_success_rate": overall_success_rate,
            "average_operation_time_ms": average_time,
            "slowest_operation": {
                "name": slowest_op[0],
                "average_time_ms": slowest_op[1]["average_time_ms"]
            },
            "fastest_operation": {
                "name": fastest_op[0],
                "average_time_ms": fastest_op[1]["average_time_ms"]
            }
        }
    
    def get_recent_metrics(self, minutes: int = 5) -> List[PerformanceMetric]:
        """Get custom metrics from the last N minutes."""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        
        return [
            metric for metric in self.metrics.custom_metrics
            if metric.timestamp >= cutoff_time
        ]
    
    def clear_metrics(self) -> None:
        """Clear all collected metrics."""
        self.metrics = PerformanceMetrics()
    
    def enable_collection(self) -> None:
        """Enable metrics collection."""
        self.collection_enabled = True
    
    def disable_collection(self) -> None:
        """Disable metrics collection."""
        self.collection_enabled = False
    
    def export_metrics(self) -> Dict[str, Any]:
        """Export all metrics for external analysis."""
        return {
            "operation_times": dict(self.metrics.operation_times),
            "success_rates": dict(self.metrics.success_rates),
            "custom_metrics": [metric.model_dump() for metric in self.metrics.custom_metrics],
            "summary": self.get_performance_summary(),
            "export_time": datetime.now().isoformat()
        }
    
    def import_metrics(self, data: Dict[str, Any]) -> None:
        """Import metrics from external data."""
        if "operation_times" in data:
            self.metrics.operation_times = defaultdict(list, data["operation_times"])
        
        if "success_rates" in data:
            self.metrics.success_rates = defaultdict(list, data["success_rates"])
        
        if "custom_metrics" in data:
            self.metrics.custom_metrics = [
                PerformanceMetric(**metric_data) 
                for metric_data in data["custom_metrics"]
            ]


# Decorator for automatic operation timing
def timed_operation(collector: MetricsCollector, operation_name: str):
    """Decorator to automatically time operations."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            timer = collector.time_operation(operation_name)
            success = True
            result = None
            
            try:
                with timer:
                    result = func(*args, **kwargs)
            except Exception as e:
                success = False
                raise e
            finally:
                duration = timer.stop()
                collector.record_operation_time(operation_name, duration)
                collector.record_operation_success(operation_name, success)
            
            return result
        return wrapper
    return decorator