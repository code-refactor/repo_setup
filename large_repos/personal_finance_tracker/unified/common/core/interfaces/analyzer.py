from abc import ABC, abstractmethod
from typing import Any, Dict, List, Protocol, runtime_checkable

from ..models.analysis_results import AnalysisResult
from ..models.base_transaction import BaseTransaction


@runtime_checkable
class Analyzer(Protocol):
    """Standard interface for all analyzers."""
    
    def analyze(self, data: Any) -> AnalysisResult:
        """Perform analysis on the provided data."""
        ...
    
    def validate_input(self, data: Any) -> bool:
        """Validate input data before analysis."""
        ...
    
    def get_configuration(self) -> Dict[str, Any]:
        """Get current configuration."""
        ...


class FinancialAnalyzer(ABC):
    """Abstract base class for financial analyzers."""
    
    @abstractmethod
    def analyze(self, transactions: List[BaseTransaction]) -> AnalysisResult:
        """Analyze financial transactions."""
        pass
    
    @abstractmethod
    def get_summary(self) -> Dict[str, Any]:
        """Get analysis summary."""
        pass
    
    @abstractmethod
    def export_results(self, format_type: str = "json") -> str:
        """Export analysis results in specified format."""
        pass
    
    def validate_transactions(self, transactions: List[BaseTransaction]) -> bool:
        """Validate transaction data."""
        if not transactions:
            return False
        
        for transaction in transactions:
            if not isinstance(transaction, BaseTransaction):
                return False
            if transaction.amount is None or transaction.date is None:
                return False
        
        return True
    
    def filter_transactions_by_category(self, transactions: List[BaseTransaction], 
                                      category: str) -> List[BaseTransaction]:
        """Filter transactions by category."""
        return [t for t in transactions if t.category == category]
    
    def filter_transactions_by_date_range(self, transactions: List[BaseTransaction],
                                        start_date, end_date) -> List[BaseTransaction]:
        """Filter transactions by date range."""
        return [t for t in transactions if start_date <= t.date <= end_date]