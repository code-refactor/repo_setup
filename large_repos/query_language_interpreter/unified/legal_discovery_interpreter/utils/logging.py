"""Logging utilities for the legal discovery interpreter.

This module now integrates with the common audit system while maintaining
backward compatibility with the existing legal discovery logger interface.
"""

import logging
import os
import json
import datetime
from typing import Dict, Any, Optional

from common.core import AuditLogger, InMemoryAuditLogger, AccessLogger, AuditEvent, AccessAction, LogLevel


class LegalDiscoveryLogger:
    """Logger for legal discovery operations.
    
    This logger now integrates with the common audit system while maintaining
    backward compatibility. It ensures that all operations are properly logged 
    for transparency and defensibility in court proceedings.
    """
    
    def __init__(
        self,
        name: str,
        log_dir: str = "logs",
        file_level: int = logging.INFO,
        console_level: int = logging.WARNING,
        format_string: Optional[str] = None,
        audit_logger: Optional[AuditLogger] = None,
    ):
        """Initialize the logger.
        
        Args:
            name: Logger name
            log_dir: Directory to store log files
            file_level: Logging level for file handler
            console_level: Logging level for console handler
            format_string: Custom format string for log messages
            audit_logger: Optional audit logger instance, creates InMemoryAuditLogger if None
        """
        self.name = name
        self.log_dir = log_dir
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Capture all levels
        
        # Initialize the common audit system
        if audit_logger is None:
            audit_logger = InMemoryAuditLogger()
        self._audit_logger = audit_logger
        self._access_logger = AccessLogger(audit_logger)
        
        # Create the log directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Set the format string
        if format_string is None:
            format_string = (
                "%(asctime)s [%(levelname)s] %(name)s - "
                "%(message)s (%(filename)s:%(lineno)d)"
            )
        
        formatter = logging.Formatter(format_string)
        
        # Add a file handler
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        file_handler = logging.FileHandler(
            os.path.join(log_dir, f"{name}-{timestamp}.log")
        )
        file_handler.setLevel(file_level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Add a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Keep the traditional audit logger for backward compatibility
        audit_handler = logging.FileHandler(
            os.path.join(log_dir, f"{name}-audit-{timestamp}.log")
        )
        audit_handler.setLevel(logging.INFO)
        audit_handler.setFormatter(formatter)
        self.audit_logger = logging.getLogger(f"{name}.audit")
        self.audit_logger.setLevel(logging.INFO)
        self.audit_logger.addHandler(audit_handler)
    
    def debug(self, message: str) -> None:
        """Log a debug message.
        
        Args:
            message: Message to log
        """
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """Log an info message.
        
        Args:
            message: Message to log
        """
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log a warning message.
        
        Args:
            message: Message to log
        """
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log an error message.
        
        Args:
            message: Message to log
        """
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """Log a critical message.
        
        Args:
            message: Message to log
        """
        self.logger.critical(message)
    
    def audit(self, action: str, details: Dict[str, Any], user: Optional[str] = None) -> str:
        """Log an audit event.
        
        Args:
            action: Action being audited
            details: Details of the action
            user: User performing the action
            
        Returns:
            Event ID of the logged audit event
        """
        # Map action string to AccessAction enum
        access_action = self._map_action_to_enum(action)
        
        # Extract resource information from details if available
        resource = details.get('resource', action)
        if 'query' in details:
            resource = f"query: {details['query'][:100]}..." if len(details.get('query', '')) > 100 else f"query: {details['query']}"
        
        # Use the common audit system
        event_id = self._access_logger.log_access(
            user_id=user or "system",
            resource=resource,
            action=access_action,
            outcome="success",
            **details
        )
        
        # Also log to traditional audit logger for backward compatibility
        audit_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "action": action,
            "user": user,
            "details": details,
        }
        self.audit_logger.info(json.dumps(audit_data))
        
        return event_id
    
    def log_query_execution(self, user_id: str, query: str, outcome: str, 
                           execution_time_ms: Optional[int] = None,
                           row_count: Optional[int] = None,
                           document_ids: Optional[list] = None) -> str:
        """Log a query execution event using the common audit system.
        
        Args:
            user_id: ID of the user executing the query
            query: Query string that was executed
            outcome: Outcome of the query execution
            execution_time_ms: Execution time in milliseconds
            row_count: Number of results returned
            document_ids: List of document IDs returned
            
        Returns:
            Event ID of the logged audit event
        """
        return self._access_logger.log_query(
            user_id=user_id,
            query=query,
            outcome=outcome,
            execution_time_ms=execution_time_ms,
            row_count=row_count,
            document_ids=document_ids
        )
    
    def log_privilege_detection(self, user_id: str, document_id: str, 
                               privilege_status: str, confidence: float) -> str:
        """Log a privilege detection event.
        
        Args:
            user_id: ID of the user
            document_id: ID of the document analyzed
            privilege_status: Detected privilege status
            confidence: Confidence score of the detection
            
        Returns:
            Event ID of the logged audit event
        """
        return self._access_logger.log_access(
            user_id=user_id,
            resource=f"document:{document_id}",
            action=AccessAction.ANALYZE,
            outcome="privilege_detected" if privilege_status == "PRIVILEGED" else "no_privilege",
            privilege_status=privilege_status,
            confidence=confidence
        )
    
    def get_audit_trail(self, filters: Dict[str, Any] = None) -> list:
        """Get audit trail using the common audit system.
        
        Args:
            filters: Optional filters for the audit trail
            
        Returns:
            List of audit events
        """
        return self._audit_logger.get_audit_trail(filters or {})
    
    def _map_action_to_enum(self, action: str) -> AccessAction:
        """Map action string to AccessAction enum.
        
        Args:
            action: Action string
            
        Returns:
            Corresponding AccessAction enum value
        """
        action_map = {
            'query': AccessAction.QUERY,
            'read': AccessAction.READ,
            'write': AccessAction.WRITE,
            'delete': AccessAction.DELETE,
            'export': AccessAction.EXPORT,
            'analyze': AccessAction.ANALYZE,
        }
        
        return action_map.get(action.lower(), AccessAction.READ)


def get_logger(name: str, audit_logger: Optional[AuditLogger] = None, **kwargs) -> LegalDiscoveryLogger:
    """Get a logger instance.
    
    Args:
        name: Logger name
        audit_logger: Optional audit logger instance
        **kwargs: Additional arguments for LegalDiscoveryLogger
        
    Returns:
        Logger instance
    """
    return LegalDiscoveryLogger(name, audit_logger=audit_logger, **kwargs)