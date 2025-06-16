"""
Pattern processing framework for unified pattern matching.

This package provides a comprehensive pattern processing framework that supports
both compliance patterns (for sensitive data detection) and file patterns
(for database file recognition).
"""

from .engine import (
    PatternType,
    PatternCategory,
    PatternMatch,
    BasePattern,
    CompliancePattern,
    FilePattern,
    PatternEngine,
    PatternValidators
)

from .compiler import (
    PatternCompiler,
    PatternOptimizer,
    PatternLibrary
)

from .validators import (
    ValidationSeverity,
    ValidationIssue,
    PatternValidator,
    PatternTester,
    validate_pattern_collection
)

__all__ = [
    # Engine classes
    "PatternType",
    "PatternCategory", 
    "PatternMatch",
    "BasePattern",
    "CompliancePattern",
    "FilePattern",
    "PatternEngine",
    "PatternValidators",
    
    # Compiler classes
    "PatternCompiler",
    "PatternOptimizer",
    "PatternLibrary",
    
    # Validator classes
    "ValidationSeverity",
    "ValidationIssue",
    "PatternValidator",
    "PatternTester",
    "validate_pattern_collection"
]