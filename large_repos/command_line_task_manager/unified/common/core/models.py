"""Base models and entities for the unified command line task manager."""

from abc import ABC
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Union, Any, TypeVar, Generic
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator


class BaseEnum(str, Enum):
    """Base class for string-based enumerations."""
    
    @classmethod
    def values(cls) -> Set[str]:
        """Get all enum values as a set."""
        return {item.value for item in cls}
    
    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Check if a value is valid for this enum."""
        return value in cls.values()


class BaseEntity(BaseModel):
    """Base entity model with common fields and functionality."""
    
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    tags: Set[str] = Field(default_factory=set)
    notes: List[str] = Field(default_factory=list)
    custom_metadata: Dict[str, Union[str, int, float, bool, list, dict]] = Field(
        default_factory=dict
    )
    
    def update(self, **kwargs) -> None:
        """Update entity fields and refresh timestamp."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the entity."""
        self.tags.add(tag)
        self.updated_at = datetime.now()
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the entity."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()
    
    def add_note(self, note: str) -> None:
        """Add a note to the entity."""
        self.notes.append(note)
        self.updated_at = datetime.now()
    
    def update_custom_metadata(self, key: str, value: Union[str, int, float, bool, list, dict]) -> None:
        """Update a custom metadata field."""
        self.custom_metadata[key] = value
        self.updated_at = datetime.now()


class BaseLink(BaseModel):
    """Base model for entity associations/links."""
    
    id: UUID = Field(default_factory=uuid4)
    source_id: UUID
    target_id: UUID
    link_type: str
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def update_metadata(self, key: str, value: Any) -> None:
        """Update link metadata."""
        self.metadata[key] = value


class BaseVersion(BaseModel):
    """Base model for entity versioning."""
    
    id: UUID = Field(default_factory=uuid4)
    entity_id: UUID
    version_number: int
    timestamp: datetime = Field(default_factory=datetime.now)
    changes: Dict[str, Any] = Field(default_factory=dict)
    created_by: Optional[str] = None
    description: Optional[str] = None
    
    def add_change(self, field: str, old_value: Any, new_value: Any) -> None:
        """Record a field change."""
        self.changes[field] = {
            "old": old_value,
            "new": new_value,
            "timestamp": datetime.now()
        }


class StatusChange(BaseModel):
    """Represents a status change event."""
    
    id: UUID = Field(default_factory=uuid4)
    old_status: Optional[str] = None
    new_status: str
    timestamp: datetime = Field(default_factory=datetime.now)
    user: Optional[str] = None
    note: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Annotation(BaseModel):
    """Represents an annotation on an entity."""
    
    id: UUID = Field(default_factory=uuid4)
    content: str
    author: Optional[str] = None
    annotation_type: str = "note"
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('content')
    def content_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Annotation content cannot be empty')
        return v.strip()


class StatusManagedEntity(BaseEntity):
    """Base entity with status management capabilities."""
    
    status: str
    status_history: List[StatusChange] = Field(default_factory=list)
    
    def update_status(self, new_status: str, user: Optional[str] = None, 
                     note: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Update entity status with history tracking."""
        if self.status != new_status:
            status_change = StatusChange(
                old_status=self.status,
                new_status=new_status,
                user=user,
                note=note,
                metadata=metadata or {}
            )
            self.status_history.append(status_change)
            self.status = new_status
            self.updated_at = datetime.now()
    
    def get_status_history(self, limit: Optional[int] = None) -> List[StatusChange]:
        """Get status change history, optionally limited."""
        history = sorted(self.status_history, key=lambda x: x.timestamp, reverse=True)
        return history[:limit] if limit else history
    
    def has_been_status(self, status: str) -> bool:
        """Check if entity has ever been in a specific status."""
        return status == self.status or any(
            change.old_status == status or change.new_status == status
            for change in self.status_history
        )


class AnnotatedEntity(BaseEntity):
    """Base entity with rich annotation capabilities."""
    
    annotations: List[Annotation] = Field(default_factory=list)
    
    def add_annotation(self, content: str, author: Optional[str] = None, 
                      annotation_type: str = "note", 
                      metadata: Optional[Dict[str, Any]] = None) -> Annotation:
        """Add an annotation to the entity."""
        annotation = Annotation(
            content=content,
            author=author,
            annotation_type=annotation_type,
            metadata=metadata or {}
        )
        self.annotations.append(annotation)
        self.updated_at = datetime.now()
        return annotation
    
    def get_annotations(self, annotation_type: Optional[str] = None, 
                       author: Optional[str] = None, 
                       limit: Optional[int] = None) -> List[Annotation]:
        """Get annotations with optional filtering."""
        filtered = self.annotations
        
        if annotation_type:
            filtered = [a for a in filtered if a.annotation_type == annotation_type]
        
        if author:
            filtered = [a for a in filtered if a.author == author]
        
        # Sort by timestamp (newest first)
        filtered = sorted(filtered, key=lambda x: x.timestamp, reverse=True)
        
        return filtered[:limit] if limit else filtered
    
    def remove_annotation(self, annotation_id: UUID) -> bool:
        """Remove an annotation by ID."""
        initial_count = len(self.annotations)
        self.annotations = [a for a in self.annotations if a.id != annotation_id]
        if len(self.annotations) < initial_count:
            self.updated_at = datetime.now()
            return True
        return False


class StatusManagedAnnotatedEntity(StatusManagedEntity, AnnotatedEntity):
    """Entity with both status management and annotation capabilities."""
    
    def update_status_with_annotation(self, new_status: str, user: Optional[str] = None, 
                                    note: Optional[str] = None, 
                                    metadata: Optional[Dict[str, Any]] = None) -> None:
        """Update status and automatically add an annotation."""
        old_status = self.status
        self.update_status(new_status, user, note, metadata)
        
        # Add automatic annotation for status change
        annotation_content = f"Status changed from '{old_status}' to '{new_status}'"
        if note:
            annotation_content += f". Note: {note}"
            
        self.add_annotation(
            content=annotation_content,
            author=user,
            annotation_type="status_change",
            metadata={"old_status": old_status, "new_status": new_status}
        )


# Type variables for generic typing
EntityType = TypeVar('EntityType', bound=BaseEntity)
LinkType = TypeVar('LinkType', bound=BaseLink)


class EntityCollection(Generic[EntityType]):
    """Generic collection for managing entities."""
    
    def __init__(self):
        self._entities: Dict[UUID, EntityType] = {}
        self._tags_index: Dict[str, Set[UUID]] = {}
    
    def add(self, entity: EntityType) -> None:
        """Add an entity to the collection."""
        self._entities[entity.id] = entity
        self._update_tags_index(entity)
    
    def get(self, entity_id: UUID) -> Optional[EntityType]:
        """Get an entity by ID."""
        return self._entities.get(entity_id)
    
    def remove(self, entity_id: UUID) -> bool:
        """Remove an entity from the collection."""
        if entity_id in self._entities:
            entity = self._entities[entity_id]
            self._remove_from_tags_index(entity)
            del self._entities[entity_id]
            return True
        return False
    
    def list_all(self) -> List[EntityType]:
        """Get all entities as a list."""
        return list(self._entities.values())
    
    def find_by_tags(self, tags: Set[str]) -> List[EntityType]:
        """Find entities that have all specified tags."""
        if not tags:
            return self.list_all()
        
        # Find intersection of entity IDs for all tags
        entity_ids = None
        for tag in tags:
            tag_entities = self._tags_index.get(tag, set())
            if entity_ids is None:
                entity_ids = tag_entities.copy()
            else:
                entity_ids &= tag_entities
        
        if entity_ids is None:
            return []
        
        return [self._entities[eid] for eid in entity_ids if eid in self._entities]
    
    def _update_tags_index(self, entity: EntityType) -> None:
        """Update the tags index for an entity."""
        for tag in entity.tags:
            if tag not in self._tags_index:
                self._tags_index[tag] = set()
            self._tags_index[tag].add(entity.id)
    
    def _remove_from_tags_index(self, entity: EntityType) -> None:
        """Remove an entity from the tags index."""
        for tag in entity.tags:
            if tag in self._tags_index:
                self._tags_index[tag].discard(entity.id)
                if not self._tags_index[tag]:
                    del self._tags_index[tag]


class AssociationManager(Generic[LinkType]):
    """Manager for entity associations using link entities."""
    
    def __init__(self):
        self._links: Dict[UUID, LinkType] = {}
        self._source_index: Dict[UUID, Set[UUID]] = {}
        self._target_index: Dict[UUID, Set[UUID]] = {}
    
    def add_link(self, link: LinkType) -> None:
        """Add a link between entities."""
        self._links[link.id] = link
        
        # Update indices
        if link.source_id not in self._source_index:
            self._source_index[link.source_id] = set()
        self._source_index[link.source_id].add(link.id)
        
        if link.target_id not in self._target_index:
            self._target_index[link.target_id] = set()
        self._target_index[link.target_id].add(link.id)
    
    def remove_link(self, link_id: UUID) -> bool:
        """Remove a link by ID."""
        if link_id in self._links:
            link = self._links[link_id]
            
            # Update indices
            self._source_index[link.source_id].discard(link_id)
            self._target_index[link.target_id].discard(link_id)
            
            # Clean up empty index entries
            if not self._source_index[link.source_id]:
                del self._source_index[link.source_id]
            if not self._target_index[link.target_id]:
                del self._target_index[link.target_id]
            
            del self._links[link_id]
            return True
        return False
    
    def get_outgoing_links(self, source_id: UUID) -> List[LinkType]:
        """Get all links originating from a source entity."""
        link_ids = self._source_index.get(source_id, set())
        return [self._links[lid] for lid in link_ids if lid in self._links]
    
    def get_incoming_links(self, target_id: UUID) -> List[LinkType]:
        """Get all links targeting an entity."""
        link_ids = self._target_index.get(target_id, set())
        return [self._links[lid] for lid in link_ids if lid in self._links]
    
    def get_bidirectional_links(self, entity_id: UUID) -> List[LinkType]:
        """Get all links connected to an entity (both incoming and outgoing)."""
        outgoing = self.get_outgoing_links(entity_id)
        incoming = self.get_incoming_links(entity_id)
        
        # Combine and deduplicate
        all_links = {link.id: link for link in outgoing + incoming}
        return list(all_links.values())
    
    def find_links_by_type(self, link_type: str) -> List[LinkType]:
        """Find all links of a specific type."""
        return [link for link in self._links.values() if link.link_type == link_type]