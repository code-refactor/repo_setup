from typing import Dict, List, Any, Optional
from datetime import datetime
from ..core.models import PerformanceMetric
from ..core.interfaces import MetricsCollectorInterface
from ..core.utils import Timer


class MetricsCollector(MetricsCollectorInterface):
    """Collects and stores performance metrics"""
    
    def __init__(self):
        self.metrics: List[PerformanceMetric] = []
        self.counters: Dict[str, float] = {}
        self.gauges: Dict[str, float] = {}
    
    def collect_metrics(self, entities: List[Any]) -> Dict[str, Any]:
        """Collect performance metrics from entities"""
        metrics = {}
        
        for entity in entities:
            if hasattr(entity, 'get_metrics'):
                entity_metrics = entity.get_metrics()
                entity_id = getattr(entity, 'id', str(entity))
                metrics[entity_id] = entity_metrics
        
        return metrics
    
    def record_metric(self, name: str, value: float, tags: Dict[str, str] = None) -> None:
        """Record a single metric"""
        metric = PerformanceMetric(
            name=name,
            value=value,
            unit="",
            timestamp=datetime.now(),
            tags=tags or {}
        )
        self.metrics.append(metric)
    
    def increment_counter(self, name: str, value: float = 1.0) -> None:
        """Increment a counter metric"""
        self.counters[name] = self.counters.get(name, 0) + value
    
    def set_gauge(self, name: str, value: float) -> None:
        """Set a gauge metric value"""
        self.gauges[name] = value
    
    def get_counter(self, name: str) -> float:
        """Get counter value"""
        return self.counters.get(name, 0)
    
    def get_gauge(self, name: str) -> float:
        """Get gauge value"""
        return self.gauges.get(name, 0)
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics"""
        return {
            'counters': self.counters.copy(),
            'gauges': self.gauges.copy(),
            'metrics_count': len(self.metrics),
            'latest_metrics': [
                {
                    'name': m.name,
                    'value': m.value,
                    'timestamp': m.timestamp.isoformat(),
                    'tags': m.tags
                }
                for m in self.metrics[-10:]  # Last 10 metrics
            ]
        }


class PerformanceMonitor:
    """Monitor and track performance of operations"""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.operation_timers: Dict[str, Timer] = {}
    
    def start_operation(self, operation_name: str) -> Timer:
        """Start timing an operation"""
        timer = Timer(operation_name)
        timer.__enter__()
        self.operation_timers[operation_name] = timer
        return timer
    
    def end_operation(self, operation_name: str, tags: Dict[str, str] = None) -> Optional[float]:
        """End timing an operation and record the metric"""
        if operation_name not in self.operation_timers:
            return None
        
        timer = self.operation_timers[operation_name]
        timer.__exit__(None, None, None)
        
        elapsed = timer.elapsed
        if elapsed is not None:
            self.metrics_collector.record_metric(
                f"{operation_name}_duration_seconds",
                elapsed,
                tags
            )
        
        del self.operation_timers[operation_name]
        return elapsed
    
    def measure_operation(self, operation_name: str, tags: Dict[str, str] = None):
        """Context manager for measuring operation performance"""
        return OperationTimer(self, operation_name, tags)
    
    def record_throughput(self, operation_name: str, count: int, duration_seconds: float, 
                         tags: Dict[str, str] = None) -> None:
        """Record throughput metrics for an operation"""
        if duration_seconds > 0:
            throughput = count / duration_seconds
            self.metrics_collector.record_metric(
                f"{operation_name}_throughput_per_second",
                throughput,
                tags
            )
    
    def record_resource_usage(self, resource_type: str, usage_value: float, 
                             capacity_value: float, tags: Dict[str, str] = None) -> None:
        """Record resource usage metrics"""
        # Record absolute usage
        self.metrics_collector.record_metric(
            f"resource_{resource_type}_usage",
            usage_value,
            tags
        )
        
        # Record utilization percentage
        if capacity_value > 0:
            utilization = (usage_value / capacity_value) * 100
            self.metrics_collector.record_metric(
                f"resource_{resource_type}_utilization_percent",
                utilization,
                tags
            )


class OperationTimer:
    """Context manager for timing operations"""
    
    def __init__(self, monitor: PerformanceMonitor, operation_name: str, 
                 tags: Dict[str, str] = None):
        self.monitor = monitor
        self.operation_name = operation_name
        self.tags = tags
        self.timer = None
    
    def __enter__(self):
        self.timer = self.monitor.start_operation(self.operation_name)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.monitor.end_operation(self.operation_name, self.tags)