"""Base service classes and patterns for the unified command line task manager."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Set, TypeVar, Union, Callable
from uuid import UUID

from .exceptions import (
    EntityNotFoundError, ServiceError, ValidationError, 
    AssociationError, ValidationErrorCollection
)
from .models import BaseEntity, BaseLink, StatusManagedEntity, AnnotatedEntity
from .storage import BaseStorageInterface, FilterQuery


# Type variables
EntityType = TypeVar('EntityType', bound=BaseEntity)
LinkType = TypeVar('LinkType', bound=BaseLink)


class ValidationMixin:
    """Mixin providing common validation functionality."""
    
    def validate_required_fields(self, data: Dict[str, Any], required_fields: List[str]) -> None:
        """Validate that required fields are present and not empty."""
        errors = ValidationErrorCollection()
        
        for field in required_fields:
            value = data.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                errors.add_error(field, f"Field '{field}' is required")
        
        errors.raise_if_errors()
    
    def validate_field_values(self, data: Dict[str, Any], 
                            validators: Dict[str, Callable[[Any], bool]],
                            error_messages: Dict[str, str]) -> None:
        """Validate field values using custom validators."""
        errors = ValidationErrorCollection()
        
        for field, validator in validators.items():
            if field in data:
                value = data[field]
                try:
                    if not validator(value):
                        message = error_messages.get(field, f"Invalid value for field '{field}'")
                        errors.add_error(field, message, value)
                except Exception as e:
                    errors.add_error(field, f"Validation error: {str(e)}", value)
        
        errors.raise_if_errors()
    
    def validate_enum_field(self, value: str, enum_class: type, field_name: str) -> None:
        """Validate that a value is valid for an enum class."""
        if hasattr(enum_class, 'is_valid') and not enum_class.is_valid(value):
            valid_values = ', '.join(enum_class.values())
            raise ValidationError(
                f"Invalid {field_name}: {value}. Valid values: {valid_values}",
                field_name, value
            )


class AssociationMixin(Generic[EntityType, LinkType]):
    """Mixin providing entity association management."""
    
    def __init__(self):
        self._association_validators: Dict[str, Callable[[UUID, UUID], bool]] = {}
    
    def register_association_validator(self, link_type: str, 
                                    validator: Callable[[UUID, UUID], bool]) -> None:
        """Register a validator for a specific link type."""
        self._association_validators[link_type] = validator
    
    def create_association(self, source_id: UUID, target_id: UUID, link_type: str,
                         link_storage: BaseStorageInterface[LinkType],
                         link_class: type, metadata: Optional[Dict[str, Any]] = None) -> LinkType:
        """Create an association between two entities."""
        # Validate the association if validator is registered
        if link_type in self._association_validators:
            validator = self._association_validators[link_type]
            if not validator(source_id, target_id):
                raise AssociationError(
                    "Entity", "Entity", "create",
                    f"Association validation failed for link type '{link_type}'"
                )
        
        # Create the link
        link_data = {
            "source_id": source_id,
            "target_id": target_id,
            "link_type": link_type,
            "metadata": metadata or {}
        }
        
        link = link_class(**link_data)
        link_storage.create(link)
        return link
    
    def remove_association(self, source_id: UUID, target_id: UUID, link_type: str,
                         link_storage: BaseStorageInterface[LinkType]) -> bool:
        """Remove an association between two entities."""
        query = FilterQuery().filter_by(
            source_id=source_id,
            target_id=target_id,
            link_type=link_type
        )
        
        links = link_storage.list(query)
        removed_count = 0
        
        for link in links:
            if link_storage.delete(link.id):
                removed_count += 1
        
        return removed_count > 0
    
    def get_associated_entities(self, entity_id: UUID, link_type: str,
                              link_storage: BaseStorageInterface[LinkType],
                              target_storage: BaseStorageInterface[EntityType],
                              direction: str = "outgoing") -> List[EntityType]:
        """Get entities associated with a given entity."""
        if direction == "outgoing":
            query = FilterQuery().filter_by(source_id=entity_id, link_type=link_type)
        elif direction == "incoming":
            query = FilterQuery().filter_by(target_id=entity_id, link_type=link_type)
        else:
            raise ValueError("Direction must be 'outgoing' or 'incoming'")
        
        links = link_storage.list(query)
        
        # Get target entities
        target_ids = []
        for link in links:
            target_id = link.target_id if direction == "outgoing" else link.source_id
            target_ids.append(target_id)
        
        # Fetch target entities
        entities = []
        for target_id in target_ids:
            entity = target_storage.get(target_id)
            if entity:
                entities.append(entity)
        
        return entities


class BaseService(ValidationMixin, AssociationMixin, Generic[EntityType]):
    """Base service class providing common CRUD operations and patterns."""
    
    def __init__(self, storage: BaseStorageInterface[EntityType], entity_type_name: str):
        ValidationMixin.__init__(self)
        AssociationMixin.__init__(self)
        self._storage = storage
        self._entity_type_name = entity_type_name
        self._create_hooks: List[Callable[[EntityType], None]] = []
        self._update_hooks: List[Callable[[EntityType, EntityType], None]] = []
        self._delete_hooks: List[Callable[[UUID], None]] = []
    
    # Hook registration methods
    def register_create_hook(self, hook: Callable[[EntityType], None]) -> None:
        """Register a hook to be called after entity creation."""
        self._create_hooks.append(hook)
    
    def register_update_hook(self, hook: Callable[[EntityType, EntityType], None]) -> None:
        """Register a hook to be called after entity update (old, new)."""
        self._update_hooks.append(hook)
    
    def register_delete_hook(self, hook: Callable[[UUID], None]) -> None:
        """Register a hook to be called after entity deletion."""
        self._delete_hooks.append(hook)
    
    # Core CRUD operations
    def create(self, entity_data: Dict[str, Any], entity_class: type) -> EntityType:
        """Create a new entity."""
        try:
            # Perform pre-creation validation
            self._validate_create_data(entity_data)
            
            # Create the entity
            entity = entity_class(**entity_data)
            entity_id = self._storage.create(entity)
            
            # Run create hooks
            for hook in self._create_hooks:
                try:
                    hook(entity)
                except Exception as e:
                    # Log hook failure but don't fail the operation
                    pass
            
            return entity
            
        except Exception as e:
            raise ServiceError(self._entity_type_name, "create", str(e))
    
    def get(self, entity_id: UUID) -> Optional[EntityType]:
        """Get an entity by ID."""
        try:
            return self._storage.get(entity_id)
        except Exception as e:
            raise ServiceError(self._entity_type_name, "get", str(e))
    
    def get_or_raise(self, entity_id: UUID) -> EntityType:
        """Get an entity by ID or raise EntityNotFoundError."""
        entity = self.get(entity_id)
        if entity is None:
            raise EntityNotFoundError(self._entity_type_name, str(entity_id))
        return entity
    
    def update(self, entity_id: UUID, update_data: Dict[str, Any]) -> bool:
        """Update an entity."""
        try:
            # Get the existing entity
            old_entity = self.get_or_raise(entity_id)
            
            # Validate update data
            self._validate_update_data(update_data, old_entity)
            
            # Create updated entity
            updated_entity = old_entity.model_copy()
            updated_entity.update(**update_data)
            
            # Update in storage
            success = self._storage.update(updated_entity)
            
            if success:
                # Run update hooks
                for hook in self._update_hooks:
                    try:
                        hook(old_entity, updated_entity)
                    except Exception as e:
                        # Log hook failure but don't fail the operation
                        pass
            
            return success
            
        except EntityNotFoundError:
            raise
        except Exception as e:
            raise ServiceError(self._entity_type_name, "update", str(e))
    
    def delete(self, entity_id: UUID) -> bool:
        """Delete an entity."""
        try:
            # Check if entity exists
            if not self._storage.exists(entity_id):
                return False
            
            # Perform pre-deletion validation
            self._validate_delete(entity_id)
            
            # Delete the entity
            success = self._storage.delete(entity_id)
            
            if success:
                # Run delete hooks
                for hook in self._delete_hooks:
                    try:
                        hook(entity_id)
                    except Exception as e:
                        # Log hook failure but don't fail the operation
                        pass
            
            return success
            
        except Exception as e:
            raise ServiceError(self._entity_type_name, "delete", str(e))
    
    def list(self, filters: Optional[Dict[str, Any]] = None,
            sort_by: str = "created_at", sort_reverse: bool = True,
            limit: Optional[int] = None, offset: int = 0) -> List[EntityType]:
        """List entities with optional filtering and pagination."""
        try:
            query = FilterQuery()
            
            if filters:
                query.filter_by(**filters)
            
            query.sort(sort_by, sort_reverse)
            
            if limit is not None:
                query.paginate(limit, offset)
            
            return self._storage.list(query)
            
        except Exception as e:
            raise ServiceError(self._entity_type_name, "list", str(e))
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count entities matching the filters."""
        try:
            query = FilterQuery()
            if filters:
                query.filter_by(**filters)
            
            return self._storage.count(query)
            
        except Exception as e:
            raise ServiceError(self._entity_type_name, "count", str(e))
    
    def exists(self, entity_id: UUID) -> bool:
        """Check if an entity exists."""
        try:
            return self._storage.exists(entity_id)
        except Exception as e:
            raise ServiceError(self._entity_type_name, "exists", str(e))
    
    # Tag management
    def add_tag(self, entity_id: UUID, tag: str) -> bool:
        """Add a tag to an entity."""
        entity = self.get_or_raise(entity_id)
        entity.add_tag(tag)
        return self._storage.update(entity)
    
    def remove_tag(self, entity_id: UUID, tag: str) -> bool:
        """Remove a tag from an entity."""
        entity = self.get_or_raise(entity_id)
        entity.remove_tag(tag)
        return self._storage.update(entity)
    
    def find_by_tags(self, tags: Set[str]) -> List[EntityType]:
        """Find entities with all specified tags."""
        query = FilterQuery().filter_by(tags=tags)
        return self._storage.list(query)
    
    # Note management
    def add_note(self, entity_id: UUID, note: str) -> bool:
        """Add a note to an entity."""
        entity = self.get_or_raise(entity_id)
        entity.add_note(note)
        return self._storage.update(entity)
    
    # Custom metadata management
    def update_metadata(self, entity_id: UUID, key: str, 
                       value: Union[str, int, float, bool, list, dict]) -> bool:
        """Update custom metadata for an entity."""
        entity = self.get_or_raise(entity_id)
        entity.update_custom_metadata(key, value)
        return self._storage.update(entity)
    
    # Validation hooks (to be overridden by subclasses)
    def _validate_create_data(self, data: Dict[str, Any]) -> None:
        """Validate data before entity creation. Override in subclasses."""
        pass
    
    def _validate_update_data(self, data: Dict[str, Any], existing_entity: EntityType) -> None:
        """Validate data before entity update. Override in subclasses."""
        pass
    
    def _validate_delete(self, entity_id: UUID) -> None:
        """Validate before entity deletion. Override in subclasses."""
        pass
    
    # Bulk operations
    def bulk_create(self, entities_data: List[Dict[str, Any]], entity_class: type) -> List[EntityType]:
        """Create multiple entities in bulk."""
        created_entities = []
        errors = []
        
        for i, entity_data in enumerate(entities_data):
            try:
                entity = self.create(entity_data, entity_class)
                created_entities.append(entity)
            except Exception as e:
                errors.append(f"Entity {i}: {str(e)}")
        
        if errors:
            error_summary = "; ".join(errors)
            raise ServiceError(self._entity_type_name, "bulk_create", 
                             f"Failed to create {len(errors)} entities: {error_summary}")
        
        return created_entities
    
    def bulk_update(self, updates: List[Dict[str, Any]]) -> int:
        """Update multiple entities in bulk. Each update dict must contain 'id' field."""
        updated_count = 0
        errors = []
        
        for update_data in updates:
            if 'id' not in update_data:
                errors.append("Update data missing 'id' field")
                continue
            
            entity_id = update_data.pop('id')
            try:
                if self.update(entity_id, update_data):
                    updated_count += 1
            except Exception as e:
                errors.append(f"Entity {entity_id}: {str(e)}")
        
        if errors:
            error_summary = "; ".join(errors)
            raise ServiceError(self._entity_type_name, "bulk_update",
                             f"Failed to update some entities: {error_summary}")
        
        return updated_count


class StatusManagedService(BaseService[StatusManagedEntity]):
    """Service for entities with status management capabilities."""
    
    def __init__(self, storage: BaseStorageInterface[StatusManagedEntity], entity_type_name: str):
        super().__init__(storage, entity_type_name)
        self._status_validators: Dict[str, Callable[[str, str], bool]] = {}
        self._status_transition_hooks: Dict[str, List[Callable[[StatusManagedEntity, str, str], None]]] = {}
    
    def register_status_validator(self, from_status: str, to_status: str, 
                                validator: Callable[[str, str], bool]) -> None:
        """Register a validator for status transitions."""
        key = f"{from_status}->{to_status}"
        self._status_validators[key] = validator
    
    def register_status_transition_hook(self, from_status: str, to_status: str,
                                      hook: Callable[[StatusManagedEntity, str, str], None]) -> None:
        """Register a hook to be called on specific status transitions."""
        key = f"{from_status}->{to_status}"
        if key not in self._status_transition_hooks:
            self._status_transition_hooks[key] = []
        self._status_transition_hooks[key].append(hook)
    
    def update_status(self, entity_id: UUID, new_status: str, user: Optional[str] = None,
                     note: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Update entity status with validation and hooks."""
        entity = self.get_or_raise(entity_id)
        old_status = entity.status
        
        # Validate status transition
        transition_key = f"{old_status}->{new_status}"
        if transition_key in self._status_validators:
            validator = self._status_validators[transition_key]
            if not validator(old_status, new_status):
                raise ValidationError(
                    f"Invalid status transition from '{old_status}' to '{new_status}'"
                )
        
        # Update status
        entity.update_status(new_status, user, note, metadata)
        success = self._storage.update(entity)
        
        if success:
            # Run transition hooks
            if transition_key in self._status_transition_hooks:
                for hook in self._status_transition_hooks[transition_key]:
                    try:
                        hook(entity, old_status, new_status)
                    except Exception:
                        # Log hook failure but don't fail the operation
                        pass
        
        return success
    
    def get_by_status(self, status: str) -> List[StatusManagedEntity]:
        """Get all entities with a specific status."""
        return self.list(filters={"status": status})
    
    def get_by_statuses(self, statuses: List[str]) -> List[StatusManagedEntity]:
        """Get all entities with any of the specified statuses."""
        return self.list(filters={"status": statuses})
    
    def get_status_history(self, entity_id: UUID, limit: Optional[int] = None) -> List:
        """Get status change history for an entity."""
        entity = self.get_or_raise(entity_id)
        return entity.get_status_history(limit)


class AnnotationService(BaseService[AnnotatedEntity]):
    """Service for entities with annotation capabilities."""
    
    def add_annotation(self, entity_id: UUID, content: str, author: Optional[str] = None,
                      annotation_type: str = "note", 
                      metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Add an annotation to an entity."""
        entity = self.get_or_raise(entity_id)
        entity.add_annotation(content, author, annotation_type, metadata)
        return self._storage.update(entity)
    
    def remove_annotation(self, entity_id: UUID, annotation_id: UUID) -> bool:
        """Remove an annotation from an entity."""
        entity = self.get_or_raise(entity_id)
        if entity.remove_annotation(annotation_id):
            return self._storage.update(entity)
        return False
    
    def get_annotations(self, entity_id: UUID, annotation_type: Optional[str] = None,
                       author: Optional[str] = None, limit: Optional[int] = None) -> List:
        """Get annotations for an entity."""
        entity = self.get_or_raise(entity_id)
        return entity.get_annotations(annotation_type, author, limit)
    
    def find_by_annotation_content(self, search_term: str, 
                                 annotation_type: Optional[str] = None) -> List[AnnotatedEntity]:
        """Find entities by annotation content."""
        all_entities = self.list()
        matching_entities = []
        
        for entity in all_entities:
            annotations = entity.get_annotations(annotation_type)
            for annotation in annotations:
                if search_term.lower() in annotation.content.lower():
                    matching_entities.append(entity)
                    break  # Only add entity once even if multiple annotations match
        
        return matching_entities


class AssociationService(BaseService[BaseLink]):
    """Service for managing entity associations."""
    
    def __init__(self, storage: BaseStorageInterface[BaseLink]):
        super().__init__(storage, "Association")
    
    def create_association(self, source_id: UUID, target_id: UUID, link_type: str,
                         metadata: Optional[Dict[str, Any]] = None) -> BaseLink:
        """Create an association between two entities."""
        link_data = {
            "source_id": source_id,
            "target_id": target_id,
            "link_type": link_type,
            "metadata": metadata or {}
        }
        return self.create(link_data, BaseLink)
    
    def remove_association(self, source_id: UUID, target_id: UUID, link_type: str) -> bool:
        """Remove an association between two entities."""
        query = FilterQuery().filter_by(
            source_id=source_id,
            target_id=target_id,
            link_type=link_type
        )
        
        links = self._storage.list(query)
        for link in links:
            if self.delete(link.id):
                return True
        return False
    
    def get_outgoing_associations(self, source_id: UUID, 
                                link_type: Optional[str] = None) -> List[BaseLink]:
        """Get all outgoing associations for an entity."""
        filters = {"source_id": source_id}
        if link_type:
            filters["link_type"] = link_type
        return self.list(filters=filters)
    
    def get_incoming_associations(self, target_id: UUID,
                                link_type: Optional[str] = None) -> List[BaseLink]:
        """Get all incoming associations for an entity."""
        filters = {"target_id": target_id}
        if link_type:
            filters["link_type"] = link_type
        return self.list(filters=filters)
    
    def get_bidirectional_associations(self, entity_id: UUID,
                                     link_type: Optional[str] = None) -> List[BaseLink]:
        """Get all associations (incoming and outgoing) for an entity."""
        outgoing = self.get_outgoing_associations(entity_id, link_type)
        incoming = self.get_incoming_associations(entity_id, link_type)
        
        # Combine and deduplicate
        all_links = {link.id: link for link in outgoing + incoming}
        return list(all_links.values())
    
    def get_associated_entity_ids(self, entity_id: UUID, link_type: str,
                                direction: str = "outgoing") -> List[UUID]:
        """Get IDs of entities associated with a given entity."""
        if direction == "outgoing":
            links = self.get_outgoing_associations(entity_id, link_type)
            return [link.target_id for link in links]
        elif direction == "incoming":
            links = self.get_incoming_associations(entity_id, link_type)
            return [link.source_id for link in links]
        else:
            raise ValueError("Direction must be 'outgoing' or 'incoming'")


class CombinedEntityService(StatusManagedService, AnnotationService):
    """Service combining status management and annotation capabilities."""
    
    def update_status_with_annotation(self, entity_id: UUID, new_status: str,
                                    user: Optional[str] = None, note: Optional[str] = None,
                                    metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Update status and automatically add an annotation."""
        entity = self.get_or_raise(entity_id)
        
        # Ensure entity supports both status and annotations
        if not hasattr(entity, 'update_status_with_annotation'):
            # Fallback to separate operations
            status_success = self.update_status(entity_id, new_status, user, note, metadata)
            if status_success and note:
                self.add_annotation(entity_id, f"Status update: {note}", user, "status_change")
            return status_success
        
        # Use entity's combined method
        old_status = entity.status
        entity.update_status_with_annotation(new_status, user, note, metadata)
        return self._storage.update(entity)