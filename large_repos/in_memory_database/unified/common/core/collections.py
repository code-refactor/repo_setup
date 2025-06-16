"""
Collection classes for the unified in-memory database library.

This module provides common collection types that can be shared across both
vectordb and syncdb implementations.
"""

import threading
import time
from typing import Any, Dict, List, Optional, Iterator, Tuple, Generic, TypeVar
from collections import OrderedDict, defaultdict
from .base import ThreadSafeMixin, TimestampedMixin, SerializableMixin

K = TypeVar('K')
V = TypeVar('V')


class ThreadSafeDict(ThreadSafeMixin, Generic[K, V]):
    """Thread-safe dictionary implementation."""
    
    def __init__(self, initial_data: Optional[Dict[K, V]] = None):
        super().__init__()
        self._data = initial_data or {}
    
    def __getitem__(self, key: K) -> V:
        with self._lock:
            return self._data[key]
    
    def __setitem__(self, key: K, value: V):
        with self._lock:
            self._data[key] = value
    
    def __delitem__(self, key: K):
        with self._lock:
            del self._data[key]
    
    def __contains__(self, key: K) -> bool:
        with self._lock:
            return key in self._data
    
    def __len__(self) -> int:
        with self._lock:
            return len(self._data)
    
    def __iter__(self) -> Iterator[K]:
        with self._lock:
            return iter(list(self._data.keys()))
    
    def get(self, key: K, default: V = None) -> V:
        with self._lock:
            return self._data.get(key, default)
    
    def pop(self, key: K, default: V = None) -> V:
        with self._lock:
            return self._data.pop(key, default)
    
    def update(self, other: Dict[K, V]):
        with self._lock:
            self._data.update(other)
    
    def keys(self) -> List[K]:
        with self._lock:
            return list(self._data.keys())
    
    def values(self) -> List[V]:
        with self._lock:
            return list(self._data.values())
    
    def items(self) -> List[Tuple[K, V]]:
        with self._lock:
            return list(self._data.items())
    
    def clear(self):
        with self._lock:
            self._data.clear()
    
    def copy(self) -> Dict[K, V]:
        with self._lock:
            return self._data.copy()


class LRUCache(ThreadSafeMixin, Generic[K, V]):
    """Least Recently Used cache implementation."""
    
    def __init__(self, max_size: int):
        super().__init__()
        if max_size <= 0:
            raise ValueError("max_size must be positive")
        self._max_size = max_size
        self._cache = OrderedDict()
        self._hits = 0
        self._misses = 0
    
    def __getitem__(self, key: K) -> V:
        with self._lock:
            if key in self._cache:
                # Move to end (most recently used)
                self._cache.move_to_end(key)
                self._hits += 1
                return self._cache[key]
            else:
                self._misses += 1
                raise KeyError(key)
    
    def __setitem__(self, key: K, value: V):
        with self._lock:
            if key in self._cache:
                # Update existing item and move to end
                self._cache[key] = value
                self._cache.move_to_end(key)
            else:
                # Add new item
                self._cache[key] = value
                if len(self._cache) > self._max_size:
                    # Remove least recently used item
                    self._cache.popitem(last=False)
    
    def __delitem__(self, key: K):
        with self._lock:
            del self._cache[key]
    
    def __contains__(self, key: K) -> bool:
        with self._lock:
            return key in self._cache
    
    def __len__(self) -> int:
        with self._lock:
            return len(self._cache)
    
    def get(self, key: K, default: V = None) -> V:
        try:
            return self[key]
        except KeyError:
            return default
    
    def clear(self):
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            total_requests = self._hits + self._misses
            hit_ratio = self._hits / total_requests if total_requests > 0 else 0.0
            return {
                'size': len(self._cache),
                'max_size': self._max_size,
                'hits': self._hits,
                'misses': self._misses,
                'hit_ratio': hit_ratio
            }


class TimestampedCollection(TimestampedMixin, ThreadSafeMixin, Generic[V]):
    """Collection with automatic timestamping."""
    
    def __init__(self):
        super().__init__()
        self._items: List[Tuple[float, V]] = []
    
    def add(self, item: V) -> float:
        """Add item with current timestamp."""
        timestamp = time.time()
        with self._lock:
            self._items.append((timestamp, item))
            self._touch()
        return timestamp
    
    def get_items_since(self, since_timestamp: float) -> List[Tuple[float, V]]:
        """Get items added since specified timestamp."""
        with self._lock:
            return [(ts, item) for ts, item in self._items if ts > since_timestamp]
    
    def get_items_between(self, start_timestamp: float, 
                         end_timestamp: float) -> List[Tuple[float, V]]:
        """Get items added between timestamps."""
        with self._lock:
            return [(ts, item) for ts, item in self._items 
                   if start_timestamp <= ts <= end_timestamp]
    
    def get_latest(self, count: int = 1) -> List[Tuple[float, V]]:
        """Get latest items."""
        with self._lock:
            return self._items[-count:] if count <= len(self._items) else self._items
    
    def get_oldest(self, count: int = 1) -> List[Tuple[float, V]]:
        """Get oldest items."""
        with self._lock:
            return self._items[:count]
    
    def remove_older_than(self, timestamp: float) -> int:
        """Remove items older than timestamp. Returns count of removed items."""
        with self._lock:
            original_count = len(self._items)
            self._items = [(ts, item) for ts, item in self._items if ts >= timestamp]
            removed_count = original_count - len(self._items)
            if removed_count > 0:
                self._touch()
            return removed_count
    
    def clear(self):
        """Clear all items."""
        with self._lock:
            self._items.clear()
            self._touch()
    
    def __len__(self) -> int:
        with self._lock:
            return len(self._items)
    
    def is_empty(self) -> bool:
        with self._lock:
            return len(self._items) == 0


class VersionedContainer(SerializableMixin, TimestampedMixin, ThreadSafeMixin, Generic[V]):
    """Container with version tracking."""
    
    def __init__(self, initial_value: V = None, max_versions: int = 10):
        super().__init__()
        self._max_versions = max_versions
        self._current_version = 0
        self._versions: Dict[int, Tuple[float, V]] = {}
        if initial_value is not None:
            self.set(initial_value)
    
    def set(self, value: V) -> int:
        """Set new value and return version number."""
        with self._lock:
            self._current_version += 1
            timestamp = time.time()
            self._versions[self._current_version] = (timestamp, value)
            
            # Remove old versions if we exceed max_versions
            if len(self._versions) > self._max_versions:
                oldest_version = min(self._versions.keys())
                del self._versions[oldest_version]
            
            self._touch()
            return self._current_version
    
    def get(self, version: Optional[int] = None) -> V:
        """Get value at specified version (latest if None)."""
        with self._lock:
            if version is None:
                version = self._current_version
            
            if version not in self._versions:
                raise ValueError(f"Version {version} not found")
            
            return self._versions[version][1]
    
    def get_with_timestamp(self, version: Optional[int] = None) -> Tuple[float, V]:
        """Get value and timestamp at specified version."""
        with self._lock:
            if version is None:
                version = self._current_version
            
            if version not in self._versions:
                raise ValueError(f"Version {version} not found")
            
            return self._versions[version]
    
    def get_current_version(self) -> int:
        """Get current version number."""
        with self._lock:
            return self._current_version
    
    def get_version_history(self) -> List[int]:
        """Get list of available version numbers."""
        with self._lock:
            return sorted(self._versions.keys())
    
    def has_version(self, version: int) -> bool:
        """Check if version exists."""
        with self._lock:
            return version in self._versions
    
    def get_version_at_time(self, timestamp: float) -> Optional[int]:
        """Get latest version at or before specified timestamp."""
        with self._lock:
            candidates = []
            for version, (ts, _) in self._versions.items():
                if ts <= timestamp:
                    candidates.append((version, ts))
            
            if not candidates:
                return None
            
            # Return version with latest timestamp
            return max(candidates, key=lambda x: x[1])[0]


class CircularBuffer(ThreadSafeMixin, Generic[V]):
    """Fixed-size circular buffer."""
    
    def __init__(self, max_size: int):
        super().__init__()
        if max_size <= 0:
            raise ValueError("max_size must be positive")
        self._max_size = max_size
        self._buffer: List[Optional[V]] = [None] * max_size
        self._head = 0
        self._size = 0
    
    def append(self, item: V):
        """Add item to buffer."""
        with self._lock:
            self._buffer[self._head] = item
            self._head = (self._head + 1) % self._max_size
            if self._size < self._max_size:
                self._size += 1
    
    def get_all(self) -> List[V]:
        """Get all items in order (oldest to newest)."""
        with self._lock:
            if self._size == 0:
                return []
            
            if self._size < self._max_size:
                # Buffer not full yet
                return [item for item in self._buffer[:self._size] if item is not None]
            else:
                # Buffer is full, need to handle wrap-around
                return ([item for item in self._buffer[self._head:] if item is not None] +
                       [item for item in self._buffer[:self._head] if item is not None])
    
    def get_latest(self, count: int = 1) -> List[V]:
        """Get latest items."""
        all_items = self.get_all()
        return all_items[-count:] if count <= len(all_items) else all_items
    
    def is_full(self) -> bool:
        """Check if buffer is full."""
        with self._lock:
            return self._size == self._max_size
    
    def clear(self):
        """Clear all items."""
        with self._lock:
            self._buffer = [None] * self._max_size
            self._head = 0
            self._size = 0
    
    def __len__(self) -> int:
        with self._lock:
            return self._size


class CountingDict(ThreadSafeMixin, Generic[K]):
    """Dictionary that counts occurrences of keys."""
    
    def __init__(self):
        super().__init__()
        self._counts: Dict[K, int] = defaultdict(int)
    
    def increment(self, key: K, count: int = 1):
        """Increment count for key."""
        with self._lock:
            self._counts[key] += count
    
    def decrement(self, key: K, count: int = 1):
        """Decrement count for key."""
        with self._lock:
            self._counts[key] -= count
            if self._counts[key] <= 0:
                del self._counts[key]
    
    def get_count(self, key: K) -> int:
        """Get count for key."""
        with self._lock:
            return self._counts.get(key, 0)
    
    def get_total(self) -> int:
        """Get total count across all keys."""
        with self._lock:
            return sum(self._counts.values())
    
    def get_most_common(self, n: int = None) -> List[Tuple[K, int]]:
        """Get most common keys and their counts."""
        with self._lock:
            sorted_items = sorted(self._counts.items(), key=lambda x: x[1], reverse=True)
            return sorted_items[:n] if n is not None else sorted_items
    
    def clear(self):
        """Clear all counts."""
        with self._lock:
            self._counts.clear()
    
    def keys(self) -> List[K]:
        """Get all keys."""
        with self._lock:
            return list(self._counts.keys())
    
    def items(self) -> List[Tuple[K, int]]:
        """Get all key-count pairs."""
        with self._lock:
            return list(self._counts.items())
    
    def __len__(self) -> int:
        with self._lock:
            return len(self._counts)