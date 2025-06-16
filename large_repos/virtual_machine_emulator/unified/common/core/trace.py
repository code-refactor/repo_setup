"""
Execution tracing infrastructure for the unified virtual machine.

This module provides comprehensive execution tracing and analysis capabilities
that can be used by both parallel and security VM implementations.
"""

import json
import time
from dataclasses import dataclass, asdict
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union


class EventType(Enum):
    """Types of trace events."""
    INSTRUCTION = auto()
    MEMORY_ACCESS = auto()
    CONTEXT_SWITCH = auto()
    SYSTEM_CALL = auto()
    SYNCHRONIZATION = auto()
    SECURITY = auto()
    PERFORMANCE = auto()
    CUSTOM = auto()


@dataclass
class TraceEvent:
    """A single trace event."""
    timestamp: float
    event_type: EventType
    processor_id: Optional[int] = None
    thread_id: Optional[str] = None
    address: Optional[int] = None
    data: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        result = asdict(self)
        result["event_type"] = self.event_type.name
        return result


class ExecutionTracer:
    """
    Comprehensive execution tracing system.
    
    This class provides detailed execution tracing capabilities that can be
    used for debugging, analysis, and visualization of VM execution.
    """
    
    def __init__(self, enabled: bool = True, max_events: Optional[int] = None):
        """Initialize the execution tracer."""
        self.enabled = enabled
        self.max_events = max_events
        self.events: List[TraceEvent] = []
        self.start_time = time.time()
        
        # Event filtering
        self.event_filters: Dict[EventType, bool] = {
            event_type: True for event_type in EventType
        }
        
        # Performance metrics
        self.event_counts: Dict[EventType, int] = {
            event_type: 0 for event_type in EventType
        }
    
    def enable(self) -> None:
        """Enable tracing."""
        self.enabled = True
    
    def disable(self) -> None:
        """Disable tracing."""
        self.enabled = False
    
    def set_event_filter(self, event_type: EventType, enabled: bool) -> None:
        """Enable or disable tracing for a specific event type."""
        self.event_filters[event_type] = enabled
    
    def log_event(self, event_type: Union[EventType, str], data: Dict[str, Any],
                  processor_id: Optional[int] = None, thread_id: Optional[str] = None,
                  address: Optional[int] = None) -> None:
        """Log a trace event."""
        if not self.enabled:
            return
        
        # Convert string event types to enum
        if isinstance(event_type, str):
            try:
                event_type = EventType[event_type.upper()]
            except KeyError:
                event_type = EventType.CUSTOM
        
        # Check if this event type is filtered
        if not self.event_filters.get(event_type, True):
            return
        
        # Create the event
        event = TraceEvent(
            timestamp=time.time() - self.start_time,
            event_type=event_type,
            processor_id=processor_id,
            thread_id=thread_id,
            address=address,
            data=data
        )
        
        # Add to events list
        self.events.append(event)
        self.event_counts[event_type] += 1
        
        # Enforce max events limit
        if self.max_events and len(self.events) > self.max_events:
            self.events.pop(0)  # Remove oldest event
    
    def log_instruction(self, instruction: str, processor_id: Optional[int] = None,
                       thread_id: Optional[str] = None, pc: Optional[int] = None,
                       registers: Optional[Dict[str, int]] = None) -> None:
        """Log an instruction execution event."""
        data = {"instruction": instruction}
        if pc is not None:
            data["pc"] = pc
        if registers:
            data["registers"] = registers.copy()
        
        self.log_event(EventType.INSTRUCTION, data, processor_id, thread_id, pc)
    
    def log_memory_access(self, access_type: str, address: int, value: Optional[int] = None,
                         size: int = 1, processor_id: Optional[int] = None,
                         thread_id: Optional[str] = None) -> None:
        """Log a memory access event."""
        data = {
            "access_type": access_type,
            "size": size
        }
        if value is not None:
            data["value"] = value
        
        self.log_event(EventType.MEMORY_ACCESS, data, processor_id, thread_id, address)
    
    def log_context_switch(self, from_thread: Optional[str], to_thread: Optional[str],
                          processor_id: Optional[int] = None, reason: str = "unknown") -> None:
        """Log a context switch event."""
        data = {
            "from_thread": from_thread,
            "to_thread": to_thread,
            "reason": reason
        }
        
        self.log_event(EventType.CONTEXT_SWITCH, data, processor_id, to_thread)
    
    def log_synchronization(self, operation: str, sync_object: str, result: str = "success",
                           processor_id: Optional[int] = None, thread_id: Optional[str] = None) -> None:
        """Log a synchronization event."""
        data = {
            "operation": operation,
            "sync_object": sync_object,
            "result": result
        }
        
        self.log_event(EventType.SYNCHRONIZATION, data, processor_id, thread_id)
    
    def log_security_event(self, event: str, details: Dict[str, Any],
                          processor_id: Optional[int] = None, thread_id: Optional[str] = None,
                          address: Optional[int] = None) -> None:
        """Log a security-related event."""
        data = {"event": event, **details}
        
        self.log_event(EventType.SECURITY, data, processor_id, thread_id, address)
    
    def get_events(self, event_type: Optional[EventType] = None,
                   processor_id: Optional[int] = None, thread_id: Optional[str] = None,
                   start_time: Optional[float] = None, end_time: Optional[float] = None) -> List[TraceEvent]:
        """Get filtered trace events."""
        result = self.events
        
        if event_type is not None:
            result = [e for e in result if e.event_type == event_type]
        
        if processor_id is not None:
            result = [e for e in result if e.processor_id == processor_id]
        
        if thread_id is not None:
            result = [e for e in result if e.thread_id == thread_id]
        
        if start_time is not None:
            result = [e for e in result if e.timestamp >= start_time]
        
        if end_time is not None:
            result = [e for e in result if e.timestamp <= end_time]
        
        return result
    
    def get_timeline(self, processor_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get timeline of events for visualization."""
        events = self.get_events(processor_id=processor_id)
        
        timeline = []
        for event in events:
            timeline_entry = {
                "timestamp": event.timestamp,
                "type": event.event_type.name,
                "processor": event.processor_id,
                "thread": event.thread_id
            }
            
            if event.data:
                if "instruction" in event.data:
                    timeline_entry["instruction"] = event.data["instruction"]
                if "access_type" in event.data:
                    timeline_entry["memory_operation"] = event.data["access_type"]
                if "operation" in event.data:
                    timeline_entry["sync_operation"] = event.data["operation"]
            
            timeline.append(timeline_entry)
        
        return timeline
    
    def export_chrome_trace(self) -> Dict[str, Any]:
        """Export events in Chrome tracing format."""
        trace_events = []
        
        for event in self.events:
            # Convert to Chrome trace format
            chrome_event = {
                "name": event.event_type.name,
                "ph": "I",  # Instant event
                "ts": event.timestamp * 1000000,  # Convert to microseconds
                "pid": event.processor_id or 0,
                "tid": hash(event.thread_id) if event.thread_id else 0,
            }
            
            if event.data:
                chrome_event["args"] = event.data
            
            trace_events.append(chrome_event)
        
        return {"traceEvents": trace_events}
    
    def export_json(self) -> str:
        """Export events as JSON."""
        events_dict = [event.to_dict() for event in self.events]
        return json.dumps(events_dict, indent=2)
    
    def export_csv(self) -> str:
        """Export events as CSV."""
        if not self.events:
            return "timestamp,event_type,processor_id,thread_id,address,data\n"
        
        lines = ["timestamp,event_type,processor_id,thread_id,address,data"]
        
        for event in self.events:
            data_str = json.dumps(event.data) if event.data else ""
            line = f"{event.timestamp},{event.event_type.name},{event.processor_id},{event.thread_id},{event.address},\"{data_str}\""
            lines.append(line)
        
        return "\n".join(lines)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get tracing statistics."""
        if not self.events:
            return {
                "total_events": 0,
                "event_counts": {},
                "duration": 0.0,
                "events_per_second": 0.0
            }
        
        duration = self.events[-1].timestamp - self.events[0].timestamp if len(self.events) > 1 else 0.0
        
        return {
            "total_events": len(self.events),
            "event_counts": dict(self.event_counts),
            "duration": duration,
            "events_per_second": len(self.events) / max(duration, 0.001),
            "processors_used": len(set(e.processor_id for e in self.events if e.processor_id is not None)),
            "threads_used": len(set(e.thread_id for e in self.events if e.thread_id is not None))
        }
    
    def generate_ascii_timeline(self, width: int = 80, processor_id: Optional[int] = None) -> str:
        """Generate ASCII timeline visualization."""
        events = self.get_events(processor_id=processor_id)
        if not events:
            return "No events to display"
        
        lines = ["Execution Timeline", "=" * width, ""]
        
        # Group events by processor
        processors: Dict[int, List[TraceEvent]] = {}
        for event in events:
            pid = event.processor_id or 0
            if pid not in processors:
                processors[pid] = []
            processors[pid].append(event)
        
        # Generate timeline for each processor
        for pid in sorted(processors.keys()):
            processor_events = processors[pid]
            lines.append(f"Processor {pid}:")
            
            # Create timeline bars
            if len(processor_events) > 1:
                start_time = processor_events[0].timestamp
                end_time = processor_events[-1].timestamp
                duration = end_time - start_time
                
                timeline = ["-"] * (width - 20)
                
                for event in processor_events:
                    if duration > 0:
                        pos = int(((event.timestamp - start_time) / duration) * (width - 20))
                        if 0 <= pos < len(timeline):
                            if event.event_type == EventType.INSTRUCTION:
                                timeline[pos] = "I"
                            elif event.event_type == EventType.MEMORY_ACCESS:
                                timeline[pos] = "M"
                            elif event.event_type == EventType.CONTEXT_SWITCH:
                                timeline[pos] = "C"
                            elif event.event_type == EventType.SYNCHRONIZATION:
                                timeline[pos] = "S"
                            else:
                                timeline[pos] = "*"
                
                lines.append(f"  {''.join(timeline)}")
            
            lines.append("")
        
        lines.extend([
            "Legend: I=Instruction, M=Memory, C=Context Switch, S=Sync, *=Other",
            ""
        ])
        
        return "\n".join(lines)
    
    def clear(self) -> None:
        """Clear all trace events."""
        self.events.clear()
        for event_type in self.event_counts:
            self.event_counts[event_type] = 0
    
    def reset(self) -> None:
        """Reset the tracer to initial state."""
        self.clear()
        self.start_time = time.time()