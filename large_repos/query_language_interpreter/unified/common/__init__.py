"""
Unified Query Language Interpreter - Common Library

This package provides shared functionality for query language interpreters
across different domain-specific implementations (legal discovery, privacy, etc.).
"""

from . import core, utils

__version__ = "1.0.0"
__author__ = "Unified Query Language Interpreter Team"

# Expose key components for easy importing
from .core.models import (
    BaseQuery, QueryResult, QueryStatus, UserContext, 
    QueryExecutionContext, AuditEvent, PolicyDecision, Document
)

from .core.query_framework import (
    BaseQueryParser, DefaultQueryParser, BaseQueryExecutor,
    QueryValidator, QueryResultBuilder
)

from .core.audit_system import (
    AuditLogger, InMemoryAuditLogger, AccessLogger, 
    MetricsCollector, AuditSearcher
)

from .core.policy_engine import (
    PolicyEngine, RuleEvaluator, DefaultRuleEvaluator,
    ContextManager, ActionDispatcher, PolicyRule, PolicyAction
)

from .core.content_processor import (
    ContentAnalyzer, TextAnalyzer, PatternMatcher,
    EntityExtractor, FieldProcessor, DocumentAnalyzer
)

__all__ = [
    # Core modules
    'core', 'utils',
    
    # Models
    'BaseQuery', 'QueryResult', 'QueryStatus', 'UserContext',
    'QueryExecutionContext', 'AuditEvent', 'PolicyDecision', 'Document',
    
    # Query Framework
    'BaseQueryParser', 'DefaultQueryParser', 'BaseQueryExecutor',
    'QueryValidator', 'QueryResultBuilder',
    
    # Audit System
    'AuditLogger', 'InMemoryAuditLogger', 'AccessLogger',
    'MetricsCollector', 'AuditSearcher',
    
    # Policy Engine
    'PolicyEngine', 'RuleEvaluator', 'DefaultRuleEvaluator',
    'ContextManager', 'ActionDispatcher', 'PolicyRule', 'PolicyAction',
    
    # Content Processor
    'ContentAnalyzer', 'TextAnalyzer', 'PatternMatcher',
    'EntityExtractor', 'FieldProcessor', 'DocumentAnalyzer',
]
