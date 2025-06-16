"""Migrated income management system using common library."""

import calendar
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union
import time
from decimal import Decimal

import statistics

try:
    import numpy as np
    import pandas as pd
    HAS_NUMPY = True
    HAS_PANDAS = True
except ImportError:
    HAS_NUMPY = False
    HAS_PANDAS = False

# Import common library components
from common.core.engines.analysis_engine import AnalysisEngine
from common.core.engines.time_series_analyzer import TimeSeriesAnalyzer, TimeSeries, DataPoint
from common.core.models.analysis_results import AnalysisResult
from common.core.models.base_transaction import BaseTransaction, TransactionType
from common.core.utils.financial_calculations import FinancialCalculations
from common.core.utils.date_helpers import DateHelpers, PeriodType

# Import original models for backward compatibility
from personal_finance_tracker.income.models import (
    SmoothingConfig,
    SmoothingMethod,
    SmoothedIncome,
    RevenueForecast,
)


class FreelancerIncomeManager(AnalysisEngine):
    """
    Freelancer income management system extending common analysis engine.
    
    Provides sophisticated income smoothing algorithms to normalize variable
    freelance earnings into predictable budget allocations.
    """
    
    def __init__(self, smoothing_config: Optional[SmoothingConfig] = None):
        """Initialize with optional smoothing configuration."""
        super().__init__(enable_caching=True, enable_performance_tracking=True)
        self.config = smoothing_config or SmoothingConfig()
        self.time_series_analyzer = TimeSeriesAnalyzer()
        
        # Set configuration in base class
        self.set_configuration({
            'smoothing_method': self.config.method.value,
            'window_months': self.config.window_months,
            'confidence_threshold': self.config.confidence_threshold,
            'variance_cap': self.config.variance_cap
        })
    
    def analyze(self, transactions: List[BaseTransaction]) -> AnalysisResult:
        """
        Analyze income transactions and provide smoothed income calculations.
        
        Args:
            transactions: List of transactions to analyze
            
        Returns:
            AnalysisResult with smoothed income analysis
        """
        with self.measure_performance("income_analysis"):
            start_time = time.time()
            
            # Filter to income transactions only
            income_transactions = [t for t in transactions if t.is_income()]
            
            if not income_transactions:
                return AnalysisResult(
                    analysis_type="freelancer_income_analysis",
                    calculation_date=datetime.now(),
                    processing_time_ms=0.0,
                    confidence_score=Decimal('0'),
                    metadata={'error': 'No income transactions found'}
                )
            
            # Create time series from transactions
            income_series = self._create_income_time_series(income_transactions)
            
            # Calculate smoothed income
            smoothed_results = self._calculate_smoothed_income(income_series)
            
            # Generate revenue forecast
            forecast = self._generate_revenue_forecast(income_series)
            
            # Calculate summary statistics
            total_income = sum(float(t.amount) for t in income_transactions)
            avg_monthly_income = self._calculate_average_monthly_income(income_transactions)
            income_volatility = self.time_series_analyzer.calculate_volatility(income_series)
            
            processing_time = (time.time() - start_time) * 1000
            
            result = AnalysisResult(
                analysis_type="freelancer_income_analysis",
                calculation_date=datetime.now(),
                processing_time_ms=processing_time,
                confidence_score=Decimal('0.9'),
                metadata={
                    'total_transactions': len(income_transactions),
                    'total_income': total_income,
                    'avg_monthly_income': avg_monthly_income,
                    'income_volatility': float(income_volatility),
                    'smoothed_income': smoothed_results,
                    'revenue_forecast': forecast,
                    'smoothing_method': self.config.method.value,
                    'window_months': self.config.window_months
                }
            )
            
            return result
    
    def smooth_income(self, transactions: List[BaseTransaction], 
                     method: Optional[SmoothingMethod] = None) -> List[SmoothedIncome]:
        """
        Calculate smoothed income using specified or configured method.
        
        Args:
            transactions: Income transactions to smooth
            method: Optional smoothing method override
            
        Returns:
            List of SmoothedIncome objects
        """
        cache_key = self._generate_cache_key(transactions, f"smooth_{method or self.config.method}")
        
        # Check cache first
        if self.is_cached_result_available(cache_key):
            cached_result = self.get_cached_result(cache_key)
            return cached_result
        
        with self.measure_performance("income_smoothing"):
            # Filter income transactions
            income_transactions = [t for t in transactions if t.is_income()]
            
            if not income_transactions:
                return []
            
            # Create time series
            income_series = self._create_income_time_series(income_transactions)
            
            # Calculate smoothed values
            smoothed_results = self._calculate_smoothed_income(income_series, method)
            
            # Cache and return results
            self.set_cached_result(cache_key, smoothed_results, ttl_seconds=3600)
            return smoothed_results
    
    def forecast_revenue(self, transactions: List[BaseTransaction], 
                        months_ahead: int = 6) -> RevenueForecast:
        """
        Generate revenue forecast based on historical income patterns.
        
        Args:
            transactions: Historical income transactions
            months_ahead: Number of months to forecast ahead
            
        Returns:
            RevenueForecast object with projections
        """
        with self.measure_performance("revenue_forecasting"):
            income_transactions = [t for t in transactions if t.is_income()]
            
            if not income_transactions:
                # Return empty forecast
                return RevenueForecast(
                    forecast_date=datetime.now(),
                    periods_ahead=months_ahead,
                    projected_amounts=[],
                    confidence_intervals=[],
                    confidence_level=0.0
                )
            
            # Create time series
            income_series = self._create_income_time_series(income_transactions)
            
            # Generate forecast using time series analyzer
            forecast_series = self.time_series_analyzer.forecast_linear(income_series, months_ahead)
            
            # Convert to RevenueForecast format
            projected_amounts = [float(point.value) for point in forecast_series.data_points]
            
            # Calculate confidence intervals (simplified)
            volatility = float(self.time_series_analyzer.calculate_volatility(income_series))
            confidence_intervals = []
            
            for amount in projected_amounts:
                lower_bound = max(0, amount - (1.96 * volatility))
                upper_bound = amount + (1.96 * volatility)
                confidence_intervals.append((lower_bound, upper_bound))
            
            return RevenueForecast(
                forecast_date=datetime.now(),
                periods_ahead=months_ahead,
                projected_amounts=projected_amounts,
                confidence_intervals=confidence_intervals,
                confidence_level=0.95
            )
    
    def get_income_summary(self, transactions: List[BaseTransaction], 
                          start_date: Optional[datetime] = None,
                          end_date: Optional[datetime] = None) -> Dict[str, Union[float, int]]:
        """
        Generate comprehensive income summary for a date range.
        
        Args:
            transactions: Income transactions to analyze
            start_date: Start date filter (optional)
            end_date: End date filter (optional)
            
        Returns:
            Dictionary with income summary statistics
        """
        # Filter transactions by date
        filtered_transactions = transactions
        if start_date or end_date:
            filtered_transactions = []
            for t in transactions:
                if start_date and t.date < start_date:
                    continue
                if end_date and t.date > end_date:
                    continue
                filtered_transactions.append(t)
        
        income_transactions = [t for t in filtered_transactions if t.is_income()]
        
        if not income_transactions:
            return {
                'total_income': 0.0,
                'transaction_count': 0,
                'avg_transaction_amount': 0.0,
                'min_transaction': 0.0,
                'max_transaction': 0.0,
                'monthly_average': 0.0
            }
        
        amounts = [float(t.amount) for t in income_transactions]
        total_income = sum(amounts)
        
        # Calculate monthly average
        if start_date and end_date:
            months = DateHelpers.get_years_between_dates(start_date, end_date) * 12
            monthly_average = total_income / max(1, months)
        else:
            monthly_average = self._calculate_average_monthly_income(income_transactions)
        
        return {
            'total_income': total_income,
            'transaction_count': len(income_transactions),
            'avg_transaction_amount': total_income / len(income_transactions),
            'min_transaction': min(amounts),
            'max_transaction': max(amounts),
            'monthly_average': monthly_average
        }
    
    def _create_income_time_series(self, transactions: List[BaseTransaction]) -> TimeSeries:
        """Create time series from income transactions."""
        # Sort transactions by date
        sorted_transactions = sorted(transactions, key=lambda t: t.date)
        
        # Group by month and sum amounts
        monthly_data = {}
        for transaction in sorted_transactions:
            month_key = transaction.date.strftime('%Y-%m')
            if month_key not in monthly_data:
                monthly_data[month_key] = Decimal('0')
            monthly_data[month_key] += transaction.amount
        
        # Create time series
        series = TimeSeries("monthly_income")
        for month_str, amount in monthly_data.items():
            month_date = datetime.strptime(month_str, '%Y-%m')
            series.add_point(month_date, amount)
        
        return series
    
    def _calculate_smoothed_income(self, income_series: TimeSeries, 
                                  method: Optional[SmoothingMethod] = None) -> List[SmoothedIncome]:
        """Calculate smoothed income using specified method."""
        smoothing_method = method or self.config.method
        
        if smoothing_method == SmoothingMethod.SIMPLE_MOVING_AVERAGE:
            return self._simple_moving_average(income_series)
        elif smoothing_method == SmoothingMethod.EXPONENTIAL_SMOOTHING:
            return self._exponential_smoothing(income_series)
        elif smoothing_method == SmoothingMethod.SEASONAL_DECOMPOSITION:
            return self._seasonal_decomposition(income_series)
        else:
            # Default to simple moving average
            return self._simple_moving_average(income_series)
    
    def _simple_moving_average(self, income_series: TimeSeries) -> List[SmoothedIncome]:
        """Calculate smoothed income using simple moving average."""
        window = self.config.window_months
        
        # Use common library moving average
        smoothed_series = self.time_series_analyzer.calculate_moving_average(income_series, window)
        
        results = []
        for i, point in enumerate(smoothed_series.data_points):
            # Calculate confidence based on variance within window
            original_points = income_series.data_points[max(0, i):i+window+1]
            if len(original_points) >= 2:
                amounts = [float(p.value) for p in original_points]
                if HAS_NUMPY:
                    variance = np.var(amounts)
                else:
                    mean_val = statistics.mean(amounts)
                    variance = statistics.variance(amounts) if len(amounts) > 1 else 0
                confidence = max(0.1, 1.0 - (variance / (self.config.variance_cap ** 2)))
            else:
                confidence = 0.5
            
            results.append(SmoothedIncome(
                period_start=point.timestamp,
                period_end=point.timestamp + timedelta(days=30),  # Approximate month
                original_amount=float(income_series.data_points[min(i, len(income_series.data_points)-1)].value),
                smoothed_amount=float(point.value),
                confidence_score=confidence,
                method_used=SmoothingMethod.SIMPLE_MOVING_AVERAGE,
                window_size=window
            ))
        
        return results
    
    def _exponential_smoothing(self, income_series: TimeSeries) -> List[SmoothedIncome]:
        """Calculate smoothed income using exponential smoothing."""
        alpha = 0.3  # Smoothing factor
        results = []
        smoothed_value = None
        
        for i, point in enumerate(income_series.data_points):
            current_amount = float(point.value)
            
            if smoothed_value is None:
                smoothed_value = current_amount
            else:
                smoothed_value = alpha * current_amount + (1 - alpha) * smoothed_value
            
            # Calculate confidence based on recent variance
            if i >= 3:
                recent_values = [float(p.value) for p in income_series.data_points[max(0, i-3):i+1]]
                if HAS_NUMPY:
                    variance = np.var(recent_values)
                else:
                    variance = statistics.variance(recent_values) if len(recent_values) > 1 else 0
                confidence = max(0.1, 1.0 - (variance / (self.config.variance_cap ** 2)))
            else:
                confidence = 0.5
            
            results.append(SmoothedIncome(
                period_start=point.timestamp,
                period_end=point.timestamp + timedelta(days=30),
                original_amount=current_amount,
                smoothed_amount=smoothed_value,
                confidence_score=confidence,
                method_used=SmoothingMethod.EXPONENTIAL_SMOOTHING,
                window_size=3
            ))
        
        return results
    
    def _seasonal_decomposition(self, income_series: TimeSeries) -> List[SmoothedIncome]:
        """Calculate smoothed income using seasonal decomposition."""
        # For now, fall back to moving average if we don't have enough data for seasonal analysis
        if len(income_series) < 12:  # Need at least a year of data
            return self._simple_moving_average(income_series)
        
        # Convert to pandas series for seasonal decomposition
        dates = [point.timestamp for point in income_series.data_points]
        values = [float(point.value) for point in income_series.data_points]
        
        if not HAS_PANDAS:
            # Fall back to simple moving average if pandas not available
            return self._simple_moving_average(income_series)
        
        # Create pandas series with monthly frequency
        ts = pd.Series(values, index=pd.DatetimeIndex(dates, freq='M'))
        
        try:
            from statsmodels.tsa.seasonal import seasonal_decompose
            decomposition = seasonal_decompose(ts, model='additive', period=12)
            trend = decomposition.trend.fillna(method='bfill').fillna(method='ffill')
            
            results = []
            for i, (date, smoothed_value) in enumerate(trend.items()):
                original_value = values[i] if i < len(values) else smoothed_value
                
                results.append(SmoothedIncome(
                    period_start=date,
                    period_end=date + timedelta(days=30),
                    original_amount=original_value,
                    smoothed_amount=smoothed_value,
                    confidence_score=0.8,
                    method_used=SmoothingMethod.SEASONAL_DECOMPOSITION,
                    window_size=12
                ))
            
            return results
            
        except ImportError:
            # Fall back to simple moving average if statsmodels not available
            return self._simple_moving_average(income_series)
    
    def _generate_revenue_forecast(self, income_series: TimeSeries) -> Dict:
        """Generate revenue forecast data."""
        forecast_series = self.time_series_analyzer.forecast_linear(income_series, 6)
        
        return {
            'forecast_months': 6,
            'projected_amounts': [float(p.value) for p in forecast_series.data_points],
            'confidence_level': 0.8,
            'method': 'linear_trend'
        }
    
    def _calculate_average_monthly_income(self, transactions: List[BaseTransaction]) -> float:
        """Calculate average monthly income from transactions."""
        if not transactions:
            return 0.0
        
        # Sort by date
        sorted_transactions = sorted(transactions, key=lambda t: t.date)
        
        # Calculate total income and date range
        total_income = sum(float(t.amount) for t in sorted_transactions)
        start_date = sorted_transactions[0].date
        end_date = sorted_transactions[-1].date
        
        # Calculate months between start and end
        months = DateHelpers.get_years_between_dates(start_date, end_date) * 12
        months = max(1, months)  # At least 1 month
        
        return total_income / months


# Backward compatibility wrapper
class IncomeManager(FreelancerIncomeManager):
    """Backward compatibility wrapper for the original IncomeManager."""
    
    def record_income(self, transactions: List[BaseTransaction], 
                     force_recalculation: bool = False) -> None:
        """Record income transactions (for backward compatibility)."""
        if force_recalculation:
            self.clear_cache()
        
        # Analyze transactions to update internal state
        self.analyze(transactions)