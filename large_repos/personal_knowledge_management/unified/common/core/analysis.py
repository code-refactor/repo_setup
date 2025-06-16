"""
Analysis framework and utilities for the unified personal knowledge management library.
"""

from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from statistics import mean, median, mode, stdev
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, Union

from .models import BaseKnowledgeNode
from .storage import BaseStorage

T = TypeVar('T', bound=BaseKnowledgeNode)


class BaseAnalyzer(ABC):
    """Base class for data analyzers."""
    
    def __init__(self, storage: BaseStorage):
        self.storage = storage
    
    @abstractmethod
    def analyze(self, data: List[T], **kwargs) -> Dict[str, Any]:
        """Perform analysis on data."""
        pass
    
    def filter_data(self, data: List[T], filters: Dict[str, Any]) -> List[T]:
        """Common filtering logic."""
        filtered_data = []
        for item in data:
            match = True
            for key, value in filters.items():
                if not hasattr(item, key):
                    match = False
                    break
                
                item_value = getattr(item, key)
                if callable(value):
                    # Custom filter function
                    if not value(item_value):
                        match = False
                        break
                elif isinstance(value, (list, tuple)):
                    # Value in list
                    if item_value not in value:
                        match = False
                        break
                elif isinstance(value, str) and hasattr(item_value, 'lower'):
                    # String contains match
                    if value.lower() not in str(item_value).lower():
                        match = False
                        break
                elif item_value != value:
                    match = False
                    break
            
            if match:
                filtered_data.append(item)
        
        return filtered_data
    
    def calculate_statistics(self, values: List[Union[int, float]]) -> Dict[str, float]:
        """Calculate common statistical measures."""
        if not values:
            return {}
        
        stats = {
            'count': len(values),
            'min': min(values),
            'max': max(values),
            'mean': mean(values),
            'median': median(values),
            'sum': sum(values)
        }
        
        if len(values) > 1:
            stats['stdev'] = stdev(values)
        
        try:
            stats['mode'] = mode(values)
        except:
            pass  # Mode might not exist for all datasets
        
        return stats
    
    def group_by_field(self, data: List[T], field: str) -> Dict[Any, List[T]]:
        """Group data by a field value."""
        groups = defaultdict(list)
        for item in data:
            if hasattr(item, field):
                key = getattr(item, field)
                groups[key].append(item)
        return dict(groups)
    
    def count_by_field(self, data: List[T], field: str) -> Dict[Any, int]:
        """Count occurrences by field value."""
        groups = self.group_by_field(data, field)
        return {key: len(items) for key, items in groups.items()}


class StatisticalAnalyzer(BaseAnalyzer):
    """Analyzer for statistical operations."""
    
    def analyze(self, data: List[T], field: str = None, **kwargs) -> Dict[str, Any]:
        """Analyze statistical properties of data."""
        if not data:
            return {'error': 'No data provided'}
        
        result = {
            'total_count': len(data),
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        if field and hasattr(data[0], field):
            # Analyze specific field
            values = []
            for item in data:
                value = getattr(item, field, None)
                if value is not None and isinstance(value, (int, float)):
                    values.append(value)
            
            if values:
                result[f'{field}_statistics'] = self.calculate_statistics(values)
        
        return result


class TrendAnalyzer(BaseAnalyzer):
    """Analyzer for trend analysis over time."""
    
    def analyze(self, data: List[T], time_field: str = 'created_at', **kwargs) -> Dict[str, Any]:
        """Analyze trends over time."""
        if not data:
            return {'error': 'No data provided'}
        
        # Group by time periods
        time_groups = self._group_by_time_period(data, time_field, kwargs.get('period', 'day'))
        
        # Calculate trend metrics
        time_series = []
        for period, items in sorted(time_groups.items()):
            time_series.append({
                'period': period,
                'count': len(items),
                'items': [item.id for item in items]
            })
        
        # Calculate growth rate
        growth_rates = []
        for i in range(1, len(time_series)):
            current = time_series[i]['count']
            previous = time_series[i-1]['count']
            if previous > 0:
                growth_rate = ((current - previous) / previous) * 100
                growth_rates.append(growth_rate)
        
        return {
            'time_series': time_series,
            'growth_rates': growth_rates,
            'average_growth_rate': mean(growth_rates) if growth_rates else 0,
            'total_periods': len(time_series),
            'peak_period': max(time_series, key=lambda x: x['count']) if time_series else None
        }
    
    def _group_by_time_period(self, data: List[T], time_field: str, period: str) -> Dict[str, List[T]]:
        """Group data by time period."""
        groups = defaultdict(list)
        
        for item in data:
            if hasattr(item, time_field):
                timestamp = getattr(item, time_field)
                if isinstance(timestamp, datetime):
                    if period == 'day':
                        key = timestamp.strftime('%Y-%m-%d')
                    elif period == 'week':
                        key = timestamp.strftime('%Y-W%W')
                    elif period == 'month':
                        key = timestamp.strftime('%Y-%m')
                    elif period == 'year':
                        key = timestamp.strftime('%Y')
                    else:
                        key = timestamp.strftime('%Y-%m-%d')
                    
                    groups[key].append(item)
        
        return dict(groups)


class RelationshipAnalyzer(BaseAnalyzer):
    """Analyzer for relationship patterns."""
    
    def analyze(self, data: List[T], **kwargs) -> Dict[str, Any]:
        """Analyze relationship patterns in data."""
        if not data:
            return {'error': 'No data provided'}
        
        # Find items with relationship fields
        relationship_stats = {}
        
        for item in data:
            for field_name in dir(item):
                if field_name.startswith('_') or not hasattr(item, field_name):
                    continue
                
                field_value = getattr(item, field_name)
                if isinstance(field_value, list) and field_value:
                    # Assume list fields are relationships
                    if field_name not in relationship_stats:
                        relationship_stats[field_name] = {
                            'total_connections': 0,
                            'items_with_connections': 0,
                            'max_connections': 0,
                            'connection_distribution': Counter()
                        }
                    
                    connection_count = len(field_value)
                    relationship_stats[field_name]['total_connections'] += connection_count
                    if connection_count > 0:
                        relationship_stats[field_name]['items_with_connections'] += 1
                    relationship_stats[field_name]['max_connections'] = max(
                        relationship_stats[field_name]['max_connections'], 
                        connection_count
                    )
                    relationship_stats[field_name]['connection_distribution'][connection_count] += 1
        
        # Calculate averages
        for field_name, stats in relationship_stats.items():
            if stats['items_with_connections'] > 0:
                stats['average_connections'] = stats['total_connections'] / len(data)
                stats['average_connections_among_connected'] = (
                    stats['total_connections'] / stats['items_with_connections']
                )
        
        return {
            'total_items': len(data),
            'relationship_statistics': relationship_stats,
            'analysis_timestamp': datetime.now().isoformat()
        }


class FilterEngine:
    """Engine for filtering and searching data."""
    
    def __init__(self):
        self.filters: Dict[str, Callable] = {
            'contains': lambda field_value, filter_value: str(filter_value).lower() in str(field_value).lower(),
            'equals': lambda field_value, filter_value: field_value == filter_value,
            'in': lambda field_value, filter_value: field_value in filter_value,
            'greater_than': lambda field_value, filter_value: field_value > filter_value,
            'less_than': lambda field_value, filter_value: field_value < filter_value,
            'between': lambda field_value, filter_value: filter_value[0] <= field_value <= filter_value[1],
            'starts_with': lambda field_value, filter_value: str(field_value).lower().startswith(str(filter_value).lower()),
            'ends_with': lambda field_value, filter_value: str(field_value).lower().endswith(str(filter_value).lower()),
        }
    
    def filter_data(self, data: List[T], filters: Dict[str, Any]) -> List[T]:
        """Filter data using advanced filter expressions."""
        if not filters:
            return data
        
        filtered_data = []
        for item in data:
            if self._matches_filters(item, filters):
                filtered_data.append(item)
        
        return filtered_data
    
    def _matches_filters(self, item: T, filters: Dict[str, Any]) -> bool:
        """Check if item matches all filters."""
        for filter_expr, filter_value in filters.items():
            if not self._matches_filter(item, filter_expr, filter_value):
                return False
        return True
    
    def _matches_filter(self, item: T, filter_expr: str, filter_value: Any) -> bool:
        """Check if item matches a single filter."""
        # Parse filter expression (e.g., "title__contains" -> field="title", op="contains")
        if '__' in filter_expr:
            field, op = filter_expr.split('__', 1)
        else:
            field, op = filter_expr, 'equals'
        
        if not hasattr(item, field):
            return False
        
        field_value = getattr(item, field)
        
        if op in self.filters:
            return self.filters[op](field_value, filter_value)
        else:
            # Default to equals
            return field_value == filter_value
    
    def search_text(self, data: List[T], query: str, fields: Optional[List[str]] = None) -> List[T]:
        """Search for text across specified fields."""
        if not query:
            return data
        
        query_lower = query.lower()
        results = []
        
        for item in data:
            # Determine fields to search
            if fields:
                search_fields = fields
            else:
                # Default search fields
                search_fields = []
                for field_name in ['title', 'content', 'description', 'name']:
                    if hasattr(item, field_name):
                        search_fields.append(field_name)
            
            # Search in each field
            found = False
            for field in search_fields:
                if hasattr(item, field):
                    field_value = getattr(item, field)
                    if field_value and query_lower in str(field_value).lower():
                        found = True
                        break
            
            # Also search in tags if available
            if not found and hasattr(item, 'tags'):
                for tag in item.tags:
                    if query_lower in tag.lower():
                        found = True
                        break
            
            if found:
                results.append(item)
        
        return results


class AggregationEngine:
    """Engine for data aggregation operations."""
    
    def aggregate(self, data: List[T], operations: Dict[str, Any]) -> Dict[str, Any]:
        """Perform aggregation operations on data."""
        if not data:
            return {}
        
        results = {}
        
        for operation_name, operation_config in operations.items():
            if isinstance(operation_config, str):
                # Simple field aggregation
                field = operation_config
                results[operation_name] = self._aggregate_field(data, field, 'count')
            elif isinstance(operation_config, dict):
                # Complex aggregation
                field = operation_config.get('field')
                agg_type = operation_config.get('type', 'count')
                group_by = operation_config.get('group_by')
                
                if group_by:
                    results[operation_name] = self._aggregate_grouped(data, field, agg_type, group_by)
                else:
                    results[operation_name] = self._aggregate_field(data, field, agg_type)
        
        return results
    
    def _aggregate_field(self, data: List[T], field: str, agg_type: str) -> Any:
        """Aggregate a single field."""
        if not field:
            return len(data)
        
        values = []
        for item in data:
            if hasattr(item, field):
                value = getattr(item, field)
                if value is not None:
                    values.append(value)
        
        if agg_type == 'count':
            return len(values)
        elif agg_type == 'unique_count':
            return len(set(values))
        elif agg_type == 'sum':
            return sum(v for v in values if isinstance(v, (int, float)))
        elif agg_type == 'mean':
            numeric_values = [v for v in values if isinstance(v, (int, float))]
            return mean(numeric_values) if numeric_values else 0
        elif agg_type == 'min':
            return min(values) if values else None
        elif agg_type == 'max':
            return max(values) if values else None
        else:
            return values
    
    def _aggregate_grouped(self, data: List[T], field: str, agg_type: str, group_by: str) -> Dict[Any, Any]:
        """Aggregate data grouped by a field."""
        groups = defaultdict(list)
        
        for item in data:
            if hasattr(item, group_by):
                group_key = getattr(item, group_by)
                groups[group_key].append(item)
        
        results = {}
        for group_key, group_data in groups.items():
            results[group_key] = self._aggregate_field(group_data, field, agg_type)
        
        return results