"""Data models for evidence storage."""

import uuid
import os
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any, Union, Set

from pydantic import BaseModel, Field, field_validator

from securetask.utils.validation import ValidationError, validate_file_size


class EvidenceType(str, Enum):
    """Types of evidence that can be stored."""
    
    SCREENSHOT = "screenshot"
    LOG = "log"
    CODE = "code"
    NETWORK_CAPTURE = "network_capture"
    DATABASE_DUMP = "database_dump"
    CONFIG = "config"
    EXPLOIT = "exploit"
    DOCUMENT = "document"
    OTHER = "other"


class AccessLevel(str, Enum):
    """Access levels for evidence."""
    
    PUBLIC = "public"  # Available to all team members
    RESTRICTED = "restricted"  # Available to specified team members
    CONFIDENTIAL = "confidential"  # Available only to authorized personnel
    TOP_SECRET = "top_secret"  # Available only to specified individuals


class Evidence(BaseModel):
    """
    Model representing stored evidence for security findings.
    
    Holds metadata about evidence files, including origin, access controls,
    and cryptographic verification information.
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    type: EvidenceType
    file_path: str  # Path to the encrypted evidence file
    original_filename: str
    content_type: str
    hash_original: str  # SHA-256 hash of original content
    hash_encrypted: str  # SHA-256 hash of encrypted content
    size_bytes: int
    uploaded_date: datetime = Field(default_factory=datetime.now)
    uploaded_by: str
    access_level: AccessLevel = AccessLevel.RESTRICTED
    authorized_users: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    related_finding_ids: List[str] = Field(default_factory=list)
    encryption_info: Dict[str, Any] = Field(default_factory=dict)
    notes: List[Dict[str, Any]] = Field(default_factory=list)
    
    @field_validator("type")
    @classmethod
    def validate_type(cls, value):
        """Validate the evidence type."""
        if isinstance(value, EvidenceType):
            return value
            
        if isinstance(value, str) and value in [v.value for v in EvidenceType]:
            return EvidenceType(value)
            
        raise ValidationError(
            f"Invalid evidence type: {value}. Must be one of: {', '.join([v.value for v in EvidenceType])}",
            "type"
        )
    
    @field_validator("access_level")
    @classmethod
    def validate_access_level(cls, value):
        """Validate the access level."""
        if isinstance(value, AccessLevel):
            return value
            
        if isinstance(value, str) and value in [v.value for v in AccessLevel]:
            return AccessLevel(value)
            
        raise ValidationError(
            f"Invalid access level: {value}. Must be one of: {', '.join([v.value for v in AccessLevel])}",
            "access_level"
        )
    
    def add_related_finding(self, finding_id: str) -> None:
        """
        Associate evidence with a finding.
        
        Args:
            finding_id: ID of the finding to associate
        """
        if finding_id not in self.related_finding_ids:
            self.related_finding_ids.append(finding_id)
    
    def add_note(self, content: str, author: str) -> Dict[str, Any]:
        """
        Add a timestamped note to the evidence.
        
        Args:
            content: The note content
            author: The author of the note
            
        Returns:
            The created note as a dictionary
        """
        note = {
            "id": str(uuid.uuid4()),
            "content": content,
            "author": author,
            "timestamp": datetime.now()
        }
        self.notes.append(note)
        return note
    
    def is_accessible_by(self, user_id: str) -> bool:
        """
        Check if a user has access to this evidence.
        
        Args:
            user_id: ID of the user to check
            
        Returns:
            True if the user has access, False otherwise
        """
        if self.access_level == AccessLevel.PUBLIC:
            return True
            
        if user_id == self.uploaded_by:
            return True
            
        if user_id in self.authorized_users:
            return True
            
        # Confidential and top_secret require explicit authorization
        if self.access_level in [AccessLevel.CONFIDENTIAL, AccessLevel.TOP_SECRET]:
            return False
            
        # For restricted, we could implement custom logic here
        return False