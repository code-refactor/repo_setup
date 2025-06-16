from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import List, Tuple, Optional
import statistics


class PeriodType(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class TrendDirection(Enum):
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"


@dataclass
class TrendResult:
    """Result of trend analysis."""
    direction: TrendDirection
    slope: Decimal
    correlation: Decimal
    confidence: Decimal
    start_value: Decimal
    end_value: Decimal


class FinancialMetrics:
    """Common financial calculations used across persona implementations."""
    
    @staticmethod
    def calculate_percentage_change(old_value: Decimal, new_value: Decimal) -> Decimal:
        """Calculate percentage change between two values."""
        if old_value == 0:
            return Decimal('0') if new_value == 0 else Decimal('100')
        
        change = ((new_value - old_value) / abs(old_value)) * Decimal('100')
        return change.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_weighted_average(values: List[Tuple[Decimal, Decimal]]) -> Decimal:
        """Calculate weighted average from list of (value, weight) tuples."""
        if not values:
            return Decimal('0')
        
        total_weighted_value = sum(value * weight for value, weight in values)
        total_weight = sum(weight for _, weight in values)
        
        if total_weight == 0:
            return Decimal('0')
        
        return (total_weighted_value / total_weight).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_trend(series: List[Tuple[datetime, Decimal]]) -> TrendResult:
        """Calculate trend from time series data."""
        if len(series) < 2:
            return TrendResult(
                direction=TrendDirection.STABLE,
                slope=Decimal('0'),
                correlation=Decimal('0'),
                confidence=Decimal('0'),
                start_value=series[0][1] if series else Decimal('0'),
                end_value=series[0][1] if series else Decimal('0')
            )
        
        # Sort by date
        sorted_series = sorted(series, key=lambda x: x[0])
        
        # Convert to numeric values for calculation
        x_values = list(range(len(sorted_series)))
        y_values = [float(value) for _, value in sorted_series]
        
        # Calculate linear regression
        n = len(x_values)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_x2 = sum(x * x for x in x_values)
        
        # Calculate slope
        denominator = n * sum_x2 - sum_x * sum_x
        if denominator == 0:
            slope = Decimal('0')
        else:
            slope = Decimal(str((n * sum_xy - sum_x * sum_y) / denominator))
        
        # Calculate correlation coefficient
        try:
            correlation = Decimal(str(statistics.correlation(x_values, y_values)))
        except (statistics.StatisticsError, ValueError):
            correlation = Decimal('0')
        
        # Determine trend direction
        if abs(slope) < Decimal('0.01'):
            direction = TrendDirection.STABLE
        elif slope > 0:
            direction = TrendDirection.INCREASING
        else:
            direction = TrendDirection.DECREASING
        
        # Calculate confidence based on correlation strength
        confidence = abs(correlation) * Decimal('100')
        
        return TrendResult(
            direction=direction,
            slope=slope.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP),
            correlation=correlation.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP),
            confidence=confidence.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            start_value=sorted_series[0][1],
            end_value=sorted_series[-1][1]
        )
    
    @staticmethod
    def calculate_compound_growth(principal: Decimal, rate: Decimal, periods: int) -> Decimal:
        """Calculate compound growth."""
        if periods == 0:
            return principal
        
        growth_factor = (Decimal('1') + rate) ** periods
        return (principal * growth_factor).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_present_value(future_value: Decimal, rate: Decimal, periods: int) -> Decimal:
        """Calculate present value."""
        if periods == 0:
            return future_value
        
        discount_factor = (Decimal('1') + rate) ** periods
        return (future_value / discount_factor).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_roi(gain: Decimal, cost: Decimal) -> Decimal:
        """Calculate return on investment as percentage."""
        if cost == 0:
            return Decimal('0')
        
        roi = ((gain - cost) / cost) * Decimal('100')
        return roi.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def normalize_currency(amount: Decimal, precision: int = 2) -> Decimal:
        """Normalize currency amount to specified precision."""
        quantize_str = '0.' + '0' * precision
        return amount.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_standard_deviation(values: List[Decimal]) -> Decimal:
        """Calculate standard deviation of decimal values."""
        if len(values) < 2:
            return Decimal('0')
        
        float_values = [float(v) for v in values]
        std_dev = statistics.stdev(float_values)
        return Decimal(str(std_dev)).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_moving_average(values: List[Decimal], window: int) -> List[Decimal]:
        """Calculate moving average with specified window size."""
        if window <= 0 or len(values) < window:
            return values.copy()
        
        result = []
        for i in range(len(values) - window + 1):
            window_values = values[i:i + window]
            avg = sum(window_values) / len(window_values)
            result.append(avg.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        
        return result