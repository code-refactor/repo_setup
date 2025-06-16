"""
Storage and persistence layer for the unified personal knowledge management library.
"""

import json
import os
import shutil
from abc import ABC, abstractmethod
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from uuid import UUID

from .models import BaseKnowledgeNode

T = TypeVar('T', bound=BaseKnowledgeNode)


class BaseStorage(ABC):
    """Abstract base class for storage implementations."""
    
    @abstractmethod
    def save(self, item: T) -> T:
        """Save an item to storage."""
        pass
    
    @abstractmethod
    def get(self, model_type: Type[T], item_id: UUID) -> Optional[T]:
        """Retrieve an item by ID."""
        pass
    
    @abstractmethod
    def get_all(self, model_type: Type[T]) -> List[T]:
        """Retrieve all items of a given type."""
        pass
    
    @abstractmethod
    def query(self, model_type: Type[T], **filters) -> List[T]:
        """Query items with filters."""
        pass
    
    @abstractmethod
    def delete(self, model_type: Type[T], item_id: UUID) -> bool:
        """Delete an item."""
        pass
    
    @abstractmethod
    def count(self, model_type: Type[T]) -> int:
        """Count items of a given type."""
        pass


class CacheManager:
    """Thread-safe in-memory cache with TTL support."""
    
    def __init__(self, default_ttl: int = 3600):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._timestamps: Dict[str, datetime] = {}
        self._lock = Lock()
        self.default_ttl = default_ttl
    
    def _is_expired(self, key: str) -> bool:
        """Check if cache entry is expired."""
        if key not in self._timestamps:
            return True
        return datetime.now() - self._timestamps[key] > timedelta(seconds=self.default_ttl)
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get value from cache."""
        with self._lock:
            if key in self._cache and not self._is_expired(key):
                return self._cache[key]
            return None
    
    def set(self, key: str, value: Dict[str, Any]) -> None:
        """Set value in cache."""
        with self._lock:
            self._cache[key] = value
            self._timestamps[key] = datetime.now()
    
    def delete(self, key: str) -> None:
        """Delete value from cache."""
        with self._lock:
            self._cache.pop(key, None)
            self._timestamps.pop(key, None)
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
            self._timestamps.clear()
    
    def cleanup_expired(self) -> None:
        """Remove expired entries from cache."""
        with self._lock:
            expired_keys = [key for key in self._cache if self._is_expired(key)]
            for key in expired_keys:
                self._cache.pop(key, None)
                self._timestamps.pop(key, None)


class FileStorage(BaseStorage):
    """
    File-based storage implementation with JSON serialization and caching.
    """
    
    def __init__(self, base_path: Union[str, Path], enable_cache: bool = True, cache_ttl: int = 3600):
        self.base_path = Path(base_path)
        self.enable_cache = enable_cache
        self.cache = CacheManager(cache_ttl) if enable_cache else None
        self._lock = Lock()
        
        # Create base directory if it doesn't exist
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def _get_type_dir(self, model_type: Type[T]) -> Path:
        """Get directory for a specific model type."""
        type_dir = self.base_path / model_type.__name__.lower()
        type_dir.mkdir(exist_ok=True)
        return type_dir
    
    def _get_file_path(self, model_type: Type[T], item_id: UUID) -> Path:
        """Get file path for a specific item."""
        type_dir = self._get_type_dir(model_type)
        return type_dir / f"{item_id}.json"
    
    def _cache_key(self, model_type: Type[T], item_id: UUID) -> str:
        """Generate cache key for an item."""
        return f"{model_type.__name__}:{item_id}"
    
    def _serialize_item(self, item: T) -> Dict[str, Any]:
        """Serialize item to dictionary."""
        data = item.model_dump()
        # Convert UUID fields to strings for JSON serialization
        for key, value in data.items():
            if isinstance(value, UUID):
                data[key] = str(value)
            elif isinstance(value, set):
                data[key] = list(value)
            elif isinstance(value, datetime):
                data[key] = value.isoformat()
        return data
    
    def _deserialize_item(self, model_type: Type[T], data: Dict[str, Any]) -> T:
        """Deserialize dictionary to item."""
        # Convert string UUIDs back to UUID objects
        if 'id' in data and isinstance(data['id'], str):
            data['id'] = UUID(data['id'])
        
        # Convert string timestamps back to datetime objects
        for field in ['created_at', 'updated_at', 'started_at', 'completed_at']:
            if field in data and isinstance(data[field], str):
                data[field] = datetime.fromisoformat(data[field])
        
        # Convert list tags back to sets
        if 'tags' in data and isinstance(data['tags'], list):
            data['tags'] = set(data['tags'])
        
        return model_type(**data)
    
    def save(self, item: T) -> T:
        """Save an item to storage."""
        with self._lock:
            file_path = self._get_file_path(type(item), item.id)
            
            # Update timestamp
            item.update_timestamp()
            
            # Serialize and save
            data = self._serialize_item(item)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Update cache
            if self.cache:
                cache_key = self._cache_key(type(item), item.id)
                self.cache.set(cache_key, data)
            
            return item
    
    def get(self, model_type: Type[T], item_id: UUID) -> Optional[T]:
        """Retrieve an item by ID."""
        cache_key = self._cache_key(model_type, item_id)
        
        # Check cache first
        if self.cache:
            cached_data = self.cache.get(cache_key)
            if cached_data:
                return self._deserialize_item(model_type, cached_data)
        
        # Load from file
        file_path = self._get_file_path(model_type, item_id)
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Update cache
            if self.cache:
                self.cache.set(cache_key, data)
            
            return self._deserialize_item(model_type, data)
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            print(f"Error loading item {item_id}: {e}")
            return None
    
    def get_all(self, model_type: Type[T]) -> List[T]:
        """Retrieve all items of a given type."""
        type_dir = self._get_type_dir(model_type)
        items = []
        
        for file_path in type_dir.glob("*.json"):
            try:
                item_id = UUID(file_path.stem)
                item = self.get(model_type, item_id)
                if item:
                    items.append(item)
            except ValueError:
                continue
        
        return items
    
    def query(self, model_type: Type[T], **filters) -> List[T]:
        """Query items with filters."""
        items = self.get_all(model_type)
        filtered_items = []
        
        for item in items:
            match = True
            for key, value in filters.items():
                if not hasattr(item, key):
                    match = False
                    break
                
                item_value = getattr(item, key)
                if isinstance(value, str) and isinstance(item_value, str):
                    # String contains match
                    if value.lower() not in item_value.lower():
                        match = False
                        break
                elif isinstance(value, list):
                    # Value in list
                    if item_value not in value:
                        match = False
                        break
                elif item_value != value:
                    match = False
                    break
            
            if match:
                filtered_items.append(item)
        
        return filtered_items
    
    def delete(self, model_type: Type[T], item_id: UUID) -> bool:
        """Delete an item."""
        with self._lock:
            file_path = self._get_file_path(model_type, item_id)
            
            if file_path.exists():
                file_path.unlink()
                
                # Remove from cache
                if self.cache:
                    cache_key = self._cache_key(model_type, item_id)
                    self.cache.delete(cache_key)
                
                return True
            return False
    
    def count(self, model_type: Type[T]) -> int:
        """Count items of a given type."""
        type_dir = self._get_type_dir(model_type)
        return len(list(type_dir.glob("*.json")))
    
    def search(self, model_type: Type[T], query: str, fields: Optional[List[str]] = None) -> List[T]:
        """Search items by text query."""
        items = self.get_all(model_type)
        results = []
        query_lower = query.lower()
        
        for item in items:
            # Get searchable content
            if hasattr(item, 'get_searchable_content'):
                searchable_content = item.get_searchable_content()
            else:
                # Default: search in title, content, and tags
                searchable_parts = []
                if hasattr(item, 'title'):
                    searchable_parts.append(str(item.title))
                if hasattr(item, 'content') and item.content:
                    searchable_parts.append(str(item.content))
                if hasattr(item, 'tags'):
                    searchable_parts.extend(item.tags)
                searchable_content = " ".join(searchable_parts).lower()
            
            if query_lower in searchable_content:
                results.append(item)
        
        return results
    
    def backup(self, backup_path: Union[str, Path]) -> None:
        """Create a backup of all data."""
        backup_path = Path(backup_path)
        if backup_path.exists():
            shutil.rmtree(backup_path)
        shutil.copytree(self.base_path, backup_path)
    
    def restore(self, backup_path: Union[str, Path]) -> None:
        """Restore data from backup."""
        backup_path = Path(backup_path)
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup path {backup_path} does not exist")
        
        # Clear current data
        if self.base_path.exists():
            shutil.rmtree(self.base_path)
        
        # Restore from backup
        shutil.copytree(backup_path, self.base_path)
        
        # Clear cache
        if self.cache:
            self.cache.clear()


class StorageManager:
    """
    High-level storage manager that provides a unified interface across different storage backends.
    """
    
    def __init__(self, storage: BaseStorage):
        self.storage = storage
        self._executor = ThreadPoolExecutor(max_workers=4)
    
    def save(self, item: T) -> T:
        """Save an item."""
        return self.storage.save(item)
    
    def get(self, model_type: Type[T], item_id: UUID) -> Optional[T]:
        """Get an item by ID."""
        return self.storage.get(model_type, item_id)
    
    def get_all(self, model_type: Type[T]) -> List[T]:
        """Get all items of a type."""
        return self.storage.get_all(model_type)
    
    def query(self, model_type: Type[T], **filters) -> List[T]:
        """Query items with filters."""
        return self.storage.query(model_type, **filters)
    
    def delete(self, model_type: Type[T], item_id: UUID) -> bool:
        """Delete an item."""
        return self.storage.delete(model_type, item_id)
    
    def count(self, model_type: Type[T]) -> int:
        """Count items of a type."""
        return self.storage.count(model_type)
    
    def search(self, model_type: Type[T], query: str) -> List[T]:
        """Search items by text query."""
        if hasattr(self.storage, 'search'):
            return self.storage.search(model_type, query)
        # Fallback to basic filtering
        return []
    
    def bulk_save(self, items: List[T]) -> List[T]:
        """Save multiple items efficiently."""
        if len(items) == 1:
            return [self.save(items[0])]
        
        # Use thread pool for bulk operations
        futures = [self._executor.submit(self.save, item) for item in items]
        return [future.result() for future in futures]
    
    def bulk_delete(self, model_type: Type[T], item_ids: List[UUID]) -> int:
        """Delete multiple items efficiently."""
        if len(item_ids) == 1:
            return int(self.delete(model_type, item_ids[0]))
        
        # Use thread pool for bulk operations
        futures = [self._executor.submit(self.delete, model_type, item_id) for item_id in item_ids]
        return sum(int(future.result()) for future in futures)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get storage statistics."""
        stats = {
            'total_files': 0,
            'types': {}
        }
        
        if hasattr(self.storage, 'base_path'):
            base_path = self.storage.base_path
            for type_dir in base_path.iterdir():
                if type_dir.is_dir():
                    file_count = len(list(type_dir.glob("*.json")))
                    stats['types'][type_dir.name] = file_count
                    stats['total_files'] += file_count
        
        return stats