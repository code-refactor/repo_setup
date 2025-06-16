from abc import ABC, abstractmethod
from typing import Any, List, Protocol, runtime_checkable

from ..models.analysis_results import CategoryResult
from ..models.base_transaction import BaseTransaction
from ..engines.categorization_engine import CategorizationRule


@runtime_checkable
class Categorizer(Protocol):
    """Standard interface for all categorizers."""
    
    def categorize(self, item: Any) -> CategoryResult:
        """Categorize a single item."""
        ...
    
    def add_rule(self, rule: CategorizationRule) -> None:
        """Add a categorization rule."""
        ...
    
    def get_categories(self) -> List[str]:
        """Get all available categories."""
        ...


class TransactionCategorizer(ABC):
    """Abstract base class for transaction categorizers."""
    
    @abstractmethod
    def categorize(self, transaction: BaseTransaction) -> CategoryResult:
        """Categorize a single transaction."""
        pass
    
    @abstractmethod
    def batch_categorize(self, transactions: List[BaseTransaction]) -> dict:
        """Categorize multiple transactions."""
        pass
    
    @abstractmethod
    def add_rule(self, rule: CategorizationRule) -> None:
        """Add a categorization rule."""
        pass
    
    @abstractmethod
    def get_categories(self) -> List[str]:
        """Get all available categories."""
        pass
    
    def validate_transaction(self, transaction: BaseTransaction) -> bool:
        """Validate transaction for categorization."""
        return (isinstance(transaction, BaseTransaction) and 
                transaction.description is not None and
                transaction.amount is not None)
    
    def get_confidence_threshold(self) -> float:
        """Get minimum confidence threshold for categorization."""
        return 0.5
    
    def is_confident_categorization(self, result: CategoryResult) -> bool:
        """Check if categorization result meets confidence threshold."""
        return float(result.confidence_score) >= self.get_confidence_threshold()