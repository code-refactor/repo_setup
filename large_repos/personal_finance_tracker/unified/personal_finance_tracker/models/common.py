"""Common data models for the personal finance tracker."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union
from uuid import UUID, uuid4
from decimal import Decimal

from pydantic import BaseModel, Field, validator

# Import common library components
from common.core.models.base_transaction import BaseTransaction, TransactionType as CommonTransactionType
from common.core.utils.financial_calculations import FinancialCalculations


# Map common transaction types to freelancer-specific categories
class TransactionType(str, Enum):
    """Transaction type enum - extended for freelancer use cases."""

    INCOME = "income"
    EXPENSE = "expense"
    TAX_PAYMENT = "tax_payment"
    TRANSFER = "transfer"
    
    # Map to common library types
    @classmethod
    def to_common_type(cls, transaction_type: 'TransactionType') -> CommonTransactionType:
        """Convert freelancer transaction type to common library type."""
        mapping = {
            cls.INCOME: CommonTransactionType.INCOME,
            cls.EXPENSE: CommonTransactionType.EXPENSE,
            cls.TAX_PAYMENT: CommonTransactionType.EXPENSE,  # Tax payments are expenses
            cls.TRANSFER: CommonTransactionType.TRANSFER
        }
        return mapping.get(transaction_type, CommonTransactionType.EXPENSE)


class AccountType(str, Enum):
    """Account type enum."""

    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT_CARD = "credit_card"
    INVESTMENT = "investment"
    CASH = "cash"


class ExpenseCategory(str, Enum):
    """Expense category enum."""

    BUSINESS_SUPPLIES = "business_supplies"
    SOFTWARE = "software"
    MARKETING = "marketing"
    OFFICE_RENT = "office_rent"
    UTILITIES = "utilities"
    TRAVEL = "travel"
    MEALS = "meals"
    EQUIPMENT = "equipment"
    PROFESSIONAL_DEVELOPMENT = "professional_development"
    PROFESSIONAL_SERVICES = "professional_services"
    HEALTH_INSURANCE = "health_insurance"
    RETIREMENT = "retirement"
    PHONE = "phone"
    INTERNET = "internet"
    CAR = "car"
    HOME_OFFICE = "home_office"
    PERSONAL = "personal"
    OTHER = "other"


class AccountBalance(BaseModel):
    """Account balance model."""

    account_id: str
    account_name: str
    account_type: AccountType
    balance: float
    as_of_date: datetime


class Transaction(BaseTransaction):
    """Freelancer-specific transaction model extending common BaseTransaction."""
    
    def __init__(self, 
                 date: datetime,
                 amount: Union[float, Decimal],
                 description: str,
                 transaction_type: TransactionType,
                 account_id: str,
                 category: Optional[ExpenseCategory] = None,
                 business_use_percentage: Optional[float] = None,
                 project_id: Optional[str] = None,
                 client_id: Optional[str] = None,
                 invoice_id: Optional[str] = None,
                 receipt_path: Optional[str] = None,
                 notes: Optional[str] = None,
                 tags: Optional[List[str]] = None,
                 id: Optional[UUID] = None,
                 **kwargs):
        
        # Convert to common transaction type
        common_type = TransactionType.to_common_type(transaction_type)
        
        # Initialize base transaction
        super().__init__(
            id=str(id or uuid4()),
            date=date,
            amount=Decimal(str(amount)),
            description=description,
            transaction_type=common_type,
            category=category.value if category else None,
            tags=tags or [],
            metadata={}
        )
        
        # Set freelancer-specific metadata
        self.set_metadata('freelancer_transaction_type', transaction_type.value)
        self.set_metadata('account_id', account_id)
        
        if business_use_percentage is not None:
            self.business_use_percentage = business_use_percentage
        if project_id:
            self.set_metadata('project_id', project_id)
        if client_id:
            self.set_metadata('client_id', client_id)
        if invoice_id:
            self.set_metadata('invoice_id', invoice_id)
        if receipt_path:
            self.set_metadata('receipt_path', receipt_path)
        if notes:
            self.set_metadata('notes', notes)
    
    @property
    def business_use_percentage(self) -> Optional[float]:
        """Get business use percentage from metadata."""
        return self.get_metadata('business_use_percentage')
    
    @business_use_percentage.setter
    def business_use_percentage(self, value: Optional[float]):
        """Set business use percentage in metadata with validation."""
        if value is not None and (value < 0 or value > 100):
            raise ValueError("Business use percentage must be between 0 and 100")
        self.set_metadata('business_use_percentage', value)
    
    @property
    def account_id(self) -> str:
        """Get account ID from metadata."""
        return self.get_metadata('account_id')
    
    @property
    def project_id(self) -> Optional[str]:
        """Get project ID from metadata."""
        return self.get_metadata('project_id')
    
    @project_id.setter
    def project_id(self, value: Optional[str]):
        """Set project ID in metadata."""
        if value:
            self.set_metadata('project_id', value)
    
    @property
    def client_id(self) -> Optional[str]:
        """Get client ID from metadata."""
        return self.get_metadata('client_id')
    
    @client_id.setter  
    def client_id(self, value: Optional[str]):
        """Set client ID in metadata."""
        if value:
            self.set_metadata('client_id', value)
    
    @property
    def invoice_id(self) -> Optional[str]:
        """Get invoice ID from metadata."""
        return self.get_metadata('invoice_id')
    
    @invoice_id.setter
    def invoice_id(self, value: Optional[str]):
        """Set invoice ID in metadata."""
        if value:
            self.set_metadata('invoice_id', value)
    
    @property
    def receipt_path(self) -> Optional[str]:
        """Get receipt path from metadata."""
        return self.get_metadata('receipt_path')
    
    @receipt_path.setter
    def receipt_path(self, value: Optional[str]):
        """Set receipt path in metadata."""
        if value:
            self.set_metadata('receipt_path', value)
    
    @property
    def notes(self) -> Optional[str]:
        """Get notes from metadata."""
        return self.get_metadata('notes')
    
    @notes.setter
    def notes(self, value: Optional[str]):
        """Set notes in metadata."""
        if value:
            self.set_metadata('notes', value)
    
    @property
    def freelancer_transaction_type(self) -> TransactionType:
        """Get original freelancer transaction type."""
        type_str = self.get_metadata('freelancer_transaction_type')
        return TransactionType(type_str) if type_str else TransactionType.EXPENSE
    
    @classmethod
    def create_from_dict(cls, data: Dict) -> 'Transaction':
        """Create transaction from dictionary (for backward compatibility)."""
        # Handle both UUID and string IDs
        if 'id' in data and isinstance(data['id'], UUID):
            data['id'] = data['id']
        elif 'id' in data:
            data['id'] = UUID(str(data['id']))
        
        # Handle enum conversion
        if 'transaction_type' in data and isinstance(data['transaction_type'], str):
            data['transaction_type'] = TransactionType(data['transaction_type'])
        
        if 'category' in data and isinstance(data['category'], str):
            data['category'] = ExpenseCategory(data['category'])
        
        return cls(**data)


class Client(BaseModel):
    """Client model."""

    id: str
    name: str
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    active: bool = True


class Project(BaseModel):
    """Project model."""

    id: str
    name: str
    client_id: str
    start_date: datetime
    end_date: Optional[datetime] = None
    status: str  # e.g., "active", "completed", "on_hold"
    hourly_rate: Optional[float] = None
    fixed_price: Optional[float] = None
    estimated_hours: Optional[float] = None
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class TimeEntry(BaseModel):
    """Time entry model for tracking hours worked on projects."""

    id: UUID = Field(default_factory=uuid4)
    project_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_minutes: Optional[float] = None
    description: str
    billable: bool = True
    tags: List[str] = Field(default_factory=list)

    @validator("duration_minutes", always=True)
    def calculate_duration(cls, v, values):
        """Calculate duration from start and end time if not provided."""
        if v is not None:
            return v
        if (
            "start_time" in values
            and "end_time" in values
            and values["end_time"] is not None
        ):
            delta = values["end_time"] - values["start_time"]
            return delta.total_seconds() / 60
        return None


class Invoice(BaseModel):
    """Invoice model."""

    id: str
    client_id: str
    project_id: Optional[str] = None
    issue_date: datetime
    due_date: datetime
    amount: float
    status: str  # e.g., "draft", "sent", "paid", "overdue"
    payment_date: Optional[datetime] = None
    description: Optional[str] = None
    line_items: List[Dict] = Field(default_factory=list)


class TaxPayment(BaseModel):
    """Tax payment model."""

    id: UUID = Field(default_factory=uuid4)
    date: datetime
    amount: float
    tax_year: int
    quarter: int
    payment_method: str
    confirmation_number: Optional[str] = None
    notes: Optional[str] = None


class TaxRate(BaseModel):
    """Tax rate for a specific income bracket."""

    bracket_min: float
    bracket_max: Optional[float] = None
    rate: float  # Percentage (0-100)
    tax_year: int
    jurisdiction: str = "federal"  # e.g., "federal", "state", "local"


class TaxDeduction(BaseModel):
    """Tax deduction model."""

    id: UUID = Field(default_factory=uuid4)
    name: str
    amount: float
    tax_year: int
    category: str
    description: Optional[str] = None
    receipt_path: Optional[str] = None
