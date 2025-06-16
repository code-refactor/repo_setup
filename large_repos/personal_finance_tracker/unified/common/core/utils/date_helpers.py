from datetime import datetime, timedelta, date
from typing import List, Tuple, Dict, Optional
import calendar
from enum import Enum

from ..models.financial_metrics import PeriodType


class QuarterType(Enum):
    Q1 = 1
    Q2 = 2
    Q3 = 3
    Q4 = 4


class DateHelpers:
    """Date/time processing utilities for financial analysis."""
    
    @staticmethod
    def get_quarter_dates(target_date: datetime) -> Tuple[datetime, datetime]:
        """Get start and end dates for the quarter containing the target date."""
        year = target_date.year
        month = target_date.month
        
        # Determine quarter
        if month <= 3:
            quarter_start = datetime(year, 1, 1)
            quarter_end = datetime(year, 3, 31, 23, 59, 59, 999999)
        elif month <= 6:
            quarter_start = datetime(year, 4, 1)
            quarter_end = datetime(year, 6, 30, 23, 59, 59, 999999)
        elif month <= 9:
            quarter_start = datetime(year, 7, 1)
            quarter_end = datetime(year, 9, 30, 23, 59, 59, 999999)
        else:
            quarter_start = datetime(year, 10, 1)
            quarter_end = datetime(year, 12, 31, 23, 59, 59, 999999)
        
        return quarter_start, quarter_end
    
    @staticmethod
    def get_quarter_number(target_date: datetime) -> QuarterType:
        """Get quarter number for a given date."""
        month = target_date.month
        if month <= 3:
            return QuarterType.Q1
        elif month <= 6:
            return QuarterType.Q2
        elif month <= 9:
            return QuarterType.Q3
        else:
            return QuarterType.Q4
    
    @staticmethod
    def get_tax_year_dates(target_date: datetime, tax_year_start_month: int = 1) -> Tuple[datetime, datetime]:
        """
        Get start and end dates for the tax year containing the target date.
        
        Args:
            target_date: Date to find tax year for
            tax_year_start_month: Month tax year starts (1 for Jan-Dec, 4 for Apr-Mar, etc.)
        """
        year = target_date.year
        
        # Determine which tax year we're in
        if target_date.month >= tax_year_start_month:
            # Same calendar year
            tax_year_start = datetime(year, tax_year_start_month, 1)
            if tax_year_start_month == 1:
                tax_year_end = datetime(year, 12, 31, 23, 59, 59, 999999)
            else:
                # Tax year spans calendar years
                next_year = year + 1
                end_month = tax_year_start_month - 1
                last_day = calendar.monthrange(next_year, end_month)[1]
                tax_year_end = datetime(next_year, end_month, last_day, 23, 59, 59, 999999)
        else:
            # Previous tax year
            prev_year = year - 1
            tax_year_start = datetime(prev_year, tax_year_start_month, 1)
            end_month = tax_year_start_month - 1
            last_day = calendar.monthrange(year, end_month)[1]
            tax_year_end = datetime(year, end_month, last_day, 23, 59, 59, 999999)
        
        return tax_year_start, tax_year_end
    
    @staticmethod
    def get_business_days_between(start_date: datetime, end_date: datetime) -> int:
        """Calculate number of business days between two dates (excluding weekends)."""
        if start_date > end_date:
            return 0
        
        business_days = 0
        current_date = start_date.date()
        end_date_only = end_date.date()
        
        while current_date <= end_date_only:
            # Monday = 0, Sunday = 6
            if current_date.weekday() < 5:  # Monday to Friday
                business_days += 1
            current_date += timedelta(days=1)
        
        return business_days
    
    @staticmethod
    def get_working_days_in_month(year: int, month: int, 
                                 exclude_holidays: Optional[List[date]] = None) -> int:
        """Get number of working days in a specific month."""
        exclude_holidays = exclude_holidays or []
        
        # Get first and last day of month
        first_day = date(year, month, 1)
        last_day = date(year, month, calendar.monthrange(year, month)[1])
        
        working_days = 0
        current_date = first_day
        
        while current_date <= last_day:
            # Check if it's a weekday and not a holiday
            if current_date.weekday() < 5 and current_date not in exclude_holidays:
                working_days += 1
            current_date += timedelta(days=1)
        
        return working_days
    
    @staticmethod
    def group_by_period(dates: List[datetime], period: PeriodType) -> Dict[str, List[datetime]]:
        """Group dates by specified period."""
        groups = {}
        
        for date_obj in dates:
            if period == PeriodType.DAILY:
                key = date_obj.strftime('%Y-%m-%d')
            elif period == PeriodType.WEEKLY:
                # Get start of week (Monday)
                start_of_week = date_obj - timedelta(days=date_obj.weekday())
                key = start_of_week.strftime('%Y-%W')
            elif period == PeriodType.MONTHLY:
                key = date_obj.strftime('%Y-%m')
            elif period == PeriodType.QUARTERLY:
                quarter = DateHelpers.get_quarter_number(date_obj)
                key = f"{date_obj.year}-{quarter.name}"
            elif period == PeriodType.YEARLY:
                key = date_obj.strftime('%Y')
            else:
                key = date_obj.isoformat()
            
            if key not in groups:
                groups[key] = []
            groups[key].append(date_obj)
        
        return groups
    
    @staticmethod
    def get_period_boundaries(period: PeriodType, reference_date: datetime) -> Tuple[datetime, datetime]:
        """Get start and end boundaries for a period containing the reference date."""
        if period == PeriodType.DAILY:
            start = reference_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end = reference_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        elif period == PeriodType.WEEKLY:
            # Start of week (Monday)
            days_since_monday = reference_date.weekday()
            start = (reference_date - timedelta(days=days_since_monday)).replace(
                hour=0, minute=0, second=0, microsecond=0)
            end = (start + timedelta(days=6)).replace(
                hour=23, minute=59, second=59, microsecond=999999)
        
        elif period == PeriodType.MONTHLY:
            start = reference_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            last_day = calendar.monthrange(reference_date.year, reference_date.month)[1]
            end = reference_date.replace(
                day=last_day, hour=23, minute=59, second=59, microsecond=999999)
        
        elif period == PeriodType.QUARTERLY:
            start, end = DateHelpers.get_quarter_dates(reference_date)
        
        elif period == PeriodType.YEARLY:
            start = reference_date.replace(
                month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end = reference_date.replace(
                month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        
        else:
            # Default to daily
            start = reference_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end = reference_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        return start, end
    
    @staticmethod
    def get_next_business_day(target_date: datetime) -> datetime:
        """Get the next business day after the target date."""
        next_day = target_date + timedelta(days=1)
        
        # Skip weekends
        while next_day.weekday() >= 5:  # Saturday = 5, Sunday = 6
            next_day += timedelta(days=1)
        
        return next_day
    
    @staticmethod
    def get_previous_business_day(target_date: datetime) -> datetime:
        """Get the previous business day before the target date."""
        prev_day = target_date - timedelta(days=1)
        
        # Skip weekends
        while prev_day.weekday() >= 5:  # Saturday = 5, Sunday = 6
            prev_day -= timedelta(days=1)
        
        return prev_day
    
    @staticmethod
    def is_business_day(target_date: datetime) -> bool:
        """Check if date is a business day (Monday-Friday)."""
        return target_date.weekday() < 5
    
    @staticmethod
    def get_age_in_years(birth_date: datetime, reference_date: Optional[datetime] = None) -> int:
        """Calculate age in years from birth date."""
        if reference_date is None:
            reference_date = datetime.now()
        
        age = reference_date.year - birth_date.year
        
        # Adjust if birthday hasn't occurred this year
        if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
            age -= 1
        
        return max(0, age)
    
    @staticmethod
    def get_years_between_dates(start_date: datetime, end_date: datetime) -> float:
        """Calculate fractional years between two dates."""
        if start_date > end_date:
            return 0.0
        
        # Calculate total days
        total_days = (end_date - start_date).days
        
        # Average days per year (accounting for leap years)
        avg_days_per_year = 365.25
        
        return total_days / avg_days_per_year
    
    @staticmethod
    def format_period_display(period: PeriodType, reference_date: datetime) -> str:
        """Format period for display purposes."""
        if period == PeriodType.DAILY:
            return reference_date.strftime('%Y-%m-%d')
        elif period == PeriodType.WEEKLY:
            start, end = DateHelpers.get_period_boundaries(period, reference_date)
            return f"Week of {start.strftime('%Y-%m-%d')}"
        elif period == PeriodType.MONTHLY:
            return reference_date.strftime('%Y-%m (%B %Y)')
        elif period == PeriodType.QUARTERLY:
            quarter = DateHelpers.get_quarter_number(reference_date)
            return f"{reference_date.year} {quarter.name}"
        elif period == PeriodType.YEARLY:
            return reference_date.strftime('%Y')
        else:
            return reference_date.isoformat()
    
    @staticmethod
    def get_quarterly_dates_for_year(year: int) -> Dict[QuarterType, Tuple[datetime, datetime]]:
        """Get all quarterly date ranges for a specific year."""
        return {
            QuarterType.Q1: (datetime(year, 1, 1), datetime(year, 3, 31, 23, 59, 59, 999999)),
            QuarterType.Q2: (datetime(year, 4, 1), datetime(year, 6, 30, 23, 59, 59, 999999)),
            QuarterType.Q3: (datetime(year, 7, 1), datetime(year, 9, 30, 23, 59, 59, 999999)),
            QuarterType.Q4: (datetime(year, 10, 1), datetime(year, 12, 31, 23, 59, 59, 999999))
        }