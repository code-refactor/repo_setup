import time
from typing import Any, Dict, Optional
from dataclasses import dataclass
from threading import RLock


@dataclass
class CacheEntry:
    """Cache entry with value and metadata."""
    value: Any
    created_at: float
    ttl_seconds: Optional[int] = None
    access_count: int = 0
    last_accessed: float = 0
    
    def __post_init__(self):
        if self.last_accessed == 0:
            self.last_accessed = self.created_at
    
    def is_expired(self) -> bool:
        """Check if cache entry is expired."""
        if self.ttl_seconds is None:
            return False
        return time.time() - self.created_at > self.ttl_seconds
    
    def access(self) -> Any:
        """Access the cached value and update access tracking."""
        self.access_count += 1
        self.last_accessed = time.time()
        return self.value


class CacheManager:
    """Thread-safe cache manager for analysis results."""
    
    def __init__(self, max_size: int = 1000, default_ttl_seconds: Optional[int] = 3600):
        self._cache: Dict[str, CacheEntry] = {}
        self._max_size = max_size
        self._default_ttl = default_ttl_seconds
        self._lock = RLock()
        self._hits = 0
        self._misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        with self._lock:
            if key not in self._cache:
                self._misses += 1
                return None
            
            entry = self._cache[key]
            
            if entry.is_expired():
                del self._cache[key]
                self._misses += 1
                return None
            
            self._hits += 1
            return entry.access()
    
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """Set value in cache."""
        with self._lock:
            # Use default TTL if not specified
            if ttl_seconds is None:
                ttl_seconds = self._default_ttl
            
            # Evict expired entries if cache is full
            if len(self._cache) >= self._max_size:
                self._evict_expired()
                
                # If still full after evicting expired, remove LRU entries
                if len(self._cache) >= self._max_size:
                    self._evict_lru()
            
            entry = CacheEntry(
                value=value,
                created_at=time.time(),
                ttl_seconds=ttl_seconds
            )
            
            self._cache[key] = entry
    
    def has_key(self, key: str) -> bool:
        """Check if key exists in cache and is not expired."""
        with self._lock:
            if key not in self._cache:
                return False
            
            entry = self._cache[key]
            if entry.is_expired():
                del self._cache[key]
                return False
            
            return True
    
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0
    
    def size(self) -> int:
        """Get current cache size."""
        with self._lock:
            return len(self._cache)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            total_requests = self._hits + self._misses
            hit_rate = (self._hits / total_requests * 100) if total_requests > 0 else 0
            
            return {
                'size': len(self._cache),
                'max_size': self._max_size,
                'hits': self._hits,
                'misses': self._misses,
                'hit_rate_percent': round(hit_rate, 2),
                'default_ttl_seconds': self._default_ttl
            }
    
    def _evict_expired(self) -> None:
        """Remove expired entries from cache."""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self._cache.items()
            if entry.ttl_seconds is not None and current_time - entry.created_at > entry.ttl_seconds
        ]
        
        for key in expired_keys:
            del self._cache[key]
    
    def _evict_lru(self) -> None:
        """Remove least recently used entries to make space."""
        if not self._cache:
            return
        
        # Remove 10% of cache or at least 1 entry
        entries_to_remove = max(1, len(self._cache) // 10)
        
        # Sort by last accessed time (ascending) to get LRU entries
        sorted_entries = sorted(
            self._cache.items(),
            key=lambda x: x[1].last_accessed
        )
        
        for i in range(min(entries_to_remove, len(sorted_entries))):
            key = sorted_entries[i][0]
            del self._cache[key]
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get detailed cache information for debugging."""
        with self._lock:
            entries_info = []
            for key, entry in self._cache.items():
                entries_info.append({
                    'key': key,
                    'created_at': entry.created_at,
                    'ttl_seconds': entry.ttl_seconds,
                    'access_count': entry.access_count,
                    'last_accessed': entry.last_accessed,
                    'is_expired': entry.is_expired()
                })
            
            return {
                'stats': self.get_stats(),
                'entries': entries_info
            }