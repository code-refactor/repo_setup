from typing import Dict, List, Any, Optional
from datetime import datetime
from ..core.models import SystemEvent
from ..core.interfaces import AuditLogInterface


class AuditLogger(AuditLogInterface):
    """Audit logging implementation for tracking system events"""
    
    def __init__(self, max_events: int = 10000):
        self.events: List[SystemEvent] = []
        self.max_events = max_events
    
    def log_event(self, event_type: str, description: str, **details) -> None:
        """Log an audit event"""
        event = SystemEvent(
            event_type=event_type,
            description=description,
            timestamp=datetime.now(),
            entity_id=details.get('entity_id'),
            details=details
        )
        
        self.events.append(event)
        
        # Maintain max events limit
        if len(self.events) > self.max_events:
            self.events = self.events[-self.max_events:]
    
    def get_events(self, event_type: Optional[str] = None, 
                   entity_id: Optional[str] = None,
                   limit: int = 100) -> List[SystemEvent]:
        """Get audit events with optional filtering"""
        filtered_events = self.events
        
        if event_type:
            filtered_events = [e for e in filtered_events if e.event_type == event_type]
        
        if entity_id:
            filtered_events = [e for e in filtered_events if e.entity_id == entity_id]
        
        # Return most recent events first
        return sorted(filtered_events, key=lambda e: e.timestamp, reverse=True)[:limit]
    
    def get_event_summary(self) -> Dict[str, Any]:
        """Get summary of audit events"""
        event_counts = {}
        for event in self.events:
            event_counts[event.event_type] = event_counts.get(event.event_type, 0) + 1
        
        return {
            'total_events': len(self.events),
            'event_types': event_counts,
            'latest_event': self.events[-1].timestamp.isoformat() if self.events else None
        }
    
    def log_task_event(self, task_id: str, event_type: str, description: str, 
                      **details) -> None:
        """Convenience method for logging task events"""
        self.log_event(
            event_type=f"task_{event_type}",
            description=description,
            entity_id=task_id,
            task_id=task_id,
            **details
        )
    
    def log_node_event(self, node_id: str, event_type: str, description: str, 
                      **details) -> None:
        """Convenience method for logging node events"""
        self.log_event(
            event_type=f"node_{event_type}",
            description=description,
            entity_id=node_id,
            node_id=node_id,
            **details
        )
    
    def log_scheduler_event(self, event_type: str, description: str, **details) -> None:
        """Convenience method for logging scheduler events"""
        self.log_event(
            event_type=f"scheduler_{event_type}",
            description=description,
            **details
        )
    
    def clear_events(self) -> None:
        """Clear all audit events"""
        self.events.clear()
    
    def export_events(self, format: str = 'json') -> str:
        """Export events in specified format"""
        if format == 'json':
            import json
            from ..core.utils import DateTimeEncoder
            
            events_data = [
                {
                    'event_type': e.event_type,
                    'description': e.description,
                    'timestamp': e.timestamp,
                    'entity_id': e.entity_id,
                    'details': e.details
                }
                for e in self.events
            ]
            
            return json.dumps(events_data, cls=DateTimeEncoder, indent=2)
        
        elif format == 'csv':
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Header
            writer.writerow(['timestamp', 'event_type', 'entity_id', 'description'])
            
            # Data
            for event in self.events:
                writer.writerow([
                    event.timestamp.isoformat(),
                    event.event_type,
                    event.entity_id or '',
                    event.description
                ])
            
            return output.getvalue()
        
        else:
            raise ValueError(f"Unsupported export format: {format}")