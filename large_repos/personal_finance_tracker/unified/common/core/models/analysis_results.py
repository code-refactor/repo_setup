from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Any


@dataclass
class AnalysisResult:
    """Base structure for analysis outputs across all implementations."""
    
    analysis_type: str
    calculation_date: datetime
    processing_time_ms: float
    confidence_score: Optional[Decimal] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Ensure confidence_score is Decimal if provided."""
        if self.confidence_score is not None and not isinstance(self.confidence_score, Decimal):
            self.confidence_score = Decimal(str(self.confidence_score))
    
    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the result."""
        self.metadata[key] = value
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value by key."""
        return self.metadata.get(key, default)
    
    def is_confident(self, threshold: Decimal = Decimal('0.8')) -> bool:
        """Check if result meets confidence threshold."""
        if self.confidence_score is None:
            return True  # Assume confident if no score provided
        return self.confidence_score >= threshold


@dataclass
class CategoryResult:
    """Result of categorization operations."""
    
    category: str
    confidence_score: Decimal
    matched_rules: List[str] = field(default_factory=list)
    alternative_categories: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Ensure confidence_score is Decimal."""
        if not isinstance(self.confidence_score, Decimal):
            self.confidence_score = Decimal(str(self.confidence_score))
    
    def add_alternative(self, category: str, confidence: Decimal, reason: str = "") -> None:
        """Add an alternative category suggestion."""
        self.alternative_categories.append({
            'category': category,
            'confidence': confidence,
            'reason': reason
        })
    
    def is_confident(self, threshold: Decimal = Decimal('0.8')) -> bool:
        """Check if categorization meets confidence threshold."""
        return self.confidence_score >= threshold
    
    def get_best_alternative(self) -> Optional[Dict[str, Any]]:
        """Get the highest confidence alternative category."""
        if not self.alternative_categories:
            return None
        return max(self.alternative_categories, key=lambda x: x['confidence'])


@dataclass
class PerformanceMetrics:
    """Performance metrics for operations."""
    
    operation_name: str
    execution_time_ms: float
    memory_usage_mb: Optional[float] = None
    items_processed: Optional[int] = None
    cache_hit_rate: Optional[Decimal] = None
    throughput_per_second: Optional[Decimal] = None
    
    def __post_init__(self):
        """Calculate derived metrics."""
        if self.items_processed is not None and self.execution_time_ms > 0:
            items_per_second = (self.items_processed / self.execution_time_ms) * 1000
            self.throughput_per_second = Decimal(str(items_per_second)).quantize(Decimal('0.01'))
        
        if self.cache_hit_rate is not None and not isinstance(self.cache_hit_rate, Decimal):
            self.cache_hit_rate = Decimal(str(self.cache_hit_rate))
    
    def is_performant(self, max_time_ms: float) -> bool:
        """Check if operation meets performance threshold."""
        return self.execution_time_ms <= max_time_ms
    
    def get_items_per_second(self) -> Decimal:
        """Get throughput in items per second."""
        return self.throughput_per_second or Decimal('0')


@dataclass
class SummaryReport:
    """Summary report structure."""
    
    report_type: str
    generated_at: datetime
    period_start: datetime
    period_end: datetime
    summary_data: Dict[str, Any] = field(default_factory=dict)
    detailed_data: Dict[str, Any] = field(default_factory=dict)
    charts_data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_summary_item(self, key: str, value: Any) -> None:
        """Add item to summary data."""
        self.summary_data[key] = value
    
    def add_detailed_item(self, key: str, value: Any) -> None:
        """Add item to detailed data."""
        self.detailed_data[key] = value
    
    def add_chart_data(self, key: str, value: Any) -> None:
        """Add chart data."""
        self.charts_data[key] = value
    
    def get_summary_value(self, key: str, default: Any = None) -> Any:
        """Get summary data value."""
        return self.summary_data.get(key, default)


@dataclass
class ValidationResult:
    """Result of data validation."""
    
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    validated_items: int = 0
    
    def add_error(self, message: str) -> None:
        """Add validation error."""
        self.errors.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str) -> None:
        """Add validation warning."""
        self.warnings.append(message)
    
    def has_errors(self) -> bool:
        """Check if validation has errors."""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """Check if validation has warnings."""
        return len(self.warnings) > 0