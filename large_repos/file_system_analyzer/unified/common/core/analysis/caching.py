"""
Result caching with TTL support.

This module provides caching functionality for analysis results
with time-to-live (TTL) based expiration.
"""

import time
import pickle
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from threading import Lock

from ..types.models import CacheEntry

logger = logging.getLogger(__name__)


class CacheManager:
    """TTL-based result caching manager."""
    
    def __init__(self, default_ttl: int = 3600, max_size: int = 1000):
        """
        Initialize cache manager.
        
        Args:
            default_ttl: Default time-to-live in seconds
            max_size: Maximum number of cache entries
        """
        self.default_ttl = default_ttl
        self.max_size = max_size
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = Lock()
        
    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve cached result.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        with self._lock:
            entry = self._cache.get(key)
            
            if entry is None:
                return None
            
            if entry.is_expired:
                # Remove expired entry
                del self._cache[key]
                logger.debug(f"Cache entry {key} expired and removed")
                return None
            
            logger.debug(f"Cache hit for key {key}")
            return entry.value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Store result with TTL.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses default if not provided)
        """
        ttl = ttl or self.default_ttl
        expires_at = datetime.now() + timedelta(seconds=ttl)
        
        with self._lock:
            # Check if we need to evict old entries
            if len(self._cache) >= self.max_size:
                self._evict_expired()
                
                # If still at max size, evict oldest entry
                if len(self._cache) >= self.max_size:
                    oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k].created_at)
                    del self._cache[oldest_key]
                    logger.debug(f"Evicted oldest cache entry {oldest_key}")
            
            entry = CacheEntry(
                key=key,
                value=value,
                ttl_seconds=ttl,
                expires_at=expires_at
            )
            
            self._cache[key] = entry
            logger.debug(f"Cached result for key {key} (TTL: {ttl}s)")
    
    def delete(self, key: str) -> bool:
        """
        Delete cached entry.
        
        Args:
            key: Cache key to delete
            
        Returns:
            True if entry was deleted, False if not found
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                logger.debug(f"Deleted cache entry {key}")
                return True
            return False
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
            logger.debug("Cleared all cache entries")
    
    def _evict_expired(self) -> None:
        """Remove expired entries from cache."""
        expired_keys = [
            key for key, entry in self._cache.items()
            if entry.is_expired
        ]
        
        for key in expired_keys:
            del self._cache[key]
        
        if expired_keys:
            logger.debug(f"Evicted {len(expired_keys)} expired cache entries")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        with self._lock:
            self._evict_expired()
            
            total_entries = len(self._cache)
            total_size_bytes = 0
            
            try:
                # Estimate memory usage
                for entry in self._cache.values():
                    total_size_bytes += len(pickle.dumps(entry.value))
            except Exception:
                # If pickling fails, just set to 0
                total_size_bytes = 0
            
            return {
                "total_entries": total_entries,
                "max_size": self.max_size,
                "utilization": total_entries / self.max_size if self.max_size > 0 else 0,
                "estimated_size_bytes": total_size_bytes,
                "default_ttl": self.default_ttl
            }
    
    def contains(self, key: str) -> bool:
        """
        Check if key exists in cache and is not expired.
        
        Args:
            key: Cache key to check
            
        Returns:
            True if key exists and is not expired
        """
        return self.get(key) is not None


class MemoryCache(CacheManager):
    """In-memory cache implementation."""
    pass


class FileCache(CacheManager):
    """File-based cache implementation (placeholder for future enhancement)."""
    
    def __init__(self, cache_dir: str, default_ttl: int = 3600, max_size: int = 1000):
        """
        Initialize file-based cache.
        
        Args:
            cache_dir: Directory to store cache files
            default_ttl: Default time-to-live in seconds
            max_size: Maximum number of cache entries
        """
        super().__init__(default_ttl, max_size)
        self.cache_dir = cache_dir
        # TODO: Implement file-based caching for persistent storage
        logger.warning("FileCache not fully implemented, falling back to memory cache")


def create_cache_key(*args: Any) -> str:
    """
    Create a cache key from arguments.
    
    Args:
        *args: Arguments to create key from
        
    Returns:
        Cache key string
    """
    try:
        # Create a deterministic key from the arguments
        key_parts = []
        for arg in args:
            if hasattr(arg, '__dict__'):
                # For objects, use their dict representation
                key_parts.append(str(sorted(arg.__dict__.items())))
            else:
                key_parts.append(str(arg))
        
        key = "|".join(key_parts)
        
        # Hash the key if it's too long
        if len(key) > 200:
            import hashlib
            return hashlib.sha256(key.encode()).hexdigest()
        
        return key
        
    except Exception as e:
        logger.warning(f"Failed to create cache key from args: {e}")
        # Fallback to timestamp-based key
        return f"cache_key_{time.time()}"