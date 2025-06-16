from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Any
import uuid


class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"
    INVESTMENT = "investment"
    WITHDRAWAL = "withdrawal"


@dataclass
class BaseTransaction:
    """Base transaction model used across all persona implementations."""
    
    id: str
    date: datetime
    amount: Decimal
    description: str
    transaction_type: TransactionType
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        # Ensure amount is Decimal
        if not isinstance(self.amount, Decimal):
            self.amount = Decimal(str(self.amount))
    
    @classmethod
    def create(cls, 
               date: datetime,
               amount: float,
               description: str,
               transaction_type: TransactionType,
               category: Optional[str] = None,
               tags: Optional[List[str]] = None,
               metadata: Optional[Dict[str, Any]] = None) -> 'BaseTransaction':
        """Factory method to create a new transaction with auto-generated ID."""
        return cls(
            id=str(uuid.uuid4()),
            date=date,
            amount=Decimal(str(amount)),
            description=description,
            transaction_type=transaction_type,
            category=category,
            tags=tags or [],
            metadata=metadata or {}
        )
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the transaction."""
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the transaction."""
        if tag in self.tags:
            self.tags.remove(tag)
    
    def has_tag(self, tag: str) -> bool:
        """Check if transaction has a specific tag."""
        return tag in self.tags
    
    def set_metadata(self, key: str, value: Any) -> None:
        """Set metadata key-value pair."""
        self.metadata[key] = value
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value by key."""
        return self.metadata.get(key, default)
    
    def is_income(self) -> bool:
        """Check if transaction is income."""
        return self.transaction_type == TransactionType.INCOME
    
    def is_expense(self) -> bool:
        """Check if transaction is expense."""
        return self.transaction_type == TransactionType.EXPENSE
    
    def is_investment(self) -> bool:
        """Check if transaction is investment."""
        return self.transaction_type == TransactionType.INVESTMENT
    
    def __str__(self) -> str:
        return f"{self.date.strftime('%Y-%m-%d')} - {self.description}: ${self.amount}"
    
    def __repr__(self) -> str:
        return (f"BaseTransaction(id='{self.id}', date={self.date}, "
                f"amount={self.amount}, description='{self.description}', "
                f"type={self.transaction_type.value})")