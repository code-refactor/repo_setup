"""Project profitability analysis models."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator

from personal_finance_tracker.models.common import Project, TimeEntry, Transaction


class ProjectMetricType(str, Enum):
    """Types of project profitability metrics."""

    HOURLY_RATE = "hourly_rate"
    TOTAL_PROFIT = "total_profit"
    PROFIT_MARGIN = "profit_margin"
    ROI = "roi"  # Return on investment


class ProfitabilityMetric(BaseModel):
    """Profitability metric for a project."""

    project_id: str
    metric_type: ProjectMetricType
    value: float
    calculation_date: datetime = Field(default_factory=datetime.now)
    description: Optional[str] = None


class ProjectProfitability(BaseModel):
    """Project profitability analysis result."""

    project_id: str
    project_name: str
    client_id: str
    start_date: datetime
    end_date: Optional[datetime] = None
    total_hours: float
    total_revenue: float
    total_expenses: float
    total_profit: float
    effective_hourly_rate: float
    profit_margin: float  # Percentage
    roi: float  # Return on investment
    is_completed: bool
    calculation_date: datetime = Field(default_factory=datetime.now)
    metrics: List[ProfitabilityMetric] = Field(default_factory=list)

    @validator("effective_hourly_rate", "profit_margin", "roi", pre=True, always=True)
    def validate_rates(cls, v, values):
        """Ensure rates are calculated correctly."""
        if v is not None:
            return v

        # If we have all required values, calculate the field
        if (
            "total_hours" in values
            and "total_revenue" in values
            and "total_expenses" in values
        ):
            hours = values["total_hours"]
            revenue = values["total_revenue"]
            expenses = values["total_expenses"]

            if values["current_field_name"] == "effective_hourly_rate":
                return revenue / max(hours, 0.01)  # Avoid division by zero

            if values["current_field_name"] == "profit_margin":
                return 100 * (revenue - expenses) / max(revenue, 0.01)

            if values["current_field_name"] == "roi":
                return (revenue - expenses) / max(expenses, 0.01)

        return 0.0


class ClientProfitability(BaseModel):
    """Client profitability analysis result."""

    client_id: str
    client_name: str
    number_of_projects: int
    total_hours: float
    total_revenue: float
    total_expenses: float
    total_profit: float
    average_hourly_rate: float
    average_profit_margin: float
    average_invoice_payment_days: Optional[float] = None
    projects: List[ProjectProfitability] = Field(default_factory=list)
    calculation_date: datetime = Field(default_factory=datetime.now)


class TrendPoint(BaseModel):
    """Point in a trend analysis."""

    date: datetime
    value: float


class TrendAnalysis(BaseModel):
    """Trend analysis for project profitability over time."""

    metric_type: ProjectMetricType
    project_id: Optional[str] = None
    client_id: Optional[str] = None
    period: str  # "weekly", "monthly", "quarterly", "yearly"
    start_date: datetime
    end_date: datetime
    data_points: List[TrendPoint] = Field(default_factory=list)
    calculation_date: datetime = Field(default_factory=datetime.now)
    description: Optional[str] = None
