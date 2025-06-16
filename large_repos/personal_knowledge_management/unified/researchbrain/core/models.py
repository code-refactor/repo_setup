"""Core data models for the ResearchBrain knowledge management system."""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator

# Import common library components
from common.core import (
    BaseKnowledgeNode,
    SearchableEntity,
    TimestampedEntity,
    Evidence as BaseEvidence,
    Priority,
    Status
)


# Use common library base class - KnowledgeNode is now an alias
KnowledgeNode = BaseKnowledgeNode


class Note(SearchableEntity):
    """Represents a research note with content and metadata."""

    source: Optional[UUID] = None  # Reference to a source document
    page_reference: Optional[int] = None  # Page number in the source document
    attachments: List[Path] = Field(default_factory=list)
    citations: List[UUID] = Field(default_factory=list)  # References to Citation objects
    section_references: Dict[str, str] = Field(default_factory=dict)  # Section references in source documents


class CitationType(str, Enum):
    """Types of academic citations."""

    BOOK = "book"
    ARTICLE = "article"
    CONFERENCE = "conference"
    THESIS = "thesis"
    REPORT = "report"
    WEBPAGE = "webpage"
    PREPRINT = "preprint"
    OTHER = "other"


class Citation(SearchableEntity):
    """Represents a citation to an academic source."""

    authors: List[str]
    year: Optional[int] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    journal: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    publisher: Optional[str] = None
    citation_type: CitationType = CitationType.ARTICLE
    abstract: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    file_path: Optional[Path] = None
    bibtex: Optional[str] = None
    ris: Optional[str] = None  # RIS format citation data
    notes: List[UUID] = Field(default_factory=list)  # References to linked Note objects
    pdf_metadata: Dict[str, Any] = Field(default_factory=dict)  # Extracted metadata from PDF
    sections: Dict[str, str] = Field(default_factory=dict)  # Extracted sections from the paper


class CitationFormat(str, Enum):
    """Academic citation formats."""

    APA = "apa"
    MLA = "mla"
    CHICAGO = "chicago"
    HARVARD = "harvard"
    IEEE = "ieee"
    VANCOUVER = "vancouver"
    BIBTEX = "bibtex"
    RIS = "ris"


class EvidenceType(str, Enum):
    """Types of evidence for research questions."""

    SUPPORTING = "supporting"
    CONTRADICTING = "contradicting"
    INCONCLUSIVE = "inconclusive"
    RELATED = "related"


class EvidenceStrength(str, Enum):
    """Strength levels for evidence."""

    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    ANECDOTAL = "anecdotal"
    THEORETICAL = "theoretical"


class Evidence(BaseEvidence):
    """Evidence linked to a research question - extends common Evidence."""

    # Override the evidence_type field to use researchbrain's enum
    evidence_type: EvidenceType = Field(description="Type of evidence")
    strength: EvidenceStrength = Field(description="Strength of evidence")
    description: Optional[str] = Field(default=None, description="Evidence description")  # Make optional for researchbrain
    note_id: UUID  # Reference to the note containing the evidence
    citation_ids: List[UUID] = Field(default_factory=list)  # References to supporting citations


class ResearchQuestion(SearchableEntity):
    """Represents a research question or hypothesis."""

    question: str
    description: Optional[str] = None  # Keep for backward compatibility
    evidence: List[Evidence] = Field(default_factory=list)
    status: str = "open"  # open, resolved, abandoned
    priority: int = 0  # Use integer for backward compatibility with tests
    related_questions: List[UUID] = Field(default_factory=list)  # References to related questions
    knowledge_gaps: List[str] = Field(default_factory=list)  # Identified knowledge gaps
    
    def __init__(self, question: str, title: str = "", content: str = "", description: Optional[str] = None, priority: int = 0, **kwargs):
        """Initialize ResearchQuestion with question as title if title not provided."""
        if not title:
            title = question
        if not content and description:
            content = description
        
        kwargs['question'] = question
        kwargs['description'] = description
        kwargs['priority'] = priority
        super().__init__(title=title, content=content, **kwargs)
    
    def get_searchable_content(self) -> str:
        """Get all searchable text content from this research question."""
        parts = [self.question]
        if self.content:
            parts.append(self.content)
        parts.extend(self.knowledge_gaps)
        parts.extend(self.tags)
        return " ".join(parts).lower()


class ExperimentStatus(str, Enum):
    """Status options for experiments."""

    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"


class Experiment(TimestampedEntity):
    """Represents a scientific experiment with structured metadata."""

    title: str
    hypothesis: str
    status: ExperimentStatus = ExperimentStatus.PLANNED
    methodology: str
    variables: Dict[str, Any] = Field(default_factory=dict)
    results: Optional[str] = None
    conclusion: Optional[str] = None
    research_question_id: Optional[UUID] = None  # Link to a research question
    notes: List[UUID] = Field(default_factory=list)  # References to linked Note objects
    collaborators: List[UUID] = Field(default_factory=list)  # References to collaborators
    template_name: Optional[str] = None  # Name of the template used to create the experiment
    reproducibility_info: Dict[str, Any] = Field(default_factory=dict)  # Information for reproducibility
    
    # Map start/end dates to TimestampedEntity fields
    @property
    def start_date(self) -> Optional[datetime]:
        return self.started_at
    
    @start_date.setter
    def start_date(self, value: Optional[datetime]):
        self.started_at = value
    
    @property
    def end_date(self) -> Optional[datetime]:
        return self.completed_at
    
    @end_date.setter
    def end_date(self, value: Optional[datetime]):
        self.completed_at = value

    @field_validator("completed_at")
    def completed_at_after_started_at(cls, v, info):
        """Validate that completed_at is after started_at if both are provided."""
        values = info.data
        if v and "started_at" in values and values["started_at"]:
            if v < values["started_at"]:
                raise ValueError("completed_at must be after started_at")
        return v


class GrantStatus(str, Enum):
    """Status options for grant proposals."""

    DRAFTING = "drafting"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    AWARDED = "awarded"
    REJECTED = "rejected"
    COMPLETED = "completed"


class GrantProposal(SearchableEntity):
    """Represents a grant proposal workspace."""

    funding_agency: str
    deadline: Optional[datetime] = None
    status: GrantStatus = GrantStatus.DRAFTING
    amount: Optional[float] = None
    description: str
    notes: List[UUID] = Field(default_factory=list)  # References to related notes
    experiments: List[UUID] = Field(default_factory=list)  # References to related experiments
    research_questions: List[UUID] = Field(default_factory=list)  # References to research questions
    collaborators: List[UUID] = Field(default_factory=list)  # References to collaborators
    budget_items: Dict[str, Any] = Field(default_factory=dict)  # Budget line items and justifications
    timeline: Dict[str, Any] = Field(default_factory=dict)  # Project timeline information
    export_history: List[Dict[str, Any]] = Field(default_factory=list)  # Record of exports
    
    def get_searchable_content(self) -> str:
        """Get all searchable text content from this grant proposal."""
        parts = [self.title, self.funding_agency, self.description]
        parts.extend(self.tags)
        return " ".join(str(p) for p in parts if p).lower()


class CollaboratorRole(str, Enum):
    """Roles for collaborators."""

    PRINCIPAL_INVESTIGATOR = "principal_investigator"
    CO_INVESTIGATOR = "co_investigator"
    COLLABORATOR = "collaborator"
    ADVISOR = "advisor"
    CONSULTANT = "consultant"
    STUDENT = "student"


class Collaborator(SearchableEntity):
    """Represents a research collaborator."""

    name: str
    email: Optional[str] = None
    affiliation: Optional[str] = None
    role: CollaboratorRole = CollaboratorRole.COLLABORATOR
    notes: List[UUID] = Field(default_factory=list)  # References to notes they've contributed to
    permissions: Dict[str, bool] = Field(default_factory=dict)  # Permissions for different operations
    experiments: List[UUID] = Field(default_factory=list)  # Experiments they're involved in
    grants: List[UUID] = Field(default_factory=list)  # Grants they're involved in
    
    @property
    def title(self) -> str:
        """Use name as title for SearchableEntity compatibility."""
        return self.name
    
    @title.setter 
    def title(self, value: str):
        """Set name when title is set."""
        self.name = value
        
    def get_searchable_content(self) -> str:
        """Get all searchable text content from this collaborator."""
        parts = [self.name]
        if self.email:
            parts.append(self.email)
        if self.affiliation:
            parts.append(self.affiliation)
        parts.extend(self.tags)
        return " ".join(parts).lower()


class Annotation(SearchableEntity):
    """Represents an annotation or comment on a knowledge node."""

    node_id: UUID  # Reference to the annotated knowledge node
    collaborator_id: UUID  # Who made the annotation
    position: Optional[str] = None  # For annotations with specific position in document
    status: str = "open"  # Status of the annotation (open, addressed, rejected)
    replies: List[UUID] = Field(default_factory=list)  # References to reply annotations
    parent_id: Optional[UUID] = None  # Reference to parent annotation if this is a reply
    resolved_by: Optional[UUID] = None  # Reference to collaborator who resolved this
    
    @property
    def title(self) -> str:
        """Generate title from content for SearchableEntity compatibility."""
        return self.content[:50] + "..." if len(self.content) > 50 else self.content
    
    @title.setter 
    def title(self, value: str):
        """Set content when title is set (for compatibility)."""
        pass  # Don't overwrite content