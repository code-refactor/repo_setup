from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from common.core.models import BaseEntity, BaseEnum, BaseLink


class CitationStyle(BaseEnum):
    """Supported academic citation styles."""
    
    APA = "apa"  # American Psychological Association
    MLA = "mla"  # Modern Language Association
    CHICAGO = "chicago"  # Chicago Manual of Style
    HARVARD = "harvard"  # Harvard referencing
    IEEE = "ieee"  # Institute of Electrical and Electronics Engineers
    VANCOUVER = "vancouver"  # Vancouver system
    NATURE = "nature"  # Nature journal style
    SCIENCE = "science"  # Science journal style


class AuthorType(BaseEnum):
    """Types of reference authors."""
    
    PERSON = "person"
    ORGANIZATION = "organization"


class ReferenceType(BaseEnum):
    """Types of academic references."""
    
    JOURNAL_ARTICLE = "journal_article"
    BOOK = "book"
    BOOK_CHAPTER = "book_chapter"
    CONFERENCE_PAPER = "conference_paper"
    THESIS = "thesis"
    REPORT = "report"
    WEBSITE = "website"
    PREPRINT = "preprint"
    DATASET = "dataset"
    SOFTWARE = "software"
    OTHER = "other"


class Author(BaseModel):
    """Model representing an author of an academic reference."""
    
    id: UUID = Field(default_factory=uuid4)
    type: AuthorType = AuthorType.PERSON
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    organization_name: Optional[str] = None
    orcid_id: Optional[str] = None
    
    def full_name(self) -> str:
        """
        Get the full name of the author.
        
        Returns:
            str: Full name in the format "Last, First" for persons, or organization name
        """
        if self.type == AuthorType.PERSON:
            if self.first_name and self.last_name:
                return f"{self.last_name}, {self.first_name}"
            elif self.last_name:
                return self.last_name
            elif self.first_name:
                return self.first_name
            else:
                return "Unknown Author"
        else:  # ORGANIZATION
            return self.organization_name or "Unknown Organization"


class Reference(BaseEntity):
    """Model representing an academic reference/citation."""
    
    type: ReferenceType
    authors: List[Author] = Field(default_factory=list)
    title: str
    year: Optional[int] = None
    
    # Journal article specific fields
    journal_name: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    doi: Optional[str] = None
    
    # Book specific fields
    publisher: Optional[str] = None
    isbn: Optional[str] = None
    edition: Optional[str] = None
    
    # Conference paper specific fields
    conference_name: Optional[str] = None
    conference_location: Optional[str] = None
    
    # Website specific fields
    url: Optional[str] = None
    accessed_date: Optional[datetime] = None
    
    # Preprint specific fields
    preprint_server: Optional[str] = None
    preprint_id: Optional[str] = None
    
    # Dataset specific fields
    repository: Optional[str] = None
    dataset_id: Optional[str] = None
    version: Optional[str] = None
    
    # General fields
    abstract: Optional[str] = None
    # keywords -> use inherited tags from BaseEntity
    # notes -> use inherited notes from BaseEntity
    # custom_fields -> use inherited custom_metadata from BaseEntity
    
    def __init__(self, keywords: Optional[Set[str]] = None, custom_fields: Optional[Dict[str, str]] = None, **kwargs):
        # Handle backward compatibility for keywords and custom_fields
        if keywords is not None:
            kwargs['tags'] = keywords
        if custom_fields is not None:
            kwargs['custom_metadata'] = custom_fields
        super().__init__(**kwargs)
    
    # Inherits update() method from BaseEntity
    
    def add_author(self, author: Author) -> None:
        """Add an author to the reference."""
        self.authors.append(author)
        self.updated_at = datetime.now()
    
    def remove_author(self, author_id: UUID) -> bool:
        """
        Remove an author from the reference.
        
        Args:
            author_id: The ID of the author to remove
            
        Returns:
            bool: True if author was removed, False if not found
        """
        original_length = len(self.authors)
        self.authors = [author for author in self.authors if author.id != author_id]
        
        if len(self.authors) < original_length:
            self.updated_at = datetime.now()
            return True
        return False
    
    def add_keyword(self, keyword: str) -> None:
        """Add a keyword to the reference (using inherited tags)."""
        self.add_tag(keyword)
    
    def remove_keyword(self, keyword: str) -> None:
        """Remove a keyword from the reference (using inherited tags)."""
        self.remove_tag(keyword)
    
    @property
    def keywords(self) -> Set[str]:
        """Get keywords (alias for tags for backward compatibility)."""
        return self.tags
    
    @keywords.setter
    def keywords(self, value: Set[str]) -> None:
        """Set keywords (alias for tags for backward compatibility)."""
        self.tags = value
    
    # Inherits add_note() method from BaseEntity
    
    def update_custom_field(self, key: str, value: str) -> None:
        """Update a custom field (using inherited custom_metadata)."""
        self.update_custom_metadata(key, value)
    
    def remove_custom_field(self, key: str) -> bool:
        """
        Remove a custom field.
        
        Args:
            key: The key of the custom field to remove
            
        Returns:
            bool: True if field was removed, False if not found
        """
        if key in self.custom_metadata:
            del self.custom_metadata[key]
            self.updated_at = datetime.now()
            return True
        return False
    
    @property
    def custom_fields(self) -> Dict[str, str]:
        """Get custom fields (alias for custom_metadata for backward compatibility)."""
        # Convert values to strings for backward compatibility
        return {k: str(v) for k, v in self.custom_metadata.items()}
    
    @custom_fields.setter
    def custom_fields(self, value: Dict[str, str]) -> None:
        """Set custom fields (alias for custom_metadata for backward compatibility)."""
        self.custom_metadata = value
    
    def author_names_formatted(self) -> str:
        """
        Get formatted author names for citation.
        
        Returns:
            str: Formatted author list for citation
        """
        if not self.authors:
            return "Unknown Author"
        
        if len(self.authors) == 1:
            return self.authors[0].full_name()
        
        if len(self.authors) == 2:
            return f"{self.authors[0].full_name()} and {self.authors[1].full_name()}"
        
        if len(self.authors) > 2:
            return f"{self.authors[0].full_name()} et al."


class TaskReferenceLink(BaseLink):
    """Model representing a link between a research task and a reference."""
    
    relevance: Optional[str] = None  # Description of why this reference is relevant to the task
    updated_at: datetime = Field(default_factory=datetime.now)  # Add updated_at for backward compatibility
    
    def __init__(self, task_id: UUID, reference_id: UUID, relevance: Optional[str] = None, notes: Optional[List[str]] = None, **kwargs):
        super().__init__(source_id=task_id, target_id=reference_id, link_type="task_reference", **kwargs)
        self.relevance = relevance
        if notes is not None:
            self.metadata["notes"] = notes
    
    @property
    def task_id(self) -> UUID:
        """Get task ID (alias for source_id for backward compatibility)."""
        return self.source_id
    
    @task_id.setter  
    def task_id(self, value: UUID) -> None:
        """Set task ID (alias for source_id for backward compatibility)."""
        self.source_id = value
    
    @property
    def reference_id(self) -> UUID:
        """Get reference ID (alias for target_id for backward compatibility)."""
        return self.target_id
    
    @reference_id.setter
    def reference_id(self, value: UUID) -> None:
        """Set reference ID (alias for target_id for backward compatibility)."""
        self.target_id = value
    
    @property
    def notes(self) -> List[str]:
        """Get notes from metadata for backward compatibility."""
        return self.metadata.get("notes", [])
    
    @notes.setter
    def notes(self, value: List[str]) -> None:
        """Set notes in metadata for backward compatibility."""
        self.metadata["notes"] = value
    
    def update(self, **kwargs) -> None:
        """Update link fields."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
    
    def add_note(self, note: str) -> None:
        """Add a note to the link."""
        notes = self.metadata.get("notes", [])
        notes.append(note)
        self.metadata["notes"] = notes
        self.updated_at = datetime.now()