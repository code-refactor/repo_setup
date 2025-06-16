"""Base storage interfaces and implementations for the unified command line task manager."""

import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Set, TypeVar, Union
from uuid import UUID

from .exceptions import EntityNotFoundError, StorageError, ValidationError
from .models import BaseEntity


# Type variable for entities
EntityType = TypeVar('EntityType', bound=BaseEntity)


class FilterQuery:
    """Query builder for filtering entities."""
    
    def __init__(self):
        self.filters: Dict[str, Any] = {}
        self.sort_by: str = "created_at"
        self.sort_reverse: bool = True
        self.limit: Optional[int] = None
        self.offset: int = 0
    
    def filter_by(self, **kwargs) -> 'FilterQuery':
        """Add filters to the query."""
        self.filters.update(kwargs)
        return self
    
    def sort(self, field: str, reverse: bool = False) -> 'FilterQuery':
        """Set sorting parameters."""
        self.sort_by = field
        self.sort_reverse = reverse
        return self
    
    def paginate(self, limit: int, offset: int = 0) -> 'FilterQuery':
        """Set pagination parameters."""
        self.limit = limit
        self.offset = offset
        return self
    
    def matches(self, entity: EntityType) -> bool:
        """Check if an entity matches the filter criteria."""
        for field, expected_value in self.filters.items():
            if not hasattr(entity, field):
                continue
            
            actual_value = getattr(entity, field)
            
            # Handle different filter types
            if isinstance(expected_value, set) and isinstance(actual_value, (set, list)):
                # Set intersection for tags, etc.
                if not expected_value.intersection(set(actual_value)):
                    return False
            elif isinstance(expected_value, list) and len(expected_value) > 0:
                # List contains any of the expected values
                if actual_value not in expected_value:
                    return False
            elif isinstance(expected_value, dict):
                # Complex field matching (e.g., date ranges)
                if not self._match_complex_filter(actual_value, expected_value):
                    return False
            else:
                # Direct equality
                if actual_value != expected_value:
                    return False
        
        return True
    
    def _match_complex_filter(self, actual_value: Any, filter_spec: Dict[str, Any]) -> bool:
        """Handle complex filter matching."""
        if "gte" in filter_spec and actual_value < filter_spec["gte"]:
            return False
        if "lte" in filter_spec and actual_value > filter_spec["lte"]:
            return False
        if "gt" in filter_spec and actual_value <= filter_spec["gt"]:
            return False
        if "lt" in filter_spec and actual_value >= filter_spec["lt"]:
            return False
        if "in" in filter_spec and actual_value not in filter_spec["in"]:
            return False
        if "not_in" in filter_spec and actual_value in filter_spec["not_in"]:
            return False
        
        return True


class BaseStorageInterface(ABC, Generic[EntityType]):
    """Abstract base interface for entity storage."""
    
    @abstractmethod
    def create(self, entity: EntityType) -> UUID:
        """Create a new entity and return its ID."""
        pass
    
    @abstractmethod  
    def get(self, entity_id: UUID) -> Optional[EntityType]:
        """Retrieve an entity by ID."""
        pass
    
    @abstractmethod
    def update(self, entity: EntityType) -> bool:
        """Update an existing entity."""
        pass
    
    @abstractmethod
    def delete(self, entity_id: UUID) -> bool:
        """Delete an entity by ID."""
        pass
    
    @abstractmethod
    def list(self, query: Optional[FilterQuery] = None) -> List[EntityType]:
        """List entities with optional filtering."""
        pass
    
    @abstractmethod
    def count(self, query: Optional[FilterQuery] = None) -> int:
        """Count entities matching the query."""
        pass
    
    @abstractmethod
    def exists(self, entity_id: UUID) -> bool:
        """Check if an entity exists."""
        pass
    
    def get_or_raise(self, entity_id: UUID, entity_type_name: str = "Entity") -> EntityType:
        """Get an entity or raise EntityNotFoundError."""
        entity = self.get(entity_id)
        if entity is None:
            raise EntityNotFoundError(entity_type_name, str(entity_id))
        return entity
    
    def list_ids(self, query: Optional[FilterQuery] = None) -> List[UUID]:
        """List entity IDs matching the query."""
        entities = self.list(query)
        return [entity.id for entity in entities]


class InMemoryStorage(BaseStorageInterface[EntityType]):
    """In-memory storage implementation for entities."""
    
    def __init__(self):
        self._entities: Dict[UUID, EntityType] = {}
        self._entity_type_name: str = "Entity"
    
    def create(self, entity: EntityType) -> UUID:
        """Create a new entity."""
        if entity.id in self._entities:
            raise StorageError("create", f"Entity with ID {entity.id} already exists")
        
        self._entities[entity.id] = entity
        return entity.id
    
    def get(self, entity_id: UUID) -> Optional[EntityType]:
        """Retrieve an entity by ID."""
        return self._entities.get(entity_id)
    
    def update(self, entity: EntityType) -> bool:
        """Update an existing entity."""
        if entity.id not in self._entities:
            return False
        
        # Update the timestamp
        entity.updated_at = datetime.now()
        self._entities[entity.id] = entity
        return True
    
    def delete(self, entity_id: UUID) -> bool:
        """Delete an entity by ID."""
        if entity_id in self._entities:
            del self._entities[entity_id]
            return True
        return False
    
    def list(self, query: Optional[FilterQuery] = None) -> List[EntityType]:
        """List entities with optional filtering."""
        entities = list(self._entities.values())
        
        if query:
            # Apply filters
            if query.filters:
                entities = [entity for entity in entities if query.matches(entity)]
            
            # Apply sorting
            if hasattr(entities[0] if entities else None, query.sort_by):
                entities.sort(
                    key=lambda e: getattr(e, query.sort_by, None),
                    reverse=query.sort_reverse
                )
            
            # Apply pagination
            if query.offset > 0:
                entities = entities[query.offset:]
            if query.limit is not None:
                entities = entities[:query.limit]
        
        return entities
    
    def count(self, query: Optional[FilterQuery] = None) -> int:
        """Count entities matching the query."""
        if query is None or not query.filters:
            return len(self._entities)
        
        return len([entity for entity in self._entities.values() if query.matches(entity)])
    
    def exists(self, entity_id: UUID) -> bool:
        """Check if an entity exists."""
        return entity_id in self._entities
    
    def clear(self) -> None:
        """Clear all entities (useful for testing)."""
        self._entities.clear()
    
    def bulk_create(self, entities: List[EntityType]) -> List[UUID]:
        """Create multiple entities in bulk."""
        created_ids = []
        for entity in entities:
            entity_id = self.create(entity)
            created_ids.append(entity_id)
        return created_ids
    
    def bulk_update(self, entities: List[EntityType]) -> int:
        """Update multiple entities in bulk."""
        updated_count = 0
        for entity in entities:
            if self.update(entity):
                updated_count += 1
        return updated_count
    
    def bulk_delete(self, entity_ids: List[UUID]) -> int:
        """Delete multiple entities in bulk."""
        deleted_count = 0
        for entity_id in entity_ids:
            if self.delete(entity_id):
                deleted_count += 1
        return deleted_count


class JSONSerializableStorage(InMemoryStorage[EntityType]):
    """In-memory storage with JSON serialization support."""
    
    def to_json(self) -> str:
        """Serialize all entities to JSON."""
        data = {
            "entities": {},
            "metadata": {
                "count": len(self._entities),
                "exported_at": datetime.now().isoformat()
            }
        }
        
        for entity_id, entity in self._entities.items():
            data["entities"][str(entity_id)] = self._serialize_entity(entity)
        
        return json.dumps(data, indent=2, default=self._json_serializer)
    
    def from_json(self, json_data: str, entity_class: type) -> None:
        """Load entities from JSON data."""
        try:
            data = json.loads(json_data)
            entities = data.get("entities", {})
            
            self._entities.clear()
            
            for entity_id_str, entity_data in entities.items():
                entity_id = UUID(entity_id_str)
                entity = self._deserialize_entity(entity_data, entity_class)
                self._entities[entity_id] = entity
                
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            raise StorageError("deserialize", f"Failed to load from JSON: {str(e)}")
    
    def _serialize_entity(self, entity: EntityType) -> Dict[str, Any]:
        """Serialize an entity to a dictionary."""
        return entity.model_dump()
    
    def _deserialize_entity(self, data: Dict[str, Any], entity_class: type) -> EntityType:
        """Deserialize a dictionary to an entity."""
        return entity_class(**data)
    
    def _json_serializer(self, obj: Any) -> Any:
        """Custom JSON serializer for complex types."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, set):
            return list(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


class TransactionalStorage(InMemoryStorage[EntityType]):
    """Storage with transaction support for batch operations."""
    
    def __init__(self):
        super().__init__()
        self._transaction_stack: List[Dict[str, Any]] = []
    
    def begin_transaction(self) -> None:
        """Begin a new transaction."""
        # Create a snapshot of current state
        snapshot = {
            "entities": {eid: entity.model_copy() for eid, entity in self._entities.items()}
        }
        self._transaction_stack.append(snapshot)
    
    def commit_transaction(self) -> None:
        """Commit the current transaction."""
        if not self._transaction_stack:
            raise StorageError("commit", "No active transaction to commit")
        
        # Simply remove the snapshot - changes are already applied
        self._transaction_stack.pop()
    
    def rollback_transaction(self) -> None:
        """Rollback the current transaction."""
        if not self._transaction_stack:
            raise StorageError("rollback", "No active transaction to rollback")
        
        # Restore the previous state
        snapshot = self._transaction_stack.pop()
        self._entities = snapshot["entities"]
    
    def has_active_transaction(self) -> bool:
        """Check if there's an active transaction."""
        return len(self._transaction_stack) > 0


class SecureStorage(InMemoryStorage[EntityType]):
    """Storage with optional encryption support."""
    
    def __init__(self, crypto_manager=None):
        super().__init__()
        self._crypto_manager = crypto_manager
        self._encrypted_fields: Set[str] = set()
    
    def register_encrypted_field(self, field_name: str) -> None:
        """Register a field to be encrypted."""
        if self._crypto_manager:
            self._encrypted_fields.add(field_name)
    
    def create(self, entity: EntityType) -> UUID:
        """Create entity with encryption."""
        if self._crypto_manager and self._encrypted_fields:
            entity = self._encrypt_entity(entity)
        return super().create(entity)
    
    def update(self, entity: EntityType) -> bool:
        """Update entity with encryption."""
        if self._crypto_manager and self._encrypted_fields:
            entity = self._encrypt_entity(entity)
        return super().update(entity)
    
    def get(self, entity_id: UUID) -> Optional[EntityType]:
        """Get entity with decryption."""
        entity = super().get(entity_id)
        if entity and self._crypto_manager and self._encrypted_fields:
            entity = self._decrypt_entity(entity)
        return entity
    
    def list(self, query: Optional[FilterQuery] = None) -> List[EntityType]:
        """List entities with decryption."""
        entities = super().list(query)
        if self._crypto_manager and self._encrypted_fields:
            entities = [self._decrypt_entity(entity) for entity in entities]
        return entities
    
    def _encrypt_entity(self, entity: EntityType) -> EntityType:
        """Encrypt specified fields in an entity."""
        if not self._crypto_manager:
            return entity
        
        entity_copy = entity.model_copy()
        entity_dict = entity_copy.model_dump()
        
        for field in self._encrypted_fields:
            if field in entity_dict and entity_dict[field] is not None:
                try:
                    # Convert to string if needed and encrypt
                    value = entity_dict[field]
                    if not isinstance(value, str):
                        import json
                        value = json.dumps(value)
                    
                    encrypted_value = self._crypto_manager.encrypt(value)
                    entity_dict[field] = encrypted_value
                except Exception:
                    # If encryption fails, leave field as-is
                    pass
        
        # Create new entity with encrypted data
        return type(entity)(**entity_dict)
    
    def _decrypt_entity(self, entity: EntityType) -> EntityType:
        """Decrypt specified fields in an entity."""
        if not self._crypto_manager:
            return entity
        
        entity_copy = entity.model_copy()
        entity_dict = entity_copy.model_dump()
        
        for field in self._encrypted_fields:
            if field in entity_dict and entity_dict[field] is not None:
                try:
                    encrypted_value = entity_dict[field]
                    decrypted_value = self._crypto_manager.decrypt(encrypted_value)
                    
                    # Try to parse as JSON, fallback to string
                    try:
                        import json
                        entity_dict[field] = json.loads(decrypted_value)
                    except (json.JSONDecodeError, TypeError):
                        entity_dict[field] = decrypted_value
                except Exception:
                    # If decryption fails, leave field as-is
                    pass
        
        # Create new entity with decrypted data
        return type(entity)(**entity_dict)


class IndexedStorage(InMemoryStorage[EntityType]):
    """Storage with advanced indexing for performance."""
    
    def __init__(self):
        super().__init__()
        self._indices: Dict[str, Dict[Any, Set[UUID]]] = {}
        self._indexed_fields: Set[str] = set()
    
    def create_index(self, field_name: str) -> None:
        """Create an index for a field."""
        if field_name not in self._indexed_fields:
            self._indexed_fields.add(field_name)
            self._indices[field_name] = {}
            
            # Build index for existing entities
            for entity in self._entities.values():
                self._update_index(entity, field_name)
    
    def create(self, entity: EntityType) -> UUID:
        """Create entity and update indices."""
        entity_id = super().create(entity)
        self._update_indices(entity)
        return entity_id
    
    def update(self, entity: EntityType) -> bool:
        """Update entity and indices."""
        old_entity = self._entities.get(entity.id)
        success = super().update(entity)
        
        if success:
            # Remove old entity from indices
            if old_entity:
                self._remove_from_indices(old_entity)
            # Add updated entity to indices
            self._update_indices(entity)
        
        return success
    
    def delete(self, entity_id: UUID) -> bool:
        """Delete entity and update indices."""
        entity = self._entities.get(entity_id)
        success = super().delete(entity_id)
        
        if success and entity:
            self._remove_from_indices(entity)
        
        return success
    
    def list(self, query: Optional[FilterQuery] = None) -> List[EntityType]:
        """Optimized list using indices when possible."""
        if not query or not query.filters:
            return super().list(query)
        
        # Try to use indices for filtering
        candidate_ids = self._get_candidates_from_indices(query.filters)
        
        if candidate_ids is not None:
            # Use index-based filtering
            entities = [self._entities[eid] for eid in candidate_ids if eid in self._entities]
        else:
            # Fall back to full scan
            entities = list(self._entities.values())
        
        # Apply remaining filters and sorting
        if query:
            if query.filters:
                entities = [entity for entity in entities if query.matches(entity)]
            
            # Apply sorting
            if hasattr(entities[0] if entities else None, query.sort_by):
                entities.sort(
                    key=lambda e: getattr(e, query.sort_by, None),
                    reverse=query.sort_reverse
                )
            
            # Apply pagination
            if query.offset > 0:
                entities = entities[query.offset:]
            if query.limit is not None:
                entities = entities[:query.limit]
        
        return entities
    
    def _update_indices(self, entity: EntityType) -> None:
        """Update all indices for an entity."""
        for field_name in self._indexed_fields:
            self._update_index(entity, field_name)
    
    def _update_index(self, entity: EntityType, field_name: str) -> None:
        """Update a specific index for an entity."""
        if not hasattr(entity, field_name):
            return
        
        value = getattr(entity, field_name)
        index = self._indices[field_name]
        
        # Handle different value types
        if isinstance(value, (list, set)):
            # Index each item in the collection
            for item in value:
                if item not in index:
                    index[item] = set()
                index[item].add(entity.id)
        else:
            # Index the value directly
            if value not in index:
                index[value] = set()
            index[value].add(entity.id)
    
    def _remove_from_indices(self, entity: EntityType) -> None:
        """Remove entity from all indices."""
        for field_name in self._indexed_fields:
            self._remove_from_index(entity, field_name)
    
    def _remove_from_index(self, entity: EntityType, field_name: str) -> None:
        """Remove entity from a specific index."""
        if not hasattr(entity, field_name):
            return
        
        value = getattr(entity, field_name)
        index = self._indices[field_name]
        
        # Handle different value types
        if isinstance(value, (list, set)):
            for item in value:
                if item in index:
                    index[item].discard(entity.id)
                    if not index[item]:
                        del index[item]
        else:
            if value in index:
                index[value].discard(entity.id)
                if not index[value]:
                    del index[value]
    
    def _get_candidates_from_indices(self, filters: Dict[str, Any]) -> Optional[Set[UUID]]:
        """Get candidate entity IDs using indices."""
        candidate_sets = []
        
        for field, value in filters.items():
            if field in self._indexed_fields:
                index = self._indices[field]
                
                if isinstance(value, (list, set)):
                    # Union of all matching values
                    field_candidates = set()
                    for v in value:
                        if v in index:
                            field_candidates.update(index[v])
                else:
                    # Direct lookup
                    field_candidates = index.get(value, set())
                
                candidate_sets.append(field_candidates)
        
        if not candidate_sets:
            return None
        
        # Intersection of all candidate sets (AND logic)
        result = candidate_sets[0]
        for candidate_set in candidate_sets[1:]:
            result = result.intersection(candidate_set)
        
        return result


class HybridStorage(SecureStorage[EntityType], IndexedStorage[EntityType]):
    """Storage combining encryption and indexing capabilities."""
    
    def __init__(self, crypto_manager=None):
        SecureStorage.__init__(self, crypto_manager)
        IndexedStorage.__init__(self)
    
    def create(self, entity: EntityType) -> UUID:
        """Create with both encryption and indexing."""
        # Encrypt first, then index
        if self._crypto_manager and self._encrypted_fields:
            entity = self._encrypt_entity(entity)
        entity_id = InMemoryStorage.create(self, entity)
        self._update_indices(entity)
        return entity_id
    
    def update(self, entity: EntityType) -> bool:
        """Update with both encryption and indexing."""
        old_entity = self._entities.get(entity.id)
        
        # Encrypt first
        if self._crypto_manager and self._encrypted_fields:
            entity = self._encrypt_entity(entity)
        
        success = InMemoryStorage.update(self, entity)
        
        if success:
            # Update indices
            if old_entity:
                self._remove_from_indices(old_entity)
            self._update_indices(entity)
        
        return success
    
    def get(self, entity_id: UUID) -> Optional[EntityType]:
        """Get with decryption."""
        entity = InMemoryStorage.get(self, entity_id)
        if entity and self._crypto_manager and self._encrypted_fields:
            entity = self._decrypt_entity(entity)
        return entity
    
    def list(self, query: Optional[FilterQuery] = None) -> List[EntityType]:
        """List with indexing optimization and decryption."""
        # Use IndexedStorage's optimized list
        entities = IndexedStorage.list(self, query)
        
        # Decrypt if needed
        if self._crypto_manager and self._encrypted_fields:
            entities = [self._decrypt_entity(entity) for entity in entities]
        
        return entities