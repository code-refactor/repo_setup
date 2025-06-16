"""Data models for security findings."""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any, Set

from pydantic import BaseModel, Field, field_validator, model_validator

from common.core.models import StatusManagedAnnotatedEntity, BaseEnum
from securetask.utils.validation import ValidationError


class FindingStatus(BaseEnum):
    """Status values for security findings."""
    
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    REMEDIATED = "remediated"
    VERIFIED = "verified"
    CLOSED = "closed"
    FALSE_POSITIVE = "false_positive"


class FindingSeverity(BaseEnum):
    """Severity levels for security findings."""
    
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class Finding(StatusManagedAnnotatedEntity):
    """
    Model representing a security finding or vulnerability.
    
    Contains comprehensive metadata about security issues, including
    technical details, affected systems, and tracking information.
    """
    
    # Override id to use string instead of UUID for backward compatibility
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    affected_systems: List[str] = Field(default_factory=list)
    discovered_date: datetime = Field(default_factory=datetime.now)
    discovered_by: str
    status: str = FindingStatus.OPEN.value
    severity: str  # critical, high, medium, low, info
    cvss_vector: Optional[str] = None
    cvss_score: Optional[float] = None
    cvss_severity: Optional[str] = None
    remediation_plan: Optional[str] = None
    remediation_date: Optional[datetime] = None
    remediated_by: Optional[str] = None
    verification_date: Optional[datetime] = None
    verified_by: Optional[str] = None
    # Inherit tags from StatusManagedAnnotatedEntity, but maintain List for compatibility
    evidence_ids: List[str] = Field(default_factory=list)
    compliance_controls: List[str] = Field(default_factory=list)
    references: List[str] = Field(default_factory=list)
    # Legacy notes field for compatibility (in addition to annotations)
    notes: List[Dict[str, Any]] = Field(default_factory=list)
    
    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        """Validate that the status is a known value."""
        if not FindingStatus.is_valid(value):
            valid_values = ', '.join(FindingStatus.values())
            raise ValidationError(
                f"Invalid status: {value}. Allowed values: {valid_values}", 
                "status"
            )
        return value
    
    @field_validator("severity")
    @classmethod
    def validate_severity(cls, value: str) -> str:
        """Validate that the severity is a known value."""
        if not FindingSeverity.is_valid(value):
            valid_values = ', '.join(FindingSeverity.values())
            raise ValidationError(
                f"Invalid severity: {value}. Allowed values: {valid_values}", 
                "severity"
            )
        return value
    
    @model_validator(mode='after')
    def status_field_validation(self) -> 'Finding':
        """Validate fields based on status."""
        if self.status == "remediated" and not self.remediation_date:
            self.remediation_date = datetime.now()
            
        if self.status == "verified" and not self.verification_date:
            self.verification_date = datetime.now()
            
        return self
        
    def validate(self, value=None) -> 'Finding':
        """
        Compatibility method for Pydantic v2 validation API.

        Args:
            value: Optional value to validate (for Pydantic v2 compatibility)

        Returns:
            The validated Finding instance

        Raises:
            ValidationError: If validation fails
        """
        if value is None:
            # Validate current instance
            self.validate_status(self.status)
            self.validate_severity(self.severity)
            return self
        else:
            # For Pydantic v2 compatibility
            if isinstance(value, dict):
                return Finding(**value)
            return value
    
    def add_note(self, content: str, author: str) -> Dict[str, Any]:
        """
        Add a timestamped note to the finding.
        
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
    
    def add_evidence(self, evidence_id: str) -> None:
        """
        Link evidence to the finding.
        
        Args:
            evidence_id: ID of the evidence to link
        """
        if evidence_id not in self.evidence_ids:
            self.evidence_ids.append(evidence_id)
            
    def remove_evidence(self, evidence_id: str) -> bool:
        """
        Remove linked evidence from the finding.
        
        Args:
            evidence_id: ID of the evidence to remove
            
        Returns:
            True if evidence was removed, False if not found
        """
        if evidence_id in self.evidence_ids:
            self.evidence_ids.remove(evidence_id)
            return True
        return False
            
    def add_compliance_control(self, control_id: str) -> None:
        """
        Link a compliance control to the finding.
        
        Args:
            control_id: ID of the compliance control to link
        """
        if control_id not in self.compliance_controls:
            self.compliance_controls.append(control_id)
    
    def remove_compliance_control(self, control_id: str) -> bool:
        """
        Remove a linked compliance control from the finding.
        
        Args:
            control_id: ID of the compliance control to remove
            
        Returns:
            True if control was removed, False if not found
        """
        if control_id in self.compliance_controls:
            self.compliance_controls.remove(control_id)
            return True
        return False
    
    def update_cvss(self, vector: str, score: float, severity: str) -> None:
        """
        Update the CVSS information for this finding.
        
        Args:
            vector: CVSS vector string
            score: Calculated CVSS score
            severity: CVSS severity rating
        """
        self.cvss_vector = vector
        self.cvss_score = score
        self.cvss_severity = severity
        
    def update_status(self, new_status: str, user: str, note: Optional[str] = None) -> None:
        """
        Update the status of the finding using enhanced status management.
        
        Args:
            new_status: New status value
            user: User making the status change
            note: Optional note about the status change
            
        Raises:
            ValidationError: If the status is invalid
        """
        # Use the enhanced status management from parent class
        old_status = self.status
        super().update_status(new_status, user, note)
        
        # Update finding-specific fields based on status
        if new_status == FindingStatus.REMEDIATED.value:
            self.remediation_date = datetime.now()
            self.remediated_by = user
        elif new_status == FindingStatus.VERIFIED.value:
            self.verification_date = datetime.now()
            self.verified_by = user