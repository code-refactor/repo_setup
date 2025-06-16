"""
Unified Personal Finance Tracker - Common Library

This package provides shared functionality for all persona-specific implementations
of the personal finance tracker system. It includes core data models, analysis
engines, utilities, and interfaces that enable code reuse and consistency across
different financial management personas.

Key Components:
- Core models for transactions and financial data
- Analysis engines for categorization and time-series processing  
- Utility functions for calculations and data processing
- Standard interfaces for extensibility
- Performance tracking and caching systems
"""

from . import core

# Re-export commonly used components for convenience
from .core import (
    BaseTransaction, TransactionType,
    AnalysisEngine, CategorizationEngine, 
    FinancialCalculations, DateHelpers,
    FinancialAnalyzer, TransactionCategorizer
)

__version__ = "1.0.0"
__author__ = "Unified Personal Finance Tracker Team"

__all__ = [
    'core',
    'BaseTransaction',
    'TransactionType', 
    'AnalysisEngine',
    'CategorizationEngine',
    'FinancialCalculations',
    'DateHelpers',
    'FinancialAnalyzer',
    'TransactionCategorizer'
]
