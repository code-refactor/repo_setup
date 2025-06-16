"""
Base data models and common patterns for the unified personal knowledge management library.
"""

from abc import ABC
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Priority(str, Enum):
    """Common priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Status(str, Enum):
    """Common status values."""
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    CANCELLED = "cancelled"


class BaseKnowledgeNode(BaseModel, ABC):
    """
    Base class for all knowledge entities in the system.
    
    Provides common fields and functionality that all entities share:
    - Unique identification
    - Timestamp tracking
    - Tagging system
    - Basic metadata
    """
    
    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    tags: Set[str] = Field(default_factory=set, description="Tags for categorization")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    def update_timestamp(self) -> None:
        """Update the last modified timestamp."""
        self.updated_at = datetime.now()
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to this entity."""
        self.tags.add(tag.strip().lower())
        self.update_timestamp()
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from this entity."""
        self.tags.discard(tag.strip().lower())
        self.update_timestamp()
    
    def has_tag(self, tag: str) -> bool:
        """Check if entity has a specific tag."""
        return tag.strip().lower() in self.tags
    
    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to this entity."""
        self.metadata[key] = value
        self.update_timestamp()
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value by key."""
        return self.metadata.get(key, default)


class BaseRelationship(BaseModel):
    """
    Base class for modeling relationships between entities.
    """
    
    id: UUID = Field(default_factory=uuid4, description="Unique relationship identifier")
    source_id: UUID = Field(description="Source entity identifier")
    target_id: UUID = Field(description="Target entity identifier") 
    relationship_type: str = Field(description="Type of relationship")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Relationship metadata")
    
    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to this relationship."""
        self.metadata[key] = value


class SearchableEntity(BaseKnowledgeNode):
    """
    Extended base class for entities that support full-text search.
    """
    
    title: str = Field(description="Entity title")
    content: Optional[str] = Field(default=None, description="Main content for searching")
    
    def get_searchable_content(self) -> str:
        """Get all searchable text content from this entity."""
        parts = [self.title]
        if self.content:
            parts.append(self.content)
        parts.extend(self.tags)
        return " ".join(parts).lower()


class TimestampedEntity(BaseKnowledgeNode):
    """
    Base class for entities that need detailed timestamp tracking.
    """
    
    started_at: Optional[datetime] = Field(default=None, description="Start timestamp")
    completed_at: Optional[datetime] = Field(default=None, description="Completion timestamp")
    
    def mark_started(self) -> None:
        """Mark entity as started."""
        self.started_at = datetime.now()
        self.update_timestamp()
    
    def mark_completed(self) -> None:
        """Mark entity as completed."""
        self.completed_at = datetime.now()
        self.update_timestamp()
    
    @property
    def is_started(self) -> bool:
        """Check if entity has been started."""
        return self.started_at is not None
    
    @property
    def is_completed(self) -> bool:
        """Check if entity has been completed."""
        return self.completed_at is not None
    
    @property
    def duration(self) -> Optional[float]:
        """Get duration in seconds if both start and end times are set."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None


class Evidence(BaseModel):
    """
    Model for evidence supporting relationships or claims.
    """
    
    class EvidenceType(str, Enum):
        EMPIRICAL = "empirical"
        THEORETICAL = "theoretical"
        ANECDOTAL = "anecdotal"
        STATISTICAL = "statistical"
    
    class EvidenceStrength(str, Enum):
        WEAK = "weak"
        MODERATE = "moderate"
        STRONG = "strong"
        DEFINITIVE = "definitive"
    
    id: UUID = Field(default_factory=uuid4, description="Evidence identifier")
    evidence_type: EvidenceType = Field(description="Type of evidence")
    strength: EvidenceStrength = Field(description="Strength of evidence")
    description: str = Field(description="Evidence description")
    source: Optional[str] = Field(default=None, description="Evidence source")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")


class ConfigurableComponent(BaseModel):
    """
    Base class for components that support configuration.
    """
    
    config: Dict[str, Any] = Field(default_factory=dict, description="Component configuration")
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set_config(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self.config[key] = value
    
    def update_config(self, updates: Dict[str, Any]) -> None:
        """Update multiple configuration values."""
        self.config.update(updates)