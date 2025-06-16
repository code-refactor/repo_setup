import json
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional, TypeVar, Generic
from uuid import uuid4

T = TypeVar('T')


def generate_id(prefix: str = "") -> str:
    """Generate a unique ID with optional prefix"""
    return f"{prefix}{uuid4().hex[:8]}" if prefix else uuid4().hex[:8]


def datetime_parser(json_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Parse datetime strings in JSON dictionaries"""
    for key, value in json_dict.items():
        if isinstance(value, str) and key.endswith('_time'):
            try:
                json_dict[key] = datetime.fromisoformat(value)
            except ValueError:
                pass
    return json_dict


class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder for datetime objects"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def calculate_checksum(data: bytes) -> str:
    """Calculate SHA-256 checksum of data"""
    return hashlib.sha256(data).hexdigest()


class Result(Generic[T]):
    """Result wrapper for error handling"""
    def __init__(self, value: Optional[T] = None, error: Optional[Exception] = None):
        self.value = value
        self.error = error
        self.is_success = error is None
    
    def unwrap(self) -> T:
        if self.error:
            raise self.error
        return self.value
    
    def unwrap_or(self, default: T) -> T:
        return self.value if self.is_success else default
    
    def map(self, func):
        """Map the value if successful"""
        if self.is_success:
            try:
                return Result.ok(func(self.value))
            except Exception as e:
                return Result.error(e)
        return self
    
    @classmethod
    def ok(cls, value: T) -> 'Result[T]':
        return cls(value=value)
    
    @classmethod
    def error(cls, error: Exception) -> 'Result[T]':
        return cls(error=error)


def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if division by zero"""
    try:
        return a / b if b != 0 else default
    except (TypeError, ZeroDivisionError):
        return default


def safe_percentage(part: float, total: float) -> float:
    """Safely calculate percentage, handling division by zero"""
    return safe_divide(part * 100, total, 0.0)


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Clamp a value between min and max bounds"""
    return max(min_value, min(value, max_value))


def deep_merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries"""
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """Flatten a nested dictionary"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


class Timer:
    """Simple timer context manager for performance monitoring"""
    
    def __init__(self, name: str = "Timer"):
        self.name = name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = datetime.now()
    
    @property
    def elapsed(self) -> Optional[float]:
        """Get elapsed time in seconds"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
    
    def __str__(self):
        elapsed = self.elapsed
        if elapsed is not None:
            return f"{self.name}: {elapsed:.3f}s"
        return f"{self.name}: Not completed"


def retry_with_backoff(func, max_retries: int = 3, base_delay: float = 1.0, 
                      exponential_base: float = 2.0):
    """Decorator for retrying functions with exponential backoff"""
    import time
    import functools
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < max_retries:
                    delay = base_delay * (exponential_base ** attempt)
                    time.sleep(delay)
                else:
                    raise
        
        raise last_exception
    
    return wrapper


def validate_config(config: Dict[str, Any], required_keys: list, 
                   optional_keys: list = None) -> Result[Dict[str, Any]]:
    """Validate configuration dictionary"""
    optional_keys = optional_keys or []
    
    # Check required keys
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        return Result.error(ValueError(f"Missing required keys: {missing_keys}"))
    
    # Check for unknown keys
    all_allowed_keys = set(required_keys + optional_keys)
    unknown_keys = [key for key in config.keys() if key not in all_allowed_keys]
    if unknown_keys:
        return Result.error(ValueError(f"Unknown keys: {unknown_keys}"))
    
    return Result.ok(config)