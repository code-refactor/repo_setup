"""Models for the income management system."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator

from personal_finance_tracker.models.common import Transaction


class SmoothingMethod(str, Enum):
    """Income smoothing method enum."""

    MOVING_AVERAGE = "moving_average"
    EXPONENTIAL_SMOOTHING = "exponential_smoothing"
    SEASONAL_ADJUSTMENT = "seasonal_adjustment"
    PERCENTILE_BASED = "percentile_based"
    ROLLING_MEDIAN = "rolling_median"


class SmoothingConfig(BaseModel):
    """Configuration for income smoothing algorithms."""

    method: SmoothingMethod = SmoothingMethod.MOVING_AVERAGE
    window_size: int = 3  # Number of months for moving average
    alpha: float = 0.3  # For exponential smoothing
    seasonal_periods: int = 12  # For seasonal adjustment
    percentile: float = 25.0  # Percentile for percentile-based method
    min_history_months: int = 3  # Minimum months of data required
    target_monthly_income: Optional[float] = None  # Override calculated smoothed income
    emergency_buffer_months: float = 2.0  # Buffer for lean months
    confidence_interval: float = 0.8  # For prediction intervals

    @validator("window_size")
    def validate_window_size(cls, v):
        """Validate window size is positive."""
        if v <= 0:
            raise ValueError("Window size must be positive")
        return v

    @validator("alpha")
    def validate_alpha(cls, v):
        """Validate alpha is between 0 and 1."""
        if v < 0 or v > 1:
            raise ValueError("Alpha must be between 0 and 1")
        return v

    @validator("percentile")
    def validate_percentile(cls, v):
        """Validate percentile is between 0 and 100."""
        if v < 0 or v > 100:
            raise ValueError("Percentile must be between 0 and 100")
        return v

    @validator("emergency_buffer_months")
    def validate_buffer(cls, v):
        """Validate buffer is non-negative."""
        if v < 0:
            raise ValueError("Emergency buffer months must be non-negative")
        return v

    @validator("confidence_interval")
    def validate_confidence(cls, v):
        """Validate confidence interval is between 0 and 1."""
        if v < 0 or v > 1:
            raise ValueError("Confidence interval must be between 0 and 1")
        return v


class RevenueForecast(BaseModel):
    """Revenue forecast model."""

    month: datetime
    expected_income: float
    lower_bound: float
    upper_bound: float
    confidence_interval: float
    sources: Dict[str, float] = Field(default_factory=dict)  # Client/project breakdown
    notes: Optional[str] = None


class SmoothedIncome(BaseModel):
    """Smoothed income calculation result."""

    period_start: datetime
    period_end: datetime
    actual_income: float
    smoothed_income: float
    method: SmoothingMethod
    configuration: SmoothingConfig
    income_deficit: float = 0.0  # Negative when actual < smoothed
    income_surplus: float = 0.0  # Positive when actual > smoothed
    notes: Optional[str] = None
