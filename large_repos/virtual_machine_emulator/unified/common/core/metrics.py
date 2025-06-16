"""
Performance metrics and analysis for the unified virtual machine.

This module provides performance measurement and analysis capabilities
that can be used by both parallel and security VM implementations.
"""

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class PerformanceSnapshot:
    """A snapshot of performance metrics at a specific time."""
    timestamp: float
    instructions_executed: int
    memory_accesses: int
    cache_hits: int = 0
    cache_misses: int = 0
    context_switches: int = 0
    thread_count: int = 0
    active_processors: int = 0


class PerformanceMetrics:
    """
    Performance measurement and analysis system.
    
    This class provides comprehensive performance tracking that can be
    used for optimization and analysis of VM execution.
    """
    
    def __init__(self, enable_detailed_tracking: bool = False):
        """Initialize the performance metrics system."""
        self.enable_detailed_tracking = enable_detailed_tracking
        
        # Basic counters
        self.instructions_executed = 0
        self.memory_accesses = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.context_switches = 0
        self.cycles = 0
        
        # Timing
        self.start_time = time.time()
        self.execution_time = 0.0
        
        # Detailed tracking
        if self.enable_detailed_tracking:
            self.snapshots: List[PerformanceSnapshot] = []
            self.instruction_breakdown: Dict[str, int] = {}
            self.memory_access_histogram: Dict[int, int] = {}
            self.latency_measurements: List[Tuple[str, float]] = []
    
    def start_measurement(self) -> None:
        """Start performance measurement."""
        self.start_time = time.time()
    
    def end_measurement(self) -> None:
        """End performance measurement."""
        self.execution_time = time.time() - self.start_time
    
    def increment_instructions(self, count: int = 1, instruction_type: Optional[str] = None) -> None:
        """Increment instruction counter."""
        self.instructions_executed += count
        
        if self.enable_detailed_tracking and instruction_type:
            self.instruction_breakdown[instruction_type] = (
                self.instruction_breakdown.get(instruction_type, 0) + count
            )
    
    def increment_memory_accesses(self, count: int = 1, address: Optional[int] = None) -> None:
        """Increment memory access counter."""
        self.memory_accesses += count
        
        if self.enable_detailed_tracking and address is not None:
            # Track memory access pattern
            page = address // 4096  # 4KB pages
            self.memory_access_histogram[page] = (
                self.memory_access_histogram.get(page, 0) + count
            )
    
    def increment_cache_hits(self, count: int = 1) -> None:
        """Increment cache hit counter."""
        self.cache_hits += count
    
    def increment_cache_misses(self, count: int = 1) -> None:
        """Increment cache miss counter."""
        self.cache_misses += count
    
    def increment_context_switches(self, count: int = 1) -> None:
        """Increment context switch counter."""
        self.context_switches += count
    
    def increment_cycles(self, count: int = 1) -> None:
        """Increment cycle counter."""
        self.cycles += count
    
    def record_latency(self, operation: str, latency: float) -> None:
        """Record operation latency."""
        if self.enable_detailed_tracking:
            self.latency_measurements.append((operation, latency))
    
    def take_snapshot(self, thread_count: int = 0, active_processors: int = 0) -> None:
        """Take a performance snapshot."""
        if not self.enable_detailed_tracking:
            return
        
        snapshot = PerformanceSnapshot(
            timestamp=time.time() - self.start_time,
            instructions_executed=self.instructions_executed,
            memory_accesses=self.memory_accesses,
            cache_hits=self.cache_hits,
            cache_misses=self.cache_misses,
            context_switches=self.context_switches,
            thread_count=thread_count,
            active_processors=active_processors
        )
        
        self.snapshots.append(snapshot)
    
    def get_instructions_per_second(self) -> float:
        """Calculate instructions per second."""
        if self.execution_time <= 0:
            return 0.0
        return self.instructions_executed / self.execution_time
    
    def get_memory_accesses_per_second(self) -> float:
        """Calculate memory accesses per second."""
        if self.execution_time <= 0:
            return 0.0
        return self.memory_accesses / self.execution_time
    
    def get_cache_hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total_accesses = self.cache_hits + self.cache_misses
        if total_accesses == 0:
            return 0.0
        return self.cache_hits / total_accesses
    
    def get_cache_miss_rate(self) -> float:
        """Calculate cache miss rate."""
        return 1.0 - self.get_cache_hit_rate()
    
    def get_cycles_per_instruction(self) -> float:
        """Calculate cycles per instruction (CPI)."""
        if self.instructions_executed == 0:
            return 0.0
        return self.cycles / self.instructions_executed
    
    def get_processor_utilization(self, num_processors: int) -> float:
        """Calculate processor utilization."""
        if self.cycles == 0 or num_processors == 0:
            return 0.0
        
        # This is a simplified calculation
        # In reality, this would depend on parallel execution
        return min(100.0, (self.instructions_executed / self.cycles) * 100.0)
    
    def get_context_switch_overhead(self) -> float:
        """Calculate context switch overhead."""
        if self.instructions_executed == 0:
            return 0.0
        return self.context_switches / self.instructions_executed
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all performance metrics."""
        metrics = {
            # Basic metrics
            "instructions_executed": self.instructions_executed,
            "memory_accesses": self.memory_accesses,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "context_switches": self.context_switches,
            "cycles": self.cycles,
            "execution_time": self.execution_time,
            
            # Derived metrics
            "instructions_per_second": self.get_instructions_per_second(),
            "memory_accesses_per_second": self.get_memory_accesses_per_second(),
            "cache_hit_rate": self.get_cache_hit_rate(),
            "cache_miss_rate": self.get_cache_miss_rate(),
            "cycles_per_instruction": self.get_cycles_per_instruction(),
            "context_switch_overhead": self.get_context_switch_overhead(),
        }
        
        # Add detailed metrics if available
        if self.enable_detailed_tracking:
            metrics.update({
                "instruction_breakdown": dict(self.instruction_breakdown),
                "memory_access_histogram": dict(self.memory_access_histogram),
                "snapshot_count": len(self.snapshots),
                "latency_measurements": len(self.latency_measurements),
            })
            
            # Add latency statistics
            if self.latency_measurements:
                latencies = [lat for _, lat in self.latency_measurements]
                metrics.update({
                    "average_latency": sum(latencies) / len(latencies),
                    "min_latency": min(latencies),
                    "max_latency": max(latencies),
                })
        
        return metrics
    
    def get_performance_summary(self) -> str:
        """Get a human-readable performance summary."""
        metrics = self.get_metrics()
        
        lines = [
            "Performance Summary",
            "=" * 50,
            f"Instructions Executed: {metrics['instructions_executed']:,}",
            f"Memory Accesses: {metrics['memory_accesses']:,}",
            f"Execution Time: {metrics['execution_time']:.3f}s",
            f"Instructions/Second: {metrics['instructions_per_second']:,.0f}",
            f"Memory Accesses/Second: {metrics['memory_accesses_per_second']:,.0f}",
            f"Cache Hit Rate: {metrics['cache_hit_rate']:.1%}",
            f"Cycles per Instruction: {metrics['cycles_per_instruction']:.2f}",
            f"Context Switches: {metrics['context_switches']:,}",
        ]
        
        if self.enable_detailed_tracking and self.instruction_breakdown:
            lines.extend([
                "",
                "Instruction Breakdown:",
                "-" * 30,
            ])
            
            for instr_type, count in sorted(self.instruction_breakdown.items()):
                percentage = (count / metrics['instructions_executed']) * 100
                lines.append(f"{instr_type}: {count:,} ({percentage:.1f}%)")
        
        return "\n".join(lines)
    
    def get_efficiency_analysis(self) -> Dict[str, Any]:
        """Analyze execution efficiency."""
        metrics = self.get_metrics()
        
        analysis = {
            "overall_efficiency": "unknown",
            "bottlenecks": [],
            "recommendations": [],
        }
        
        # Analyze cache performance
        if metrics["cache_hit_rate"] < 0.8:
            analysis["bottlenecks"].append("Low cache hit rate")
            analysis["recommendations"].append("Optimize memory access patterns")
        
        # Analyze CPI
        if metrics["cycles_per_instruction"] > 3.0:
            analysis["bottlenecks"].append("High cycles per instruction")
            analysis["recommendations"].append("Reduce instruction dependencies")
        
        # Analyze context switch overhead
        if metrics["context_switch_overhead"] > 0.1:
            analysis["bottlenecks"].append("High context switch overhead")
            analysis["recommendations"].append("Reduce thread contention")
        
        # Overall efficiency assessment
        if not analysis["bottlenecks"]:
            analysis["overall_efficiency"] = "good"
        elif len(analysis["bottlenecks"]) == 1:
            analysis["overall_efficiency"] = "moderate"
        else:
            analysis["overall_efficiency"] = "poor"
        
        return analysis
    
    def compare_with(self, other: 'PerformanceMetrics') -> Dict[str, Any]:
        """Compare performance with another metrics instance."""
        self_metrics = self.get_metrics()
        other_metrics = other.get_metrics()
        
        comparison = {}
        
        for key in ["instructions_per_second", "cache_hit_rate", "cycles_per_instruction"]:
            if key in self_metrics and key in other_metrics:
                self_val = self_metrics[key]
                other_val = other_metrics[key]
                
                if other_val != 0:
                    improvement = ((self_val - other_val) / other_val) * 100
                    comparison[key] = {
                        "self": self_val,
                        "other": other_val,
                        "improvement_percent": improvement
                    }
        
        return comparison
    
    def reset(self) -> None:
        """Reset all metrics to initial state."""
        self.instructions_executed = 0
        self.memory_accesses = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.context_switches = 0
        self.cycles = 0
        self.execution_time = 0.0
        self.start_time = time.time()
        
        if self.enable_detailed_tracking:
            self.snapshots.clear()
            self.instruction_breakdown.clear()
            self.memory_access_histogram.clear()
            self.latency_measurements.clear()