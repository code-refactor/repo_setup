"""Freelancer Financial Management System.

A specialized financial management system designed for freelancers and independent contractors
who experience irregular income patterns and project-based earnings.
"""

__version__ = "0.1.0"

from .expense.categorizer_migrated import FreelancerExpenseCategorizer as ExpenseCategorizer
from .income.income_manager_migrated import FreelancerIncomeManager as IncomeManager
from .project.profitability_analyzer_migrated import FreelancerProjectProfiler as ProjectProfitabilityAnalyzer
from .projection.financial_projector_migrated import FreelancerFinancialProjector as FinancialProjector
from .tax.tax_manager_migrated import FreelancerTaxManager as TaxManager

__all__ = [
    'ExpenseCategorizer',
    'IncomeManager', 
    'ProjectProfitabilityAnalyzer',
    'FinancialProjector',
    'TaxManager'
]
