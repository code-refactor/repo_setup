"""
Common core functionality for unified personal finance tracker.

This module provides shared infrastructure for all persona implementations including:
- Base data models and transaction structures
- Analysis engines and frameworks
- Categorization systems
- Time-series processing
- Performance tracking and caching
- Utility functions for financial calculations
- Standard interfaces and protocols
"""

# Core models
from .models import (
    BaseTransaction, TransactionType,
    FinancialMetrics, TrendResult, PeriodType,
    AnalysisResult, CategoryResult, PerformanceMetrics,
    PerformanceTracker, TimingContext
)

# Analysis engines
from .engines import (
    AnalysisEngine,
    CategorizationEngine, CategorizationRule,
    TimeSeriesAnalyzer, TimeSeries, TrendSegment,
    CacheManager
)

# Utility functions
from .utils import (
    FinancialCalculations,
    DateHelpers,
    CacheUtils,
    ExportHelpers
)

# Interfaces
from .interfaces import (
    Analyzer, FinancialAnalyzer,
    Categorizer, TransactionCategorizer,
    Reporter, ReportGenerator
)

__version__ = "1.0.0"

__all__ = [
    # Models
    'BaseTransaction', 'TransactionType',
    'FinancialMetrics', 'TrendResult', 'PeriodType', 
    'AnalysisResult', 'CategoryResult', 'PerformanceMetrics',
    'PerformanceTracker', 'TimingContext',
    
    # Engines
    'AnalysisEngine',
    'CategorizationEngine', 'CategorizationRule',
    'TimeSeriesAnalyzer', 'TimeSeries', 'TrendSegment',
    'CacheManager',
    
    # Utils
    'FinancialCalculations',
    'DateHelpers', 
    'CacheUtils',
    'ExportHelpers',
    
    # Interfaces
    'Analyzer', 'FinancialAnalyzer',
    'Categorizer', 'TransactionCategorizer',
    'Reporter', 'ReportGenerator'
]
