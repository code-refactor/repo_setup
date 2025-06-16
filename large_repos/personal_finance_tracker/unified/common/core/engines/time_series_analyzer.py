from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import statistics

from ..models.financial_metrics import PeriodType, TrendDirection, TrendResult, FinancialMetrics


@dataclass
class DataPoint:
    """Single data point in a time series."""
    timestamp: datetime
    value: Decimal
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not isinstance(self.value, Decimal):
            self.value = Decimal(str(self.value))


@dataclass
class TimeSeries:
    """Time series data structure."""
    name: str
    data_points: List[DataPoint] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_point(self, timestamp: datetime, value: Decimal, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a data point to the series."""
        point = DataPoint(timestamp, value, metadata or {})
        self.data_points.append(point)
        # Keep sorted by timestamp
        self.data_points.sort(key=lambda p: p.timestamp)
    
    def get_values(self) -> List[Decimal]:
        """Get all values in the series."""
        return [point.value for point in self.data_points]
    
    def get_timestamps(self) -> List[datetime]:
        """Get all timestamps in the series."""
        return [point.timestamp for point in self.data_points]
    
    def get_date_range(self) -> Tuple[datetime, datetime]:
        """Get the date range of the series."""
        if not self.data_points:
            now = datetime.now()
            return now, now
        
        timestamps = self.get_timestamps()
        return min(timestamps), max(timestamps)
    
    def filter_by_date_range(self, start_date: datetime, end_date: datetime) -> 'TimeSeries':
        """Filter series by date range."""
        filtered_points = [
            point for point in self.data_points
            if start_date <= point.timestamp <= end_date
        ]
        
        return TimeSeries(
            name=f"{self.name}_filtered",
            data_points=filtered_points,
            metadata=self.metadata.copy()
        )
    
    def resample(self, period: PeriodType) -> 'TimeSeries':
        """Resample the series to a different period."""
        if not self.data_points:
            return TimeSeries(f"{self.name}_resampled")
        
        grouped_data = self._group_by_period(period)
        resampled_points = []
        
        for period_key, points in grouped_data.items():
            if points:
                # Use average value for the period
                avg_value = sum(p.value for p in points) / len(points)
                # Use the first timestamp of the period as representative
                resampled_points.append(DataPoint(
                    timestamp=points[0].timestamp,
                    value=avg_value,
                    metadata={'original_count': len(points)}
                ))
        
        return TimeSeries(
            name=f"{self.name}_resampled_{period.value}",
            data_points=resampled_points,
            metadata=self.metadata.copy()
        )
    
    def _group_by_period(self, period: PeriodType) -> Dict[str, List[DataPoint]]:
        """Group data points by period."""
        groups = {}
        
        for point in self.data_points:
            if period == PeriodType.DAILY:
                key = point.timestamp.strftime('%Y-%m-%d')
            elif period == PeriodType.WEEKLY:
                # Get start of week (Monday)
                start_of_week = point.timestamp - timedelta(days=point.timestamp.weekday())
                key = start_of_week.strftime('%Y-%W')
            elif period == PeriodType.MONTHLY:
                key = point.timestamp.strftime('%Y-%m')
            elif period == PeriodType.QUARTERLY:
                quarter = (point.timestamp.month - 1) // 3 + 1
                key = f"{point.timestamp.year}-Q{quarter}"
            elif period == PeriodType.YEARLY:
                key = point.timestamp.strftime('%Y')
            else:
                key = point.timestamp.isoformat()
            
            if key not in groups:
                groups[key] = []
            groups[key].append(point)
        
        return groups
    
    def __len__(self) -> int:
        return len(self.data_points)
    
    def __iter__(self):
        return iter(self.data_points)


@dataclass
class TrendSegment:
    """Segment of a trend in time series."""
    start_date: datetime
    end_date: datetime
    trend_result: TrendResult
    data_points: List[DataPoint] = field(default_factory=list)


class TimeSeriesAnalyzer:
    """Time-series processing framework for financial data."""
    
    def __init__(self):
        self.series_cache: Dict[str, TimeSeries] = {}
    
    def create_series(self, name: str, data: List[Tuple[datetime, Decimal]]) -> TimeSeries:
        """Create a time series from date-value pairs."""
        series = TimeSeries(name)
        for timestamp, value in data:
            series.add_point(timestamp, value)
        return series
    
    def calculate_moving_average(self, series: TimeSeries, window: int) -> TimeSeries:
        """Calculate moving average with specified window size."""
        if window <= 0 or len(series) < window:
            return series
        
        values = series.get_values()
        moving_averages = FinancialMetrics.calculate_moving_average(values, window)
        
        # Create new series with moving averages
        ma_series = TimeSeries(f"{series.name}_ma_{window}")
        
        # Start from the window-th point to have enough data
        start_index = window - 1
        for i, ma_value in enumerate(moving_averages):
            original_point = series.data_points[start_index + i]
            ma_series.add_point(
                original_point.timestamp,
                ma_value,
                {'window': window, 'original_value': original_point.value}
            )
        
        return ma_series
    
    def detect_trends(self, series: TimeSeries, min_segment_length: int = 5) -> List[TrendSegment]:
        """Detect trend segments in the time series."""
        if len(series) < min_segment_length:
            return []
        
        segments = []
        current_segment_start = 0
        
        while current_segment_start < len(series.data_points) - min_segment_length:
            # Find the longest segment with consistent trend
            best_segment = None
            best_length = min_segment_length
            
            for end_idx in range(current_segment_start + min_segment_length, len(series.data_points) + 1):
                segment_points = series.data_points[current_segment_start:end_idx]
                segment_data = [(p.timestamp, p.value) for p in segment_points]
                
                trend_result = FinancialMetrics.calculate_trend(segment_data)
                
                # Check if trend is significant (good correlation)
                if trend_result.correlation >= Decimal('0.7'):
                    if end_idx - current_segment_start > best_length:
                        best_segment = TrendSegment(
                            start_date=segment_points[0].timestamp,
                            end_date=segment_points[-1].timestamp,
                            trend_result=trend_result,
                            data_points=segment_points.copy()
                        )
                        best_length = end_idx - current_segment_start
                else:
                    # Trend broke, use the best segment found so far
                    break
            
            if best_segment:
                segments.append(best_segment)
                current_segment_start += best_length
            else:
                current_segment_start += 1
        
        return segments
    
    def aggregate_by_period(self, series: TimeSeries, period: PeriodType) -> Dict[str, Decimal]:
        """Aggregate time series by period."""
        if not series.data_points:
            return {}
        
        grouped_data = series._group_by_period(period)
        aggregated = {}
        
        for period_key, points in grouped_data.items():
            if points:
                total_value = sum(p.value for p in points)
                aggregated[period_key] = FinancialMetrics.normalize_currency(total_value)
        
        return aggregated
    
    def calculate_volatility(self, series: TimeSeries) -> Decimal:
        """Calculate volatility (standard deviation) of the series."""
        if len(series) < 2:
            return Decimal('0')
        
        values = series.get_values()
        return FinancialMetrics.calculate_standard_deviation(values)
    
    def calculate_correlation(self, series1: TimeSeries, series2: TimeSeries) -> Decimal:
        """Calculate correlation between two time series."""
        if len(series1) != len(series2) or len(series1) < 2:
            return Decimal('0')
        
        values1 = [float(v) for v in series1.get_values()]
        values2 = [float(v) for v in series2.get_values()]
        
        try:
            correlation = statistics.correlation(values1, values2)
            return Decimal(str(correlation)).quantize(Decimal('0.0001'))
        except (statistics.StatisticsError, ValueError):
            return Decimal('0')
    
    def find_outliers(self, series: TimeSeries, threshold_std: Decimal = Decimal('2.0')) -> List[DataPoint]:
        """Find outliers in the series using standard deviation threshold."""
        if len(series) < 3:
            return []
        
        values = series.get_values()
        mean_value = sum(values) / len(values)
        std_dev = FinancialMetrics.calculate_standard_deviation(values)
        
        if std_dev == 0:
            return []
        
        outliers = []
        for point in series.data_points:
            deviation = abs(point.value - mean_value)
            if deviation > threshold_std * std_dev:
                outliers.append(point)
        
        return outliers
    
    def calculate_growth_rate(self, series: TimeSeries) -> Decimal:
        """Calculate overall growth rate of the series."""
        if len(series) < 2:
            return Decimal('0')
        
        start_value = series.data_points[0].value
        end_value = series.data_points[-1].value
        
        return FinancialMetrics.calculate_percentage_change(start_value, end_value)
    
    def forecast_linear(self, series: TimeSeries, periods_ahead: int) -> TimeSeries:
        """Simple linear forecast based on trend."""
        if len(series) < 2 or periods_ahead <= 0:
            return TimeSeries(f"{series.name}_forecast")
        
        # Calculate trend
        data_pairs = [(p.timestamp, p.value) for p in series.data_points]
        trend_result = FinancialMetrics.calculate_trend(data_pairs)
        
        # Generate forecast points
        forecast_series = TimeSeries(f"{series.name}_forecast")
        last_point = series.data_points[-1]
        
        # Estimate time interval between points
        if len(series) >= 2:
            time_diff = (series.data_points[-1].timestamp - series.data_points[-2].timestamp)
        else:
            time_diff = timedelta(days=1)  # Default to daily
        
        for i in range(1, periods_ahead + 1):
            forecast_timestamp = last_point.timestamp + (time_diff * i)
            forecast_value = last_point.value + (trend_result.slope * i)
            
            forecast_series.add_point(
                forecast_timestamp,
                forecast_value,
                {
                    'forecast': True,
                    'confidence': float(trend_result.confidence),
                    'periods_ahead': i
                }
            )
        
        return forecast_series
    
    def get_summary_statistics(self, series: TimeSeries) -> Dict[str, Any]:
        """Get comprehensive summary statistics for the series."""
        if not series.data_points:
            return {}
        
        values = series.get_values()
        timestamps = series.get_timestamps()
        
        summary = {
            'count': len(values),
            'min_value': min(values),
            'max_value': max(values),
            'mean_value': sum(values) / len(values),
            'total_value': sum(values),
            'start_date': min(timestamps),
            'end_date': max(timestamps),
            'date_range_days': (max(timestamps) - min(timestamps)).days,
            'volatility': self.calculate_volatility(series),
            'growth_rate': self.calculate_growth_rate(series)
        }
        
        # Add median and percentiles if enough data
        if len(values) >= 3:
            float_values = [float(v) for v in values]
            summary.update({
                'median_value': Decimal(str(statistics.median(float_values))),
                'percentile_25': Decimal(str(statistics.quantiles(float_values, n=4)[0])),
                'percentile_75': Decimal(str(statistics.quantiles(float_values, n=4)[2]))
            })
        
        return summary
    
    def cache_series(self, series: TimeSeries) -> None:
        """Cache a time series for reuse."""
        self.series_cache[series.name] = series
    
    def get_cached_series(self, name: str) -> Optional[TimeSeries]:
        """Get a cached time series."""
        return self.series_cache.get(name)
    
    def clear_cache(self) -> None:
        """Clear the series cache."""
        self.series_cache.clear()