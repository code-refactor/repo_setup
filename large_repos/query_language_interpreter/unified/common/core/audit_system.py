"""
Unified audit and logging system for the query language interpreter.

This module provides comprehensive audit logging capabilities that can be
used across all persona implementations, ensuring consistent tracking of
data access, policy enforcement, and system events.
"""

import hashlib
import hmac
import json
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set

from .models import AuditEvent, AccessAction, LogLevel, UserContext


class AuditLogger(ABC):
    """Abstract base class for audit logging."""
    
    @abstractmethod
    def log_event(self, event: AuditEvent) -> str:
        """
        Log an audit event.
        
        Args:
            event: AuditEvent to log
            
        Returns:
            Event ID of the logged event
        """
        pass
    
    @abstractmethod
    def get_audit_trail(self, filters: Dict[str, Any]) -> List[AuditEvent]:
        """
        Retrieve audit events based on filters.
        
        Args:
            filters: Dictionary of filter criteria
            
        Returns:
            List of matching audit events
        """
        pass


class InMemoryAuditLogger(AuditLogger):
    """In-memory audit logger implementation."""
    
    def __init__(self, max_events: int = 10000, hmac_key: Optional[str] = None):
        self.events: List[AuditEvent] = []
        self.max_events = max_events
        self.hmac_key = hmac_key or "default_audit_key"
        self._event_index: Dict[str, List[int]] = {}
    
    def log_event(self, event: AuditEvent) -> str:
        """Log an audit event to memory."""
        # Generate checksum for integrity
        if self.hmac_key:
            event.checksum = self._generate_checksum(event)
        
        # Add to events list
        self.events.append(event)
        
        # Update index
        self._update_index(event, len(self.events) - 1)
        
        # Trim old events if necessary
        if len(self.events) > self.max_events:
            self._trim_events()
        
        return event.event_id
    
    def get_audit_trail(self, filters: Dict[str, Any]) -> List[AuditEvent]:
        """Retrieve audit events with filtering."""
        filtered_events = []
        
        for event in self.events:
            if self._matches_filters(event, filters):
                filtered_events.append(event)
        
        # Sort by timestamp (newest first)
        filtered_events.sort(key=lambda e: e.timestamp, reverse=True)
        
        return filtered_events
    
    def _generate_checksum(self, event: AuditEvent) -> str:
        """Generate HMAC checksum for event integrity."""
        # Create string representation without checksum
        event_data = {
            'event_id': event.event_id,
            'timestamp': event.timestamp.isoformat(),
            'user_id': event.user_id,
            'action': event.action,
            'resource': event.resource,
            'outcome': event.outcome,
            'metadata': event.metadata
        }
        
        event_string = json.dumps(event_data, sort_keys=True)
        return hmac.new(
            self.hmac_key.encode(), 
            event_string.encode(), 
            hashlib.sha256
        ).hexdigest()
    
    def _update_index(self, event: AuditEvent, position: int):
        """Update event indices for faster searching."""
        # Index by user_id
        if event.user_id not in self._event_index:
            self._event_index[event.user_id] = []
        self._event_index[event.user_id].append(position)
        
        # Index by action
        action_key = f"action_{event.action}"
        if action_key not in self._event_index:
            self._event_index[action_key] = []
        self._event_index[action_key].append(position)
    
    def _matches_filters(self, event: AuditEvent, filters: Dict[str, Any]) -> bool:
        """Check if event matches filter criteria."""
        for key, value in filters.items():
            if key == 'user_id' and event.user_id != value:
                return False
            elif key == 'action' and event.action != value:
                return False
            elif key == 'resource' and event.resource != value:
                return False
            elif key == 'outcome' and event.outcome != value:
                return False
            elif key == 'start_time' and event.timestamp < value:
                return False
            elif key == 'end_time' and event.timestamp > value:
                return False
            elif key == 'query_id' and event.query_id != value:
                return False
        
        return True
    
    def _trim_events(self):
        """Remove oldest events to maintain max_events limit."""
        if len(self.events) <= self.max_events:
            return
        
        # Remove oldest 20% of events
        trim_count = len(self.events) - self.max_events
        self.events = self.events[trim_count:]
        
        # Rebuild index
        self._event_index.clear()
        for i, event in enumerate(self.events):
            self._update_index(event, i)


class AccessLogger:
    """High-level access logging interface."""
    
    def __init__(self, audit_logger: AuditLogger):
        self.audit_logger = audit_logger
        self.session_data: Dict[str, Dict[str, Any]] = {}
    
    def log_query(self, user_id: str, query: str, outcome: str, 
                  execution_time_ms: Optional[int] = None,
                  row_count: Optional[int] = None,
                  tables: Optional[List[str]] = None,
                  **kwargs) -> str:
        """Log a query execution event."""
        event = AuditEvent(
            user_id=user_id,
            action=AccessAction.QUERY,
            resource=f"query: {query[:100]}..." if len(query) > 100 else f"query: {query}",
            outcome=outcome,
            execution_time_ms=execution_time_ms,
            row_count=row_count,
            metadata={
                'query': query,
                'tables': tables or [],
                **kwargs
            }
        )
        
        return self.audit_logger.log_event(event)
    
    def log_access(self, user_id: str, resource: str, action: AccessAction,
                   outcome: str = "success", **kwargs) -> str:
        """Log a data access event."""
        event = AuditEvent(
            user_id=user_id,
            action=action,
            resource=resource,
            outcome=outcome,
            metadata=kwargs
        )
        
        return self.audit_logger.log_event(event)
    
    def log_policy_enforcement(self, user_id: str, resource: str, 
                             policy_name: str, decision: str,
                             reason: str = "", **kwargs) -> str:
        """Log a policy enforcement event."""
        event = AuditEvent(
            user_id=user_id,
            action=AccessAction.READ,  # Policy enforcement typically involves read access
            resource=resource,
            outcome=f"policy_{decision}",
            metadata={
                'policy_name': policy_name,
                'decision': decision,
                'reason': reason,
                **kwargs
            }
        )
        
        return self.audit_logger.log_event(event)
    
    def log_export(self, user_id: str, resource: str, format_type: str,
                   row_count: int, **kwargs) -> str:
        """Log a data export event."""
        event = AuditEvent(
            user_id=user_id,
            action=AccessAction.EXPORT,
            resource=resource,
            outcome="success",
            row_count=row_count,
            metadata={
                'format': format_type,
                'row_count': row_count,
                **kwargs
            }
        )
        
        return self.audit_logger.log_event(event)
    
    def get_user_activity(self, user_id: str, 
                         days: int = 7) -> List[AuditEvent]:
        """Get recent activity for a specific user."""
        start_time = datetime.now() - timedelta(days=days)
        
        filters = {
            'user_id': user_id,
            'start_time': start_time
        }
        
        return self.audit_logger.get_audit_trail(filters)
    
    def get_resource_access(self, resource: str,
                          days: int = 7) -> List[AuditEvent]:
        """Get access history for a specific resource."""
        start_time = datetime.now() - timedelta(days=days)
        
        filters = {
            'resource': resource,
            'start_time': start_time
        }
        
        return self.audit_logger.get_audit_trail(filters)


class MetricsCollector:
    """Collect and track performance metrics."""
    
    def __init__(self):
        self.metrics: Dict[str, List[float]] = {}
        self.counters: Dict[str, int] = {}
        self.start_times: Dict[str, float] = {}
    
    def start_timer(self, metric_name: str) -> str:
        """Start timing a metric."""
        timer_id = f"{metric_name}_{int(time.time() * 1000000)}"
        self.start_times[timer_id] = time.time()
        return timer_id
    
    def end_timer(self, timer_id: str) -> float:
        """End timing and record the metric."""
        if timer_id not in self.start_times:
            return 0.0
        
        elapsed = time.time() - self.start_times[timer_id]
        del self.start_times[timer_id]
        
        # Extract metric name from timer_id
        metric_name = timer_id.rsplit('_', 1)[0]
        self.record_metric(metric_name, elapsed)
        
        return elapsed
    
    def record_metric(self, name: str, value: float):
        """Record a metric value."""
        if name not in self.metrics:
            self.metrics[name] = []
        
        self.metrics[name].append(value)
        
        # Keep only recent metrics (last 1000 values)
        if len(self.metrics[name]) > 1000:
            self.metrics[name] = self.metrics[name][-1000:]
    
    def increment_counter(self, name: str, amount: int = 1):
        """Increment a counter metric."""
        self.counters[name] = self.counters.get(name, 0) + amount
    
    def get_metric_stats(self, name: str) -> Dict[str, float]:
        """Get statistics for a metric."""
        if name not in self.metrics or not self.metrics[name]:
            return {}
        
        values = self.metrics[name]
        values.sort()
        
        return {
            'count': len(values),
            'min': values[0],
            'max': values[-1],
            'avg': sum(values) / len(values),
            'median': values[len(values) // 2],
            'p95': values[int(len(values) * 0.95)],
            'p99': values[int(len(values) * 0.99)]
        }
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all metrics and counters."""
        result = {
            'metrics': {},
            'counters': self.counters.copy()
        }
        
        for name in self.metrics:
            result['metrics'][name] = self.get_metric_stats(name)
        
        return result


class AuditSearcher:
    """Advanced searching and filtering of audit events."""
    
    def __init__(self, audit_logger: AuditLogger):
        self.audit_logger = audit_logger
    
    def search_by_pattern(self, pattern: str, field: str = 'resource',
                         days: int = 30) -> List[AuditEvent]:
        """Search audit events by pattern matching."""
        start_time = datetime.now() - timedelta(days=days)
        events = self.audit_logger.get_audit_trail({'start_time': start_time})
        
        matching_events = []
        for event in events:
            field_value = getattr(event, field, '')
            if pattern.lower() in str(field_value).lower():
                matching_events.append(event)
        
        return matching_events
    
    def find_suspicious_activity(self, days: int = 7) -> List[AuditEvent]:
        """Find potentially suspicious activity patterns."""
        start_time = datetime.now() - timedelta(days=days)
        events = self.audit_logger.get_audit_trail({'start_time': start_time})
        
        suspicious_events = []
        
        # Group events by user
        user_events: Dict[str, List[AuditEvent]] = {}
        for event in events:
            if event.user_id not in user_events:
                user_events[event.user_id] = []
            user_events[event.user_id].append(event)
        
        # Look for suspicious patterns
        for user_id, user_event_list in user_events.items():
            # Too many failed queries
            failed_queries = [e for e in user_event_list 
                            if e.action == AccessAction.QUERY and 'failed' in e.outcome]
            if len(failed_queries) > 10:
                suspicious_events.extend(failed_queries)
            
            # Unusual export activity
            exports = [e for e in user_event_list if e.action == AccessAction.EXPORT]
            if len(exports) > 5:
                suspicious_events.extend(exports)
        
        return suspicious_events
    
    def generate_access_report(self, user_id: Optional[str] = None,
                             days: int = 30) -> Dict[str, Any]:
        """Generate an access report."""
        start_time = datetime.now() - timedelta(days=days)
        filters = {'start_time': start_time}
        if user_id:
            filters['user_id'] = user_id
        
        events = self.audit_logger.get_audit_trail(filters)
        
        # Analyze events
        report = {
            'period': f"{days} days",
            'total_events': len(events),
            'unique_users': len(set(e.user_id for e in events)),
            'actions': {},
            'outcomes': {},
            'most_accessed_resources': {},
            'peak_hours': [0] * 24
        }
        
        # Count actions and outcomes
        for event in events:
            report['actions'][event.action] = report['actions'].get(event.action, 0) + 1
            report['outcomes'][event.outcome] = report['outcomes'].get(event.outcome, 0) + 1
            
            # Track resource access
            resource = event.resource[:50]  # Truncate for readability
            report['most_accessed_resources'][resource] = \
                report['most_accessed_resources'].get(resource, 0) + 1
            
            # Track hourly patterns
            hour = event.timestamp.hour
            report['peak_hours'][hour] += 1
        
        # Sort most accessed resources
        report['most_accessed_resources'] = dict(
            sorted(report['most_accessed_resources'].items(), 
                  key=lambda x: x[1], reverse=True)[:10]
        )
        
        return report