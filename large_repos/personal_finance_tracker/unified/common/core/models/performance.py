import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Dict, Generator, Optional, Any
import os
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


@dataclass
class TimingContext:
    """Context for timing operations."""
    
    operation_name: str
    start_time: float
    end_time: Optional[float] = None
    memory_start: Optional[float] = None
    memory_end: Optional[float] = None
    
    def duration_ms(self) -> float:
        """Get duration in milliseconds."""
        if self.end_time is None:
            return 0.0
        return (self.end_time - self.start_time) * 1000
    
    def memory_used_mb(self) -> Optional[float]:
        """Get memory usage in MB."""
        if self.memory_start is None or self.memory_end is None:
            return None
        return self.memory_end - self.memory_start


class PerformanceTracker:
    """Track performance metrics across operations."""
    
    def __init__(self):
        self.metrics: Dict[str, list] = {}
        self.current_operations: Dict[str, TimingContext] = {}
    
    @contextmanager
    def measure_performance(self, operation_name: str, track_memory: bool = False) -> Generator[TimingContext, None, None]:
        """Context manager for measuring operation performance."""
        start_time = time.time()
        memory_start = None
        
        if track_memory and HAS_PSUTIL:
            try:
                process = psutil.Process(os.getpid())
                memory_start = process.memory_info().rss / 1024 / 1024  # MB
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                memory_start = None
        
        context = TimingContext(
            operation_name=operation_name,
            start_time=start_time,
            memory_start=memory_start
        )
        
        self.current_operations[operation_name] = context
        
        try:
            yield context
        finally:
            end_time = time.time()
            memory_end = None
            
            if track_memory and memory_start is not None and HAS_PSUTIL:
                try:
                    process = psutil.Process(os.getpid())
                    memory_end = process.memory_info().rss / 1024 / 1024  # MB
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    memory_end = None
            
            context.end_time = end_time
            context.memory_end = memory_end
            
            # Store metrics
            if operation_name not in self.metrics:
                self.metrics[operation_name] = []
            
            self.metrics[operation_name].append({
                'timestamp': datetime.now(),
                'duration_ms': context.duration_ms(),
                'memory_used_mb': context.memory_used_mb()
            })
            
            # Clean up current operations
            if operation_name in self.current_operations:
                del self.current_operations[operation_name]
    
    def get_operation_stats(self, operation_name: str) -> Dict[str, Any]:
        """Get statistics for a specific operation."""
        if operation_name not in self.metrics:
            return {}
        
        measurements = self.metrics[operation_name]
        durations = [m['duration_ms'] for m in measurements]
        memory_usage = [m['memory_used_mb'] for m in measurements if m['memory_used_mb'] is not None]
        
        stats = {
            'operation_name': operation_name,
            'total_executions': len(measurements),
            'avg_duration_ms': sum(durations) / len(durations) if durations else 0,
            'min_duration_ms': min(durations) if durations else 0,
            'max_duration_ms': max(durations) if durations else 0,
            'total_duration_ms': sum(durations),
        }
        
        if memory_usage:
            stats.update({
                'avg_memory_mb': sum(memory_usage) / len(memory_usage),
                'min_memory_mb': min(memory_usage),
                'max_memory_mb': max(memory_usage),
            })
        
        return stats
    
    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all tracked operations."""
        return {name: self.get_operation_stats(name) for name in self.metrics.keys()}
    
    def reset_metrics(self, operation_name: Optional[str] = None) -> None:
        """Reset metrics for specific operation or all operations."""
        if operation_name:
            if operation_name in self.metrics:
                del self.metrics[operation_name]
        else:
            self.metrics.clear()
            self.current_operations.clear()
    
    def is_operation_slow(self, operation_name: str, threshold_ms: float) -> bool:
        """Check if operation is slower than threshold."""
        stats = self.get_operation_stats(operation_name)
        if not stats:
            return False
        return stats.get('avg_duration_ms', 0) > threshold_ms
    
    def get_slowest_operations(self, limit: int = 5) -> list:
        """Get the slowest operations by average duration."""
        all_stats = self.get_all_stats()
        sorted_ops = sorted(
            all_stats.items(),
            key=lambda x: x[1].get('avg_duration_ms', 0),
            reverse=True
        )
        return sorted_ops[:limit]
    
    def export_metrics(self) -> Dict[str, Any]:
        """Export all metrics for reporting."""
        return {
            'summary': self.get_all_stats(),
            'raw_data': self.metrics,
            'export_timestamp': datetime.now().isoformat()
        }