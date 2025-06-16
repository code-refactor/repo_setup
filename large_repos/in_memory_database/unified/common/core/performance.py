"""
Performance monitoring classes for the unified in-memory database library.

This module provides common performance tracking functionality that can be shared
across both vectordb and syncdb implementations.
"""

import time
import threading
from collections import defaultdict, deque
from typing import Dict, List, Any, Optional, Callable, Tuple
from contextlib import contextmanager
from .base import ThreadSafeMixin, TimestampedMixin
from .collections import CircularBuffer


class PerformanceTracker(ThreadSafeMixin, TimestampedMixin):
    """Track performance metrics across operations."""
    
    def __init__(self, max_history: int = 1000):
        super().__init__()
        self._max_history = max_history
        self._metrics: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            'count': 0,
            'total_time': 0.0,
            'min_time': float('inf'),
            'max_time': 0.0,
            'history': CircularBuffer(max_history)
        })
    
    def track_operation(self, operation_name: str, duration: float, 
                       metadata: Optional[Dict[str, Any]] = None):
        """Track operation performance."""
        with self._lock:
            metric = self._metrics[operation_name]
            metric['count'] += 1
            metric['total_time'] += duration
            metric['min_time'] = min(metric['min_time'], duration)
            metric['max_time'] = max(metric['max_time'], duration)
            
            # Store in history with timestamp and metadata
            history_entry = {
                'timestamp': time.time(),
                'duration': duration,
                'metadata': metadata or {}
            }
            metric['history'].append(history_entry)
            
            self._touch()
    
    @contextmanager
    def time_operation(self, operation_name: str, metadata: Optional[Dict[str, Any]] = None):
        """Context manager to time operations."""
        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time
            self.track_operation(operation_name, duration, metadata)
    
    def get_metrics(self, operation_name: Optional[str] = None) -> Dict[str, Any]:
        """Get performance metrics."""
        with self._lock:
            if operation_name:
                if operation_name not in self._metrics:
                    return {}
                metric = self._metrics[operation_name]
                return self._format_metric(operation_name, metric)
            else:
                return {
                    name: self._format_metric(name, metric)
                    for name, metric in self._metrics.items()
                }
    
    def _format_metric(self, name: str, metric: Dict[str, Any]) -> Dict[str, Any]:
        """Format metric for output."""
        count = metric['count']
        total_time = metric['total_time']
        return {
            'operation': name,
            'count': count,
            'total_time': total_time,
            'avg_time': total_time / count if count > 0 else 0.0,
            'min_time': metric['min_time'] if metric['min_time'] != float('inf') else 0.0,
            'max_time': metric['max_time'],
            'history_size': len(metric['history'])
        }
    
    def get_recent_history(self, operation_name: str, count: int = 10) -> List[Dict[str, Any]]:
        """Get recent operation history."""
        with self._lock:
            if operation_name not in self._metrics:
                return []
            
            history = self._metrics[operation_name]['history'].get_latest(count)
            return history
    
    def get_percentiles(self, operation_name: str, 
                       percentiles: List[float] = [50, 90, 95, 99]) -> Dict[float, float]:
        """Calculate percentiles for operation durations."""
        with self._lock:
            if operation_name not in self._metrics:
                return {}
            
            history = self._metrics[operation_name]['history'].get_all()
            if not history:
                return {}
            
            durations = sorted([entry['duration'] for entry in history])
            result = {}
            
            for p in percentiles:
                if not (0 <= p <= 100):
                    continue
                
                if p == 0:
                    result[p] = durations[0]
                elif p == 100:
                    result[p] = durations[-1]
                else:
                    index = int((len(durations) - 1) * p / 100)
                    result[p] = durations[index]
            
            return result
    
    def reset_metrics(self, operation_name: Optional[str] = None):
        """Reset metrics."""
        with self._lock:
            if operation_name:
                if operation_name in self._metrics:
                    del self._metrics[operation_name]
            else:
                self._metrics.clear()
            self._touch()


class MetricsCollector(ThreadSafeMixin):
    """Collect and aggregate metrics from multiple sources."""
    
    def __init__(self):
        super().__init__()
        self._counters: Dict[str, int] = defaultdict(int)
        self._gauges: Dict[str, float] = {}
        self._histograms: Dict[str, List[float]] = defaultdict(list)
        self._timers: Dict[str, PerformanceTracker] = {}
    
    def increment_counter(self, name: str, value: int = 1):
        """Increment counter metric."""
        with self._lock:
            self._counters[name] += value
    
    def set_gauge(self, name: str, value: float):
        """Set gauge metric."""
        with self._lock:
            self._gauges[name] = value
    
    def record_histogram(self, name: str, value: float):
        """Record histogram metric."""
        with self._lock:
            self._histograms[name].append(value)
    
    def get_timer(self, name: str) -> PerformanceTracker:
        """Get or create timer for operation."""
        with self._lock:
            if name not in self._timers:
                self._timers[name] = PerformanceTracker()
            return self._timers[name]
    
    @contextmanager
    def time_operation(self, name: str, metadata: Optional[Dict[str, Any]] = None):
        """Context manager to time operations."""
        timer = self.get_timer(name)
        with timer.time_operation(name, metadata):
            yield
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all collected metrics."""
        with self._lock:
            result = {
                'counters': dict(self._counters),
                'gauges': dict(self._gauges),
                'histograms': {},
                'timers': {}
            }
            
            # Process histograms
            for name, values in self._histograms.items():
                if values:
                    result['histograms'][name] = {
                        'count': len(values),
                        'min': min(values),
                        'max': max(values),
                        'avg': sum(values) / len(values),
                        'sum': sum(values)
                    }
            
            # Process timers
            for name, timer in self._timers.items():
                result['timers'][name] = timer.get_metrics()
            
            return result
    
    def reset_all(self):
        """Reset all metrics."""
        with self._lock:
            self._counters.clear()
            self._gauges.clear()
            self._histograms.clear()
            for timer in self._timers.values():
                timer.reset_metrics()


class BenchmarkRunner:
    """Run performance benchmarks."""
    
    def __init__(self):
        self._results: List[Dict[str, Any]] = []
    
    def benchmark_function(self, func: Callable, args: tuple = (), kwargs: dict = None,
                          iterations: int = 100, warmup: int = 10, 
                          name: Optional[str] = None) -> Dict[str, Any]:
        """Benchmark a function."""
        kwargs = kwargs or {}
        func_name = name or func.__name__
        
        # Warmup
        for _ in range(warmup):
            func(*args, **kwargs)
        
        # Actual benchmark
        durations = []
        for _ in range(iterations):
            start_time = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            durations.append(duration)
        
        # Calculate statistics
        total_time = sum(durations)
        avg_time = total_time / len(durations)
        min_time = min(durations)
        max_time = max(durations)
        
        # Calculate percentiles
        sorted_durations = sorted(durations)
        percentiles = {}
        for p in [50, 90, 95, 99]:
            index = int((len(sorted_durations) - 1) * p / 100)
            percentiles[f'p{p}'] = sorted_durations[index]
        
        benchmark_result = {
            'name': func_name,
            'iterations': iterations,
            'total_time': total_time,
            'avg_time': avg_time,
            'min_time': min_time,
            'max_time': max_time,
            'ops_per_second': iterations / total_time if total_time > 0 else 0,
            'percentiles': percentiles,
            'timestamp': time.time()
        }
        
        self._results.append(benchmark_result)
        return benchmark_result
    
    def benchmark_comparison(self, functions: Dict[str, Tuple[Callable, tuple, dict]], 
                           iterations: int = 100) -> Dict[str, Any]:
        """Benchmark multiple functions for comparison."""
        results = {}
        
        for name, (func, args, kwargs) in functions.items():
            results[name] = self.benchmark_function(
                func, args, kwargs, iterations, name=name
            )
        
        # Find baseline (fastest average time)
        baseline_name = min(results.keys(), key=lambda k: results[k]['avg_time'])
        baseline_time = results[baseline_name]['avg_time']
        
        # Calculate relative performance
        comparison = {
            'baseline': baseline_name,
            'results': {}
        }
        
        for name, result in results.items():
            relative_time = result['avg_time'] / baseline_time if baseline_time > 0 else 1.0
            comparison['results'][name] = {
                **result,
                'relative_time': relative_time,
                'speedup': 1.0 / relative_time if relative_time > 0 else 1.0
            }
        
        return comparison
    
    def get_all_results(self) -> List[Dict[str, Any]]:
        """Get all benchmark results."""
        return self._results.copy()
    
    def clear_results(self):
        """Clear all benchmark results."""
        self._results.clear()


class ResourceMonitor(ThreadSafeMixin):
    """Monitor system resource usage."""
    
    def __init__(self, sample_interval: float = 1.0):
        super().__init__()
        self._sample_interval = sample_interval
        self._monitoring = False
        self._samples: List[Dict[str, Any]] = []
        self._monitor_thread: Optional[threading.Thread] = None
    
    def start_monitoring(self):
        """Start resource monitoring."""
        with self._lock:
            if self._monitoring:
                return
            
            self._monitoring = True
            self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self._monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop resource monitoring."""
        with self._lock:
            self._monitoring = False
            if self._monitor_thread:
                self._monitor_thread.join(timeout=2.0)
                self._monitor_thread = None
    
    def _monitor_loop(self):
        """Resource monitoring loop."""
        import psutil
        process = psutil.Process()
        
        while self._monitoring:
            try:
                sample = {
                    'timestamp': time.time(),
                    'cpu_percent': process.cpu_percent(),
                    'memory_mb': process.memory_info().rss / 1024 / 1024,
                    'memory_percent': process.memory_percent(),
                    'num_threads': process.num_threads(),
                    'num_fds': process.num_fds() if hasattr(process, 'num_fds') else 0
                }
                
                with self._lock:
                    self._samples.append(sample)
                    # Keep only recent samples
                    if len(self._samples) > 1000:
                        self._samples = self._samples[-1000:]
                
                time.sleep(self._sample_interval)
                
            except Exception:
                # Continue monitoring even if we can't get some metrics
                time.sleep(self._sample_interval)
    
    def get_current_usage(self) -> Dict[str, Any]:
        """Get current resource usage."""
        with self._lock:
            if not self._samples:
                return {}
            return self._samples[-1].copy()
    
    def get_usage_history(self, duration_seconds: Optional[float] = None) -> List[Dict[str, Any]]:
        """Get resource usage history."""
        with self._lock:
            if duration_seconds is None:
                return self._samples.copy()
            
            cutoff_time = time.time() - duration_seconds
            return [sample for sample in self._samples if sample['timestamp'] >= cutoff_time]
    
    def get_usage_stats(self, duration_seconds: Optional[float] = None) -> Dict[str, Any]:
        """Get resource usage statistics."""
        history = self.get_usage_history(duration_seconds)
        
        if not history:
            return {}
        
        stats = {}
        for metric in ['cpu_percent', 'memory_mb', 'memory_percent', 'num_threads', 'num_fds']:
            values = [sample[metric] for sample in history if metric in sample]
            if values:
                stats[metric] = {
                    'min': min(values),
                    'max': max(values),
                    'avg': sum(values) / len(values),
                    'current': values[-1] if values else 0
                }
        
        return stats