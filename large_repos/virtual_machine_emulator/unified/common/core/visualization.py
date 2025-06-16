"""
Visualization framework for the unified virtual machine.

This module provides visualization capabilities for execution traces,
memory access patterns, and performance analysis.
"""

import json
from typing import Any, Dict, List, Optional, Tuple, Union

from .trace import ExecutionTracer, TraceEvent, EventType
from .metrics import PerformanceMetrics


class VisualizationSystem:
    """
    Unified visualization system for execution traces and analysis.
    
    This class provides various visualization formats that can be used
    for debugging, analysis, and educational purposes.
    """
    
    def __init__(self, tracer: Optional[ExecutionTracer] = None, 
                 metrics: Optional[PerformanceMetrics] = None):
        """Initialize the visualization system."""
        self.tracer = tracer
        self.metrics = metrics
    
    def generate_ascii_timeline(self, width: int = 80, height: int = 20,
                               processor_id: Optional[int] = None) -> str:
        """Generate ASCII timeline visualization."""
        if not self.tracer:
            return "No tracer available for timeline generation"
        
        events = self.tracer.get_events(processor_id=processor_id)
        if not events:
            return "No events to display"
        
        lines = [
            "Execution Timeline",
            "=" * width,
            ""
        ]
        
        # Group events by processor and thread
        processors: Dict[int, Dict[str, List[TraceEvent]]] = {}
        
        for event in events:
            pid = event.processor_id or 0
            tid = event.thread_id or "main"
            
            if pid not in processors:
                processors[pid] = {}
            if tid not in processors[pid]:
                processors[pid][tid] = []
            
            processors[pid][tid].append(event)
        
        # Generate timeline for each processor
        for pid in sorted(processors.keys()):
            lines.append(f"Processor {pid}:")
            
            for tid in sorted(processors[pid].keys()):
                thread_events = processors[pid][tid]
                lines.append(f"  Thread {tid}:")
                
                if len(thread_events) > 1:
                    start_time = thread_events[0].timestamp
                    end_time = thread_events[-1].timestamp
                    duration = end_time - start_time
                    
                    timeline = [" "] * (width - 10)
                    
                    for event in thread_events:
                        if duration > 0:
                            pos = int(((event.timestamp - start_time) / duration) * (width - 10))
                            if 0 <= pos < len(timeline):
                                symbol = self._get_event_symbol(event.event_type)
                                timeline[pos] = symbol
                    
                    lines.append(f"    {''.join(timeline)}")
                else:
                    lines.append(f"    [Single event: {self._get_event_symbol(thread_events[0].event_type)}]")
            
            lines.append("")
        
        lines.extend([
            "Legend:",
            "  I=Instruction, M=Memory, C=Context Switch, S=Sync, X=Security, P=Performance, *=Other",
            ""
        ])
        
        return "\n".join(lines)
    
    def _get_event_symbol(self, event_type: EventType) -> str:
        """Get ASCII symbol for event type."""
        symbols = {
            EventType.INSTRUCTION: "I",
            EventType.MEMORY_ACCESS: "M",
            EventType.CONTEXT_SWITCH: "C",
            EventType.SYNCHRONIZATION: "S",
            EventType.SECURITY: "X",
            EventType.PERFORMANCE: "P",
            EventType.SYSTEM_CALL: "Y",
            EventType.CUSTOM: "*"
        }
        return symbols.get(event_type, "*")
    
    def generate_chrome_trace(self) -> str:
        """Generate Chrome tracing format for visualization in chrome://tracing."""
        if not self.tracer:
            return json.dumps({"traceEvents": []})
        
        chrome_trace = self.tracer.export_chrome_trace()
        return json.dumps(chrome_trace, indent=2)
    
    def generate_memory_heatmap(self, width: int = 80, height: int = 20) -> str:
        """Generate ASCII heatmap of memory access patterns."""
        if not self.tracer:
            return "No tracer available for memory heatmap"
        
        memory_events = self.tracer.get_events(event_type=EventType.MEMORY_ACCESS)
        if not memory_events:
            return "No memory access events to display"
        
        # Collect memory addresses
        addresses = []
        for event in memory_events:
            if event.address is not None:
                addresses.append(event.address)
        
        if not addresses:
            return "No memory addresses found in events"
        
        # Calculate address range
        min_addr = min(addresses)
        max_addr = max(addresses)
        addr_range = max_addr - min_addr
        
        if addr_range == 0:
            return "All memory accesses to same address"
        
        # Create heatmap grid
        grid = [[0 for _ in range(width)] for _ in range(height)]
        
        # Map addresses to grid positions
        for addr in addresses:
            x = int(((addr - min_addr) / addr_range) * (width - 1))
            y = int((hash(addr) % height))  # Distribute vertically by hash
            
            if 0 <= x < width and 0 <= y < height:
                grid[y][x] += 1
        
        # Find max access count for scaling
        max_count = max(max(row) for row in grid)
        
        if max_count == 0:
            return "No memory accesses mapped to grid"
        
        # Generate ASCII heatmap
        lines = [
            "Memory Access Heatmap",
            "=" * width,
            f"Address Range: 0x{min_addr:08x} - 0x{max_addr:08x}",
            ""
        ]
        
        # Heat levels
        heat_chars = " .:-=+*#%@"
        
        for row in grid:
            line = ""
            for count in row:
                heat_level = int((count / max_count) * (len(heat_chars) - 1))
                line += heat_chars[heat_level]
            lines.append(line)
        
        lines.extend([
            "",
            f"Heat Scale: '{heat_chars[0]}' (0 accesses) to '{heat_chars[-1]}' ({max_count} accesses)",
            ""
        ])
        
        return "\n".join(lines)
    
    def generate_performance_chart(self, width: int = 60) -> str:
        """Generate ASCII performance chart."""
        if not self.metrics:
            return "No metrics available for performance chart"
        
        metrics = self.metrics.get_metrics()
        
        lines = [
            "Performance Chart",
            "=" * width,
            ""
        ]
        
        # Create bar chart for key metrics
        chart_metrics = [
            ("Instructions/sec", metrics.get("instructions_per_second", 0)),
            ("Memory Acc/sec", metrics.get("memory_accesses_per_second", 0)),
            ("Cache Hit Rate", metrics.get("cache_hit_rate", 0) * 100),
            ("CPI", metrics.get("cycles_per_instruction", 0)),
        ]
        
        # Find max value for scaling
        max_val = max(val for _, val in chart_metrics if val > 0)
        
        if max_val == 0:
            lines.append("No performance data available")
            return "\n".join(lines)
        
        # Generate bars
        bar_width = width - 25
        
        for name, value in chart_metrics:
            if max_val > 0:
                bar_length = int((value / max_val) * bar_width)
                bar = "#" * bar_length + " " * (bar_width - bar_length)
                
                if name == "Cache Hit Rate":
                    lines.append(f"{name:15} |{bar}| {value:.1f}%")
                elif value >= 1000:
                    lines.append(f"{name:15} |{bar}| {value:,.0f}")
                else:
                    lines.append(f"{name:15} |{bar}| {value:.2f}")
        
        lines.append("")
        
        return "\n".join(lines)
    
    def generate_thread_gantt_chart(self, width: int = 80) -> str:
        """Generate Gantt chart showing thread execution over time."""
        if not self.tracer:
            return "No tracer available for Gantt chart"
        
        events = self.tracer.get_events()
        if not events:
            return "No events to display"
        
        # Extract thread activity periods
        thread_periods: Dict[str, List[Tuple[float, float, str]]] = {}
        
        for event in events:
            if event.thread_id and event.event_type == EventType.CONTEXT_SWITCH:
                tid = event.thread_id
                if tid not in thread_periods:
                    thread_periods[tid] = []
                
                # Simplified: assume each context switch represents activity
                activity = event.data.get("reason", "active") if event.data else "active"
                thread_periods[tid].append((event.timestamp, event.timestamp + 0.1, activity))
        
        if not thread_periods:
            return "No thread activity found"
        
        lines = [
            "Thread Gantt Chart",
            "=" * width,
            ""
        ]
        
        # Calculate time range
        all_times = []
        for periods in thread_periods.values():
            for start, end, _ in periods:
                all_times.extend([start, end])
        
        if not all_times:
            return "No time data found"
        
        min_time = min(all_times)
        max_time = max(all_times)
        time_range = max_time - min_time
        
        if time_range == 0:
            return "All events at same time"
        
        # Generate chart for each thread
        chart_width = width - 15
        
        for tid in sorted(thread_periods.keys()):
            periods = thread_periods[tid]
            
            # Create timeline for this thread
            timeline = [" "] * chart_width
            
            for start, end, activity in periods:
                start_pos = int(((start - min_time) / time_range) * chart_width)
                end_pos = int(((end - min_time) / time_range) * chart_width)
                
                # Fill the period
                for pos in range(start_pos, min(end_pos + 1, chart_width)):
                    if 0 <= pos < chart_width:
                        timeline[pos] = "#"
            
            lines.append(f"Thread {tid:8} |{''.join(timeline)}|")
        
        lines.extend([
            "",
            f"Time Range: {min_time:.3f}s - {max_time:.3f}s",
            ""
        ])
        
        return "\n".join(lines)
    
    def generate_control_flow_graph(self) -> Dict[str, Any]:
        """Generate control flow graph data structure."""
        if not self.tracer:
            return {"nodes": [], "edges": [], "error": "No tracer available"}
        
        events = self.tracer.get_events(event_type=EventType.INSTRUCTION)
        
        nodes = set()
        edges = []
        
        prev_pc = None
        
        for event in events:
            if event.data and "pc" in event.data:
                pc = event.data["pc"]
                nodes.add(pc)
                
                if prev_pc is not None and prev_pc != pc - 1:
                    # Control flow change (jump, call, etc.)
                    edges.append({
                        "source": prev_pc,
                        "target": pc,
                        "type": "control_flow"
                    })
                elif prev_pc is not None:
                    # Sequential flow
                    edges.append({
                        "source": prev_pc,
                        "target": pc,
                        "type": "sequential"
                    })
                
                prev_pc = pc
        
        nodes_list = [{"address": addr, "id": f"addr_{addr}"} for addr in sorted(nodes)]
        
        return {
            "nodes": nodes_list,
            "edges": edges,
            "stats": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "control_flow_edges": len([e for e in edges if e["type"] == "control_flow"]),
                "sequential_edges": len([e for e in edges if e["type"] == "sequential"])
            }
        }
    
    def export_visualization_data(self, format_type: str = "json") -> Union[str, Dict[str, Any]]:
        """Export all visualization data in the specified format."""
        data = {
            "timeline": self.generate_ascii_timeline(),
            "memory_heatmap": self.generate_memory_heatmap(),
            "performance_chart": self.generate_performance_chart(),
            "thread_gantt": self.generate_thread_gantt_chart(),
            "control_flow_graph": self.generate_control_flow_graph(),
        }
        
        if self.tracer:
            data["chrome_trace"] = self.tracer.export_chrome_trace()
            data["trace_statistics"] = self.tracer.get_statistics()
        
        if self.metrics:
            data["performance_metrics"] = self.metrics.get_metrics()
            data["efficiency_analysis"] = self.metrics.get_efficiency_analysis()
        
        if format_type == "json":
            return json.dumps(data, indent=2)
        elif format_type == "dict":
            return data
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def generate_summary_report(self) -> str:
        """Generate a comprehensive summary report."""
        lines = [
            "Virtual Machine Execution Report",
            "=" * 50,
            ""
        ]
        
        # Add performance summary
        if self.metrics:
            lines.extend([
                self.metrics.get_performance_summary(),
                ""
            ])
        
        # Add trace statistics
        if self.tracer:
            stats = self.tracer.get_statistics()
            lines.extend([
                "Execution Trace Summary",
                "-" * 30,
                f"Total Events: {stats['total_events']:,}",
                f"Duration: {stats['duration']:.3f}s",
                f"Events/Second: {stats['events_per_second']:,.0f}",
                f"Processors Used: {stats['processors_used']}",
                f"Threads Used: {stats['threads_used']}",
                ""
            ])
        
        # Add visualizations
        lines.extend([
            "Timeline Visualization",
            "-" * 30,
            self.generate_ascii_timeline(width=60, height=10),
            "",
            "Performance Chart",
            "-" * 30,
            self.generate_performance_chart(width=50),
            ""
        ])
        
        return "\n".join(lines)