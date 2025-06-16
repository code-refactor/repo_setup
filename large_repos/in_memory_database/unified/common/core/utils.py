"""
Utility functions for the unified in-memory database library.

This module provides common utility functions that can be shared across both
vectordb and syncdb implementations.
"""

import json
import time
import uuid
import hashlib
from typing import Any, List, Dict, Union, Callable, Optional
from datetime import datetime


# ID Generation
def generate_id() -> str:
    """Generate a unique identifier."""
    return str(uuid.uuid4())


def generate_client_id() -> str:
    """Generate a client-specific identifier."""
    return f"client_{uuid.uuid4().hex[:8]}"


def generate_deterministic_id(data: str) -> str:
    """Generate a deterministic ID based on input data."""
    return hashlib.sha256(data.encode()).hexdigest()[:16]


# Validation Functions
def validate_type(value: Any, expected_type: type, name: str):
    """Validate that value is of expected type."""
    if not isinstance(value, expected_type):
        raise TypeError(f"{name} must be of type {expected_type.__name__}, got {type(value).__name__}")


def validate_range(value: Union[int, float], min_val: Union[int, float], 
                  max_val: Union[int, float], name: str):
    """Validate that value is within specified range."""
    if not (min_val <= value <= max_val):
        raise ValueError(f"{name} must be between {min_val} and {max_val}, got {value}")


def validate_dimensions(vector1: List[float], vector2: List[float], operation: str):
    """Validate that two vectors have the same dimensions."""
    if len(vector1) != len(vector2):
        raise ValueError(f"Cannot perform {operation}: vectors have different dimensions "
                        f"({len(vector1)} vs {len(vector2)})")


def validate_non_empty(value: Union[List, Dict, str], name: str):
    """Validate that value is not empty."""
    if not value:
        raise ValueError(f"{name} cannot be empty")


def validate_positive(value: Union[int, float], name: str):
    """Validate that value is positive."""
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")


def validate_non_negative(value: Union[int, float], name: str):
    """Validate that value is non-negative."""
    if value < 0:
        raise ValueError(f"{name} must be non-negative, got {value}")


# Time Utilities
def get_timestamp() -> float:
    """Get current timestamp."""
    return time.time()


def format_timestamp(timestamp: float, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """Format timestamp as string."""
    return datetime.fromtimestamp(timestamp).strftime(format_str)


def timestamp_to_datetime(timestamp: float) -> datetime:
    """Convert timestamp to datetime object."""
    return datetime.fromtimestamp(timestamp)


def datetime_to_timestamp(dt: datetime) -> float:
    """Convert datetime to timestamp."""
    return dt.timestamp()


# JSON Utilities
def safe_json_serialize(obj: Any) -> str:
    """Safely serialize object to JSON string."""
    try:
        return json.dumps(obj, default=str)
    except Exception as e:
        raise ValueError(f"Failed to serialize object to JSON: {e}")


def safe_json_deserialize(json_str: str) -> Any:
    """Safely deserialize JSON string to object."""
    try:
        return json.loads(json_str)
    except Exception as e:
        raise ValueError(f"Failed to deserialize JSON string: {e}")


# Collection Utilities
def flatten_dict(d: Dict[str, Any], separator: str = '.') -> Dict[str, Any]:
    """Flatten nested dictionary."""
    result = {}
    
    def _flatten(obj, parent_key=''):
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_key = f"{parent_key}{separator}{key}" if parent_key else key
                _flatten(value, new_key)
        else:
            result[parent_key] = obj
    
    _flatten(d)
    return result


def unflatten_dict(d: Dict[str, Any], separator: str = '.') -> Dict[str, Any]:
    """Unflatten dictionary with separator-based keys."""
    result = {}
    for key, value in d.items():
        keys = key.split(separator)
        current = result
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
    return result


def deep_merge(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries."""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def filter_dict(d: Dict[str, Any], predicate: Callable[[str, Any], bool]) -> Dict[str, Any]:
    """Filter dictionary based on predicate function."""
    return {k: v for k, v in d.items() if predicate(k, v)}


# String Utilities
def camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case."""
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_to_camel(name: str) -> str:
    """Convert snake_case to camelCase."""
    components = name.split('_')
    return components[0] + ''.join(word.capitalize() for word in components[1:])


# Hashing Utilities
def hash_object(obj: Any) -> str:
    """Generate hash for any object."""
    if isinstance(obj, dict):
        # Sort keys for consistent hashing
        sorted_items = sorted(obj.items())
        content = json.dumps(sorted_items, sort_keys=True)
    elif isinstance(obj, (list, tuple)):
        content = json.dumps(list(obj), sort_keys=True)
    else:
        content = str(obj)
    
    return hashlib.sha256(content.encode()).hexdigest()


def hash_vector(vector: List[float], precision: int = 6) -> str:
    """Generate hash for vector with specified precision."""
    rounded_vector = [round(x, precision) for x in vector]
    return hash_object(rounded_vector)


# Retry Utilities
def retry_on_exception(max_attempts: int = 3, delay: float = 1.0, 
                      exceptions: tuple = (Exception,)):
    """Decorator to retry function on specified exceptions."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay * (2 ** attempt))  # Exponential backoff
                    continue
            raise last_exception
        return wrapper
    return decorator


# Batch Processing Utilities
def batch_process(items: List[Any], batch_size: int, 
                 process_func: Callable[[List[Any]], Any]) -> List[Any]:
    """Process items in batches."""
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        result = process_func(batch)
        if isinstance(result, list):
            results.extend(result)
        else:
            results.append(result)
    return results


def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split list into chunks of specified size."""
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


# Comparison Utilities
def approximately_equal(a: float, b: float, tolerance: float = 1e-9) -> bool:
    """Check if two floats are approximately equal."""
    return abs(a - b) < tolerance


def compare_vectors(v1: List[float], v2: List[float], tolerance: float = 1e-9) -> bool:
    """Compare two vectors for approximate equality."""
    if len(v1) != len(v2):
        return False
    return all(approximately_equal(a, b, tolerance) for a, b in zip(v1, v2))