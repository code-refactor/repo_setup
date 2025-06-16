import hashlib
import json
import pickle
from typing import Any, Dict, Optional, Union, Callable
from functools import wraps
from datetime import datetime, timedelta


class CacheUtils:
    """Caching utilities for financial analysis operations."""
    
    @staticmethod
    def generate_cache_key(*args, **kwargs) -> str:
        """Generate a consistent cache key from arguments."""
        # Convert all arguments to a serializable format
        key_data = {
            'args': [CacheUtils._serialize_for_key(arg) for arg in args],
            'kwargs': {k: CacheUtils._serialize_for_key(v) for k, v in sorted(kwargs.items())}
        }
        
        # Create hash from serialized data
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_string.encode('utf-8')).hexdigest()
    
    @staticmethod
    def _serialize_for_key(obj: Any) -> Any:
        """Convert object to a serializable format for cache key generation."""
        if obj is None:
            return None
        elif isinstance(obj, (str, int, float, bool)):
            return obj
        elif isinstance(obj, (list, tuple)):
            return [CacheUtils._serialize_for_key(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: CacheUtils._serialize_for_key(v) for k, v in sorted(obj.items())}
        elif hasattr(obj, '__dict__'):
            # For custom objects, use their attributes
            return CacheUtils._serialize_for_key(vars(obj))
        else:
            # Fallback to string representation
            return str(obj)
    
    @staticmethod
    def memoize(ttl_seconds: Optional[int] = None, max_size: int = 128):
        """
        Decorator for memoizing function results.
        
        Args:
            ttl_seconds: Time to live for cached results (None = no expiration)
            max_size: Maximum number of cached results
        """
        def decorator(func: Callable) -> Callable:
            cache = {}
            cache_times = {}
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key
                cache_key = CacheUtils.generate_cache_key(*args, **kwargs)
                
                # Check if result is cached and not expired
                if cache_key in cache:
                    if ttl_seconds is None:
                        return cache[cache_key]
                    
                    cache_time = cache_times.get(cache_key)
                    if cache_time and datetime.now() - cache_time < timedelta(seconds=ttl_seconds):
                        return cache[cache_key]
                    else:
                        # Expired, remove from cache
                        del cache[cache_key]
                        if cache_key in cache_times:
                            del cache_times[cache_key]
                
                # Execute function and cache result
                result = func(*args, **kwargs)
                
                # Implement LRU eviction if cache is full
                if len(cache) >= max_size:
                    # Remove oldest entry
                    if cache_times:
                        oldest_key = min(cache_times.keys(), key=lambda k: cache_times[k])
                        del cache[oldest_key]
                        del cache_times[oldest_key]
                    elif cache:
                        # Fallback: remove arbitrary entry
                        arbitrary_key = next(iter(cache))
                        del cache[arbitrary_key]
                
                cache[cache_key] = result
                cache_times[cache_key] = datetime.now()
                
                return result
            
            # Add cache management methods
            wrapper.cache_clear = lambda: cache.clear() or cache_times.clear()
            wrapper.cache_info = lambda: {
                'size': len(cache),
                'max_size': max_size,
                'ttl_seconds': ttl_seconds
            }
            
            return wrapper
        return decorator
    
    @staticmethod
    def cache_result(cache_dict: Dict[str, Any], key: str, result: Any, 
                    ttl_seconds: Optional[int] = None) -> None:
        """Store result in cache dictionary with optional TTL."""
        cache_entry = {
            'result': result,
            'timestamp': datetime.now()
        }
        
        if ttl_seconds:
            cache_entry['expires_at'] = datetime.now() + timedelta(seconds=ttl_seconds)
        
        cache_dict[key] = cache_entry
    
    @staticmethod
    def get_cached_result(cache_dict: Dict[str, Any], key: str) -> Optional[Any]:
        """Retrieve result from cache dictionary, checking TTL."""
        if key not in cache_dict:
            return None
        
        cache_entry = cache_dict[key]
        
        # Check if expired
        if 'expires_at' in cache_entry:
            if datetime.now() > cache_entry['expires_at']:
                del cache_dict[key]
                return None
        
        return cache_entry['result']
    
    @staticmethod
    def is_cache_valid(cache_dict: Dict[str, Any], key: str) -> bool:
        """Check if cached entry is valid (exists and not expired)."""
        if key not in cache_dict:
            return False
        
        cache_entry = cache_dict[key]
        
        # Check if expired
        if 'expires_at' in cache_entry:
            return datetime.now() <= cache_entry['expires_at']
        
        return True
    
    @staticmethod
    def cleanup_expired_cache(cache_dict: Dict[str, Any]) -> int:
        """Remove expired entries from cache dictionary. Returns number removed."""
        current_time = datetime.now()
        expired_keys = []
        
        for key, cache_entry in cache_dict.items():
            if 'expires_at' in cache_entry:
                if current_time > cache_entry['expires_at']:
                    expired_keys.append(key)
        
        for key in expired_keys:
            del cache_dict[key]
        
        return len(expired_keys)
    
    @staticmethod
    def get_cache_stats(cache_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Get statistics about a cache dictionary."""
        current_time = datetime.now()
        total_entries = len(cache_dict)
        expired_entries = 0
        entries_with_ttl = 0
        
        for cache_entry in cache_dict.values():
            if 'expires_at' in cache_entry:
                entries_with_ttl += 1
                if current_time > cache_entry['expires_at']:
                    expired_entries += 1
        
        return {
            'total_entries': total_entries,
            'expired_entries': expired_entries,
            'valid_entries': total_entries - expired_entries,
            'entries_with_ttl': entries_with_ttl,
            'entries_without_ttl': total_entries - entries_with_ttl
        }
    
    @staticmethod
    def serialize_for_cache(obj: Any) -> bytes:
        """Serialize object for storage in persistent cache."""
        return pickle.dumps(obj)
    
    @staticmethod
    def deserialize_from_cache(data: bytes) -> Any:
        """Deserialize object from persistent cache."""
        return pickle.loads(data)
    
    @staticmethod
    def create_cache_key_from_object(obj: Any, operation: str = "") -> str:
        """Create cache key from object state and operation."""
        if hasattr(obj, '__dict__'):
            obj_data = vars(obj)
        else:
            obj_data = str(obj)
        
        combined_data = {
            'object': obj_data,
            'operation': operation,
            'timestamp': datetime.now().date().isoformat()  # Daily cache invalidation
        }
        
        return CacheUtils.generate_cache_key(combined_data)