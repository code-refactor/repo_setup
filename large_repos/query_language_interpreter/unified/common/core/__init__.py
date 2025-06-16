"""
Core components of the unified query language interpreter.

This module contains the fundamental building blocks for query processing,
audit logging, policy enforcement, and content analysis.
"""

from .models import (
    BaseQuery, QueryResult, QueryStatus, UserContext, QueryExecutionContext,
    AuditEvent, PolicyDecision, Document, AccessAction, LogLevel
)

from .query_framework import (
    BaseQueryParser, DefaultQueryParser, BaseQueryExecutor,
    QueryValidator, QueryResultBuilder, QueryParseError, QueryExecutionError
)

from .audit_system import (
    AuditLogger, InMemoryAuditLogger, AccessLogger,
    MetricsCollector, AuditSearcher
)

from .policy_engine import (
    PolicyEngine, RuleEvaluator, DefaultRuleEvaluator,
    ContextManager, ActionDispatcher, PolicyRule, PolicyAction, RuleType
)

from .content_processor import (
    ContentAnalyzer, TextAnalyzer, PatternMatcher,
    EntityExtractor, FieldProcessor, DocumentAnalyzer, AnalysisResult
)

__all__ = [
    # Models
    'BaseQuery', 'QueryResult', 'QueryStatus', 'UserContext', 'QueryExecutionContext',
    'AuditEvent', 'PolicyDecision', 'Document', 'AccessAction', 'LogLevel',
    
    # Query Framework
    'BaseQueryParser', 'DefaultQueryParser', 'BaseQueryExecutor',
    'QueryValidator', 'QueryResultBuilder', 'QueryParseError', 'QueryExecutionError',
    
    # Audit System
    'AuditLogger', 'InMemoryAuditLogger', 'AccessLogger',
    'MetricsCollector', 'AuditSearcher',
    
    # Policy Engine
    'PolicyEngine', 'RuleEvaluator', 'DefaultRuleEvaluator',
    'ContextManager', 'ActionDispatcher', 'PolicyRule', 'PolicyAction', 'RuleType',
    
    # Content Processor
    'ContentAnalyzer', 'TextAnalyzer', 'PatternMatcher',
    'EntityExtractor', 'FieldProcessor', 'DocumentAnalyzer', 'AnalysisResult',
]
