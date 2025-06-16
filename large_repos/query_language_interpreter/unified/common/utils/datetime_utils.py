"""
Date and time utilities for the unified query language interpreter.

This module provides common date/time processing functions for handling
temporal queries, date parsing, and time-based calculations.
"""

import re
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple, Union

DateLike = Union[str, datetime]


class DateParser:
    """Parse various date formats into datetime objects."""
    
    def __init__(self):
        self.date_patterns = [
            # ISO formats
            (r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})', '%Y-%m-%dT%H:%M:%S'),
            (r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})', '%Y-%m-%d %H:%M:%S'),
            (r'(\d{4})-(\d{2})-(\d{2})', '%Y-%m-%d'),
            
            # US formats
            (r'(\d{1,2})/(\d{1,2})/(\d{4})', '%m/%d/%Y'),
            (r'(\d{1,2})/(\d{1,2})/(\d{2})', '%m/%d/%y'),
            (r'(\d{1,2})-(\d{1,2})-(\d{4})', '%m-%d-%Y'),
            (r'(\d{1,2})-(\d{1,2})-(\d{2})', '%m-%d-%y'),
            
            # European formats
            (r'(\d{1,2})\.(\d{1,2})\.(\d{4})', '%d.%m.%Y'),
            (r'(\d{1,2})\.(\d{1,2})\.(\d{2})', '%d.%m.%y'),
            
            # Month name formats
            (r'(\w+) (\d{1,2}), (\d{4})', '%B %d, %Y'),
            (r'(\w+) (\d{1,2}) (\d{4})', '%B %d %Y'),
            (r'(\d{1,2}) (\w+) (\d{4})', '%d %B %Y'),
            
            # Time only
            (r'(\d{1,2}):(\d{2}):(\d{2})', '%H:%M:%S'),
            (r'(\d{1,2}):(\d{2})', '%H:%M'),
        ]
        
        # Compile regex patterns
        self.compiled_patterns = [
            (re.compile(pattern), format_str) 
            for pattern, format_str in self.date_patterns
        ]
    
    def parse_date(self, date_string: str) -> Optional[datetime]:
        """Parse a date string into a datetime object."""
        if not date_string or not isinstance(date_string, str):
            return None
        
        date_string = date_string.strip()
        
        # Try each pattern
        for pattern, format_str in self.compiled_patterns:
            if pattern.match(date_string):
                try:
                    return datetime.strptime(date_string, format_str)
                except ValueError:
                    continue
        
        # Try natural language parsing (simplified)
        return self._parse_natural_date(date_string)
    
    def _parse_natural_date(self, date_string: str) -> Optional[datetime]:
        """Parse natural language dates like 'yesterday', 'last week'."""
        date_string = date_string.lower().strip()
        now = datetime.now()
        
        if date_string in ['now', 'today']:
            return now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_string == 'yesterday':
            return (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_string == 'tomorrow':
            return (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_string == 'last week':
            return (now - timedelta(weeks=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_string == 'next week':
            return (now + timedelta(weeks=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_string == 'last month':
            # Approximate - subtract 30 days
            return (now - timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_string == 'next month':
            # Approximate - add 30 days
            return (now + timedelta(days=30)).replace(hour=0, minute=0, second=0, microsecond=0)
        
        return None


class DateRange:
    """Represent and manipulate date ranges."""
    
    def __init__(self, start_date: DateLike, end_date: DateLike):
        self.parser = DateParser()
        
        self.start_date = self._to_datetime(start_date)
        self.end_date = self._to_datetime(end_date)
        
        if self.start_date and self.end_date and self.start_date > self.end_date:
            self.start_date, self.end_date = self.end_date, self.start_date
    
    def _to_datetime(self, date: DateLike) -> Optional[datetime]:
        """Convert various date types to datetime."""
        if isinstance(date, datetime):
            return date
        elif isinstance(date, str):
            return self.parser.parse_date(date)
        else:
            return None
    
    def contains(self, date: DateLike) -> bool:
        """Check if a date is within this range."""
        dt = self._to_datetime(date)
        if not dt or not self.start_date or not self.end_date:
            return False
        return self.start_date <= dt <= self.end_date
    
    def overlaps(self, other: 'DateRange') -> bool:
        """Check if this range overlaps with another."""
        if not all([self.start_date, self.end_date, other.start_date, other.end_date]):
            return False
        
        return (self.start_date <= other.end_date and 
                self.end_date >= other.start_date)
    
    def duration(self) -> Optional[timedelta]:
        """Get the duration of this date range."""
        if self.start_date and self.end_date:
            return self.end_date - self.start_date
        return None
    
    def days_count(self) -> int:
        """Get the number of days in this range."""
        duration = self.duration()
        return duration.days if duration else 0
    
    def split_by_days(self, days: int) -> List['DateRange']:
        """Split the range into smaller ranges of specified days."""
        if not self.start_date or not self.end_date:
            return []
        
        ranges = []
        current_start = self.start_date
        
        while current_start < self.end_date:
            current_end = min(current_start + timedelta(days=days), self.end_date)
            ranges.append(DateRange(current_start, current_end))
            current_start = current_end + timedelta(days=1)
        
        return ranges
    
    def __str__(self) -> str:
        """String representation of the date range."""
        start_str = self.start_date.strftime('%Y-%m-%d') if self.start_date else 'None'
        end_str = self.end_date.strftime('%Y-%m-%d') if self.end_date else 'None'
        return f"DateRange({start_str} to {end_str})"


class TimeFrameResolver:
    """Resolve time frame expressions into concrete date ranges."""
    
    def __init__(self):
        self.parser = DateParser()
    
    def resolve_timeframe(self, expression: str) -> Optional[DateRange]:
        """Resolve a timeframe expression to a DateRange."""
        expression = expression.lower().strip()
        now = datetime.now()
        
        # Handle relative timeframes
        if 'last' in expression:
            return self._resolve_last_timeframe(expression, now)
        elif 'next' in expression:
            return self._resolve_next_timeframe(expression, now)
        elif 'this' in expression:
            return self._resolve_this_timeframe(expression, now)
        elif 'between' in expression:
            return self._resolve_between_timeframe(expression)
        elif 'since' in expression:
            return self._resolve_since_timeframe(expression, now)
        elif 'until' in expression or 'before' in expression:
            return self._resolve_until_timeframe(expression, now)
        else:
            # Try to parse as absolute dates
            return self._resolve_absolute_timeframe(expression)
    
    def _resolve_last_timeframe(self, expression: str, now: datetime) -> Optional[DateRange]:
        """Resolve 'last X' expressions."""
        if 'last week' in expression:
            start = now - timedelta(weeks=1)
            end = now
        elif 'last month' in expression:
            start = now - timedelta(days=30)
            end = now
        elif 'last year' in expression:
            start = now - timedelta(days=365)
            end = now
        elif 'last quarter' in expression:
            start = now - timedelta(days=90)
            end = now
        elif re.search(r'last (\d+) days?', expression):
            match = re.search(r'last (\d+) days?', expression)
            days = int(match.group(1))
            start = now - timedelta(days=days)
            end = now
        elif re.search(r'last (\d+) weeks?', expression):
            match = re.search(r'last (\d+) weeks?', expression)
            weeks = int(match.group(1))
            start = now - timedelta(weeks=weeks)
            end = now
        elif re.search(r'last (\d+) months?', expression):
            match = re.search(r'last (\d+) months?', expression)
            months = int(match.group(1))
            start = now - timedelta(days=months * 30)  # Approximate
            end = now
        else:
            return None
        
        return DateRange(start, end)
    
    def _resolve_next_timeframe(self, expression: str, now: datetime) -> Optional[DateRange]:
        """Resolve 'next X' expressions."""
        if 'next week' in expression:
            start = now
            end = now + timedelta(weeks=1)
        elif 'next month' in expression:
            start = now
            end = now + timedelta(days=30)
        elif 'next year' in expression:
            start = now
            end = now + timedelta(days=365)
        elif re.search(r'next (\d+) days?', expression):
            match = re.search(r'next (\d+) days?', expression)
            days = int(match.group(1))
            start = now
            end = now + timedelta(days=days)
        else:
            return None
        
        return DateRange(start, end)
    
    def _resolve_this_timeframe(self, expression: str, now: datetime) -> Optional[DateRange]:
        """Resolve 'this X' expressions."""
        if 'this week' in expression:
            # Start of current week (Monday)
            start = now - timedelta(days=now.weekday())
            end = start + timedelta(days=6)
        elif 'this month' in expression:
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            # Last day of current month
            if now.month == 12:
                next_month = now.replace(year=now.year + 1, month=1, day=1)
            else:
                next_month = now.replace(month=now.month + 1, day=1)
            end = next_month - timedelta(days=1)
        elif 'this year' in expression:
            start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end = now.replace(month=12, day=31, hour=23, minute=59, second=59)
        elif 'this quarter' in expression:
            quarter = (now.month - 1) // 3 + 1
            quarter_start_month = (quarter - 1) * 3 + 1
            start = now.replace(month=quarter_start_month, day=1, hour=0, minute=0, second=0, microsecond=0)
            
            if quarter == 4:
                end = now.replace(month=12, day=31, hour=23, minute=59, second=59)
            else:
                end_month = quarter * 3
                end = now.replace(month=end_month, day=31, hour=23, minute=59, second=59)
        else:
            return None
        
        return DateRange(start, end)
    
    def _resolve_between_timeframe(self, expression: str) -> Optional[DateRange]:
        """Resolve 'between X and Y' expressions."""
        # Extract dates from between expression
        pattern = r'between\s+(.+?)\s+and\s+(.+)'
        match = re.search(pattern, expression)
        
        if match:
            start_str = match.group(1).strip()
            end_str = match.group(2).strip()
            
            start_date = self.parser.parse_date(start_str)
            end_date = self.parser.parse_date(end_str)
            
            if start_date and end_date:
                return DateRange(start_date, end_date)
        
        return None
    
    def _resolve_since_timeframe(self, expression: str, now: datetime) -> Optional[DateRange]:
        """Resolve 'since X' expressions."""
        pattern = r'since\s+(.+)'
        match = re.search(pattern, expression)
        
        if match:
            date_str = match.group(1).strip()
            start_date = self.parser.parse_date(date_str)
            
            if start_date:
                return DateRange(start_date, now)
        
        return None
    
    def _resolve_until_timeframe(self, expression: str, now: datetime) -> Optional[DateRange]:
        """Resolve 'until X' or 'before X' expressions."""
        patterns = [r'until\s+(.+)', r'before\s+(.+)']
        
        for pattern in patterns:
            match = re.search(pattern, expression)
            if match:
                date_str = match.group(1).strip()
                end_date = self.parser.parse_date(date_str)
                
                if end_date:
                    # Use a reasonable start date (1 year ago)
                    start_date = now - timedelta(days=365)
                    return DateRange(start_date, end_date)
        
        return None
    
    def _resolve_absolute_timeframe(self, expression: str) -> Optional[DateRange]:
        """Resolve absolute date expressions."""
        # Try to find two dates in the expression
        dates = []
        words = expression.split()
        
        for i, word in enumerate(words):
            # Try different combinations of words as potential dates
            for j in range(i + 1, min(i + 4, len(words) + 1)):
                date_str = ' '.join(words[i:j])
                parsed_date = self.parser.parse_date(date_str)
                if parsed_date:
                    dates.append(parsed_date)
                    break
        
        if len(dates) >= 2:
            return DateRange(dates[0], dates[1])
        elif len(dates) == 1:
            # Single date - treat as a single day range
            date = dates[0]
            start = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end = date.replace(hour=23, minute=59, second=59, microsecond=999999)
            return DateRange(start, end)
        
        return None


class DateFormatter:
    """Format dates for display and output."""
    
    @staticmethod
    def format_datetime(dt: datetime, format_type: str = 'iso') -> str:
        """Format datetime according to specified type."""
        if format_type == 'iso':
            return dt.isoformat()
        elif format_type == 'us':
            return dt.strftime('%m/%d/%Y %I:%M %p')
        elif format_type == 'european':
            return dt.strftime('%d.%m.%Y %H:%M')
        elif format_type == 'readable':
            return dt.strftime('%B %d, %Y at %I:%M %p')
        elif format_type == 'date_only':
            return dt.strftime('%Y-%m-%d')
        elif format_type == 'time_only':
            return dt.strftime('%H:%M:%S')
        else:
            return dt.strftime(format_type)
    
    @staticmethod
    def format_duration(duration: timedelta) -> str:
        """Format duration in human-readable form."""
        total_seconds = int(duration.total_seconds())
        
        if total_seconds < 60:
            return f"{total_seconds} seconds"
        elif total_seconds < 3600:
            minutes = total_seconds // 60
            return f"{minutes} minutes"
        elif total_seconds < 86400:
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours} hours, {minutes} minutes" if minutes > 0 else f"{hours} hours"
        else:
            days = total_seconds // 86400
            hours = (total_seconds % 86400) // 3600
            return f"{days} days, {hours} hours" if hours > 0 else f"{days} days"
    
    @staticmethod
    def format_relative_time(dt: datetime, reference: Optional[datetime] = None) -> str:
        """Format datetime relative to a reference time (default: now)."""
        if reference is None:
            reference = datetime.now()
        
        delta = reference - dt
        
        if delta.total_seconds() < 0:
            # Future time
            delta = -delta
            prefix = "in "
            suffix = ""
        else:
            # Past time
            prefix = ""
            suffix = " ago"
        
        total_seconds = int(delta.total_seconds())
        
        if total_seconds < 60:
            return f"{prefix}{total_seconds} seconds{suffix}"
        elif total_seconds < 3600:
            minutes = total_seconds // 60
            return f"{prefix}{minutes} minutes{suffix}"
        elif total_seconds < 86400:
            hours = total_seconds // 3600
            return f"{prefix}{hours} hours{suffix}"
        elif total_seconds < 2592000:  # 30 days
            days = total_seconds // 86400
            return f"{prefix}{days} days{suffix}"
        elif total_seconds < 31536000:  # 365 days
            months = total_seconds // 2592000
            return f"{prefix}{months} months{suffix}"
        else:
            years = total_seconds // 31536000
            return f"{prefix}{years} years{suffix}"


class TimezoneUtils:
    """Timezone handling utilities."""
    
    @staticmethod
    def to_utc(dt: datetime) -> datetime:
        """Convert datetime to UTC."""
        if dt.tzinfo is None:
            # Assume local timezone
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    
    @staticmethod
    def from_timestamp(timestamp: Union[int, float]) -> datetime:
        """Convert Unix timestamp to datetime."""
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
    
    @staticmethod
    def to_timestamp(dt: datetime) -> float:
        """Convert datetime to Unix timestamp."""
        return dt.timestamp()
    
    @staticmethod
    def is_business_day(dt: datetime) -> bool:
        """Check if datetime falls on a business day (Monday-Friday)."""
        return dt.weekday() < 5
    
    @staticmethod
    def is_business_hours(dt: datetime, start_hour: int = 9, end_hour: int = 17) -> bool:
        """Check if datetime falls within business hours."""
        return start_hour <= dt.hour < end_hour