"""
Shared data models and structures for the unified query language interpreter.

This module defines the core data structures that are common across all
persona implementations, providing a unified foundation for query processing,
results handling, and audit logging.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union
from uuid import uuid4


class QueryStatus(str, Enum):
    """Unified query execution status."""
    PENDING = "pending"
    EXECUTING = "executing" 
    COMPLETED = "completed"
    FAILED = "failed"
    DENIED = "denied"
    MODIFIED = "modified"


class LogLevel(str, Enum):
    """Log level enumeration."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AccessAction(str, Enum):
    """Types of access actions for audit logging."""
    QUERY = "query"
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXPORT = "export"
    ANALYZE = "analyze"


@dataclass
class BaseQuery:
    """Universal query representation."""
    query_id: str = field(default_factory=lambda: str(uuid4()))
    raw_query: str = ""
    parsed_query: Optional[Dict[str, Any]] = None
    tables: List[str] = field(default_factory=list)
    fields: List[str] = field(default_factory=list)
    joins: List[Dict[str, Any]] = field(default_factory=list)
    conditions: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UserContext:
    """Universal user context model."""
    user_id: str
    role: str
    purpose: Optional[str] = None
    department: Optional[str] = None
    permissions: Set[str] = field(default_factory=set)
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
    request_time: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QueryResult:
    """Standardized query result format."""
    query_id: str
    status: QueryStatus
    execution_time_ms: int
    timestamp: datetime = field(default_factory=datetime.now)
    user_id: Optional[str] = None
    
    # Results data
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    columns: Optional[List[str]] = None
    data: Optional[List[Dict[str, Any]]] = None
    
    # Legal discovery specific fields
    document_ids: Optional[List[str]] = None
    relevance_scores: Optional[Dict[str, float]] = None
    privilege_status: Optional[Dict[str, str]] = None
    
    # Privacy specific fields
    minimized: bool = False
    anonymized: bool = False
    privacy_reason: Optional[str] = None
    access_granted: bool = True
    
    # Common metadata and error handling
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    reason: Optional[str] = None
    warnings: List[str] = field(default_factory=list)


@dataclass
class AuditEvent:
    """Common audit event structure."""
    event_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    user_id: str = ""
    action: AccessAction = AccessAction.QUERY
    resource: str = ""
    outcome: str = ""
    
    # Event details
    query_id: Optional[str] = None
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
    
    # Execution context
    execution_time_ms: Optional[int] = None
    row_count: Optional[int] = None
    
    # Security and compliance
    risk_score: Optional[float] = None
    compliance_flags: List[str] = field(default_factory=list)
    
    # Extensible metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Integrity verification
    checksum: Optional[str] = None


@dataclass
class PolicyDecision:
    """Shared policy decision format."""
    decision_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Decision outcome
    allowed: bool = False
    action: str = ""  # allow, deny, modify, log
    reason: str = ""
    confidence: float = 0.0
    
    # Context
    user_context: Optional[UserContext] = None
    query_context: Optional[BaseQuery] = None
    resource: str = ""
    
    # Policy details
    matched_rules: List[str] = field(default_factory=list)
    applied_policies: List[str] = field(default_factory=list)
    
    # Enforcement actions
    modifications: Dict[str, Any] = field(default_factory=dict)
    logging_required: bool = True
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Document:
    """Universal document representation."""
    document_id: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Common temporal fields
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    accessed_at: Optional[datetime] = None
    
    # Source information
    source: Optional[str] = None
    source_type: Optional[str] = None
    
    # Content analysis
    content_type: Optional[str] = None
    language: Optional[str] = None
    size_bytes: Optional[int] = None
    
    # Domain-specific extensions
    legal_metadata: Dict[str, Any] = field(default_factory=dict)
    privacy_metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Classification and tags
    tags: Set[str] = field(default_factory=set)
    classification: Optional[str] = None
    sensitivity_level: Optional[str] = None


@dataclass
class QueryExecutionContext:
    """Context for query execution across both personas."""
    query: BaseQuery
    user_context: UserContext
    
    # Execution environment
    execution_id: str = field(default_factory=lambda: str(uuid4()))
    start_time: datetime = field(default_factory=datetime.now)
    timeout_seconds: int = 300
    
    # Data sources and services
    data_sources: Dict[str, Any] = field(default_factory=dict)
    services: Dict[str, Any] = field(default_factory=dict)
    
    # Execution state
    status: QueryStatus = QueryStatus.PENDING
    progress: float = 0.0
    
    # Results and logging
    result: Optional[QueryResult] = None
    audit_events: List[AuditEvent] = field(default_factory=list)
    
    # Error handling
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    # Configuration
    config: Dict[str, Any] = field(default_factory=dict)
    
    def add_audit_event(self, action: AccessAction, resource: str, outcome: str, **kwargs):
        """Add an audit event to the execution context."""
        event = AuditEvent(
            user_id=self.user_context.user_id,
            action=action,
            resource=resource,
            outcome=outcome,
            query_id=self.query.query_id,
            session_id=self.user_context.session_id,
            ip_address=self.user_context.ip_address,
            **kwargs
        )
        self.audit_events.append(event)
        
    def add_error(self, error: str):
        """Add an error to the execution context."""
        self.errors.append(error)
        
    def add_warning(self, warning: str):
        """Add a warning to the execution context."""
        self.warnings.append(warning)
        
    def update_progress(self, progress: float):
        """Update execution progress (0.0 to 1.0)."""
        self.progress = max(0.0, min(1.0, progress))
        
    def get_execution_time_ms(self) -> int:
        """Get execution time in milliseconds."""
        if self.result and self.result.timestamp:
            delta = self.result.timestamp - self.start_time
            return int(delta.total_seconds() * 1000)
        else:
            delta = datetime.now() - self.start_time
            return int(delta.total_seconds() * 1000)


# Type aliases for common patterns
QueryData = Dict[str, Any]
DocumentCollection = Dict[str, Document]
ServiceRegistry = Dict[str, Any]
ConfigDict = Dict[str, Any]