"""Ethical Finance - Values-Aligned Financial Management System."""

__version__ = "0.1.0"

from .ethical_screening.screening_migrated import SociallyResponsibleEthicalScreener as EthicalScreener
from .portfolio_analysis.analysis_migrated import SociallyResponsiblePortfolioAnalysisSystem as PortfolioAnalysisSystem
from .impact_measurement.impact_migrated import SociallyResponsibleImpactMeasurementEngine as ImpactMeasurementEngine
from .shareholder_advocacy.advocacy_migrated import SociallyResponsibleShareholderAdvocacyTracker as ShareholderAdvocacyTracker
from .values_budgeting.budgeting_migrated import SociallyResponsibleValuesAlignedBudgeting as ValuesAlignedBudgeting

__all__ = [
    'EthicalScreener',
    'PortfolioAnalysisSystem',
    'ImpactMeasurementEngine', 
    'ShareholderAdvocacyTracker',
    'ValuesAlignedBudgeting'
]