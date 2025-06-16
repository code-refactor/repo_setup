"""
Common utilities and helpers for the unified personal knowledge management library.
"""

import re
import string
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set, Union
from uuid import UUID, uuid4


class UUIDUtils:
    """Utilities for handling UUIDs."""
    
    @staticmethod
    def generate() -> UUID:
        """Generate a new UUID."""
        return uuid4()
    
    @staticmethod
    def is_valid(uuid_str: str) -> bool:
        """Check if a string is a valid UUID."""
        try:
            UUID(uuid_str)
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def from_string(uuid_str: str) -> Optional[UUID]:
        """Convert string to UUID, return None if invalid."""
        try:
            return UUID(uuid_str)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def to_string(uuid_obj: UUID) -> str:
        """Convert UUID to string."""
        return str(uuid_obj)
    
    @staticmethod
    def generate_short_id(length: int = 8) -> str:
        """Generate a short ID based on UUID."""
        return str(uuid4()).replace('-', '')[:length]


class DateUtils:
    """Utilities for handling dates and times."""
    
    @staticmethod
    def now() -> datetime:
        """Get current datetime."""
        return datetime.now()
    
    @staticmethod
    def parse_iso(date_str: str) -> Optional[datetime]:
        """Parse ISO format date string."""
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None
    
    @staticmethod
    def to_iso(dt: datetime) -> str:
        """Convert datetime to ISO format string."""
        return dt.isoformat()
    
    @staticmethod
    def format_relative(dt: datetime) -> str:
        """Format datetime as relative time (e.g., '2 hours ago')."""
        now = datetime.now()
        if dt > now:
            return "in the future"
        
        diff = now - dt
        
        if diff.days > 0:
            if diff.days == 1:
                return "yesterday"
            elif diff.days < 7:
                return f"{diff.days} days ago"
            elif diff.days < 30:
                weeks = diff.days // 7
                return f"{weeks} week{'s' if weeks > 1 else ''} ago"
            elif diff.days < 365:
                months = diff.days // 30
                return f"{months} month{'s' if months > 1 else ''} ago"
            else:
                years = diff.days // 365
                return f"{years} year{'s' if years > 1 else ''} ago"
        
        hours = diff.seconds // 3600
        if hours > 0:
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        
        minutes = diff.seconds // 60
        if minutes > 0:
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        
        return "just now"
    
    @staticmethod
    def add_days(dt: datetime, days: int) -> datetime:
        """Add days to a datetime."""
        return dt + timedelta(days=days)
    
    @staticmethod
    def add_hours(dt: datetime, hours: int) -> datetime:
        """Add hours to a datetime."""
        return dt + timedelta(hours=hours)
    
    @staticmethod
    def start_of_day(dt: datetime) -> datetime:
        """Get start of day for a datetime."""
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    
    @staticmethod
    def end_of_day(dt: datetime) -> datetime:
        """Get end of day for a datetime."""
        return dt.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    @staticmethod
    def days_between(start: datetime, end: datetime) -> int:
        """Calculate days between two datetimes."""
        return (end.date() - start.date()).days


class ValidationUtils:
    """Utilities for data validation."""
    
    @staticmethod
    def is_email(email: str) -> bool:
        """Check if string is a valid email address."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def is_url(url: str) -> bool:
        """Check if string is a valid URL."""
        pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$'
        return bool(re.match(pattern, url))
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize a string to be safe for use as a filename."""
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Remove leading/trailing whitespace and dots
        filename = filename.strip(' .')
        
        # Ensure it's not empty
        if not filename:
            filename = 'untitled'
        
        return filename
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
        """Validate that required fields are present and not empty."""
        missing_fields = []
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields.append(field)
        return missing_fields
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text by removing extra whitespace and converting to lowercase."""
        if not text:
            return ""
        return ' '.join(text.strip().lower().split())
    
    @staticmethod
    def is_valid_tag(tag: str) -> bool:
        """Check if a string is a valid tag."""
        if not tag or not isinstance(tag, str):
            return False
        
        # Remove whitespace
        tag = tag.strip()
        
        # Check length
        if len(tag) == 0 or len(tag) > 50:
            return False
        
        # Check for invalid characters
        invalid_chars = set('<>:"/\\|?*[]{}()+=!@#$%^&')
        return not any(char in invalid_chars for char in tag)


class SearchUtils:
    """Utilities for text search and indexing."""
    
    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Tokenize text into words."""
        if not text:
            return []
        
        # Convert to lowercase and split on whitespace and punctuation
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens
    
    @staticmethod
    def remove_stop_words(tokens: List[str], stop_words: Optional[Set[str]] = None) -> List[str]:
        """Remove common stop words from tokens."""
        if stop_words is None:
            stop_words = {
                'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
                'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
                'to', 'was', 'were', 'will', 'with', 'the', 'this', 'but', 'they',
                'have', 'had', 'what', 'said', 'each', 'which', 'she', 'do',
                'how', 'their', 'if', 'up', 'out', 'many', 'then', 'them'
            }
        
        return [token for token in tokens if token not in stop_words]
    
    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """Calculate simple similarity between two texts."""
        if not text1 or not text2:
            return 0.0
        
        tokens1 = set(SearchUtils.tokenize(text1))
        tokens2 = set(SearchUtils.tokenize(text2))
        
        if not tokens1 or not tokens2:
            return 0.0
        
        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)
        
        return len(intersection) / len(union)
    
    @staticmethod
    def highlight_matches(text: str, query: str, highlight_start: str = "**", highlight_end: str = "**") -> str:
        """Highlight query matches in text."""
        if not query or not text:
            return text
        
        # Escape special regex characters in query
        escaped_query = re.escape(query)
        
        # Find and replace matches (case insensitive)
        pattern = re.compile(escaped_query, re.IGNORECASE)
        
        def replace_match(match):
            return f"{highlight_start}{match.group()}{highlight_end}"
        
        return pattern.sub(replace_match, text)
    
    @staticmethod
    def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
        """Extract keywords from text using simple frequency analysis."""
        if not text:
            return []
        
        tokens = SearchUtils.tokenize(text)
        tokens = SearchUtils.remove_stop_words(tokens)
        
        # Filter out very short words
        tokens = [token for token in tokens if len(token) > 2]
        
        # Count frequency
        word_freq = {}
        for token in tokens:
            word_freq[token] = word_freq.get(token, 0) + 1
        
        # Sort by frequency and return top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:max_keywords]]


class TextUtils:
    """Utilities for text processing and formatting."""
    
    @staticmethod
    def truncate(text: str, max_length: int, suffix: str = "...") -> str:
        """Truncate text to maximum length."""
        if not text or len(text) <= max_length:
            return text
        
        if max_length <= len(suffix):
            return suffix[:max_length]
        
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def word_count(text: str) -> int:
        """Count words in text."""
        if not text:
            return 0
        return len(text.split())
    
    @staticmethod
    def reading_time(text: str, words_per_minute: int = 200) -> int:
        """Calculate estimated reading time in minutes."""
        word_count = TextUtils.word_count(text)
        return max(1, word_count // words_per_minute)
    
    @staticmethod
    def excerpt(text: str, max_words: int = 50) -> str:
        """Create an excerpt from text."""
        if not text:
            return ""
        
        words = text.split()
        if len(words) <= max_words:
            return text
        
        return ' '.join(words[:max_words]) + "..."
    
    @staticmethod
    def remove_html_tags(text: str) -> str:
        """Remove HTML tags from text."""
        if not text:
            return ""
        
        # Simple regex to remove HTML tags
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)
    
    @staticmethod
    def slugify(text: str) -> str:
        """Convert text to URL-friendly slug."""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Replace spaces and special characters with hyphens
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        
        # Remove leading/trailing hyphens
        return text.strip('-')
    
    @staticmethod
    def capitalize_words(text: str) -> str:
        """Capitalize first letter of each word."""
        if not text:
            return ""
        return string.capwords(text)


class CollectionUtils:
    """Utilities for working with collections."""
    
    @staticmethod
    def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
        """Split a list into chunks of specified size."""
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
    
    @staticmethod
    def flatten_list(nested_list: List[List[Any]]) -> List[Any]:
        """Flatten a nested list."""
        return [item for sublist in nested_list for item in sublist]
    
    @staticmethod
    def unique_preserve_order(lst: List[Any]) -> List[Any]:
        """Remove duplicates from list while preserving order."""
        seen = set()
        result = []
        for item in lst:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    
    @staticmethod
    def group_by_key(items: List[Dict[str, Any]], key: str) -> Dict[Any, List[Dict[str, Any]]]:
        """Group list of dictionaries by a key."""
        groups = {}
        for item in items:
            group_key = item.get(key)
            if group_key not in groups:
                groups[group_key] = []
            groups[group_key].append(item)
        return groups
    
    @staticmethod
    def sort_by_key(items: List[Dict[str, Any]], key: str, reverse: bool = False) -> List[Dict[str, Any]]:
        """Sort list of dictionaries by a key."""
        return sorted(items, key=lambda x: x.get(key, ''), reverse=reverse)
    
    @staticmethod
    def merge_dictionaries(*dicts: Dict[str, Any]) -> Dict[str, Any]:
        """Merge multiple dictionaries."""
        result = {}
        for d in dicts:
            result.update(d)
        return result


class ConfigUtils:
    """Utilities for configuration management."""
    
    @staticmethod
    def get_nested_value(data: Dict[str, Any], key_path: str, default: Any = None) -> Any:
        """Get nested value from dictionary using dot notation."""
        keys = key_path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        
        return current
    
    @staticmethod
    def set_nested_value(data: Dict[str, Any], key_path: str, value: Any) -> None:
        """Set nested value in dictionary using dot notation."""
        keys = key_path.split('.')
        current = data
        
        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    @staticmethod
    def flatten_config(config: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
        """Flatten nested configuration dictionary."""
        flattened = {}
        
        for key, value in config.items():
            new_key = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, dict):
                flattened.update(ConfigUtils.flatten_config(value, new_key))
            else:
                flattened[new_key] = value
        
        return flattened
    
    @staticmethod
    def expand_config(flattened_config: Dict[str, Any]) -> Dict[str, Any]:
        """Expand flattened configuration back to nested structure."""
        expanded = {}
        
        for key, value in flattened_config.items():
            ConfigUtils.set_nested_value(expanded, key, value)
        
        return expanded