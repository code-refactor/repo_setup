"""
Core data models for the ProductMind knowledge management system.
"""
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

# Import common library components
from common.core import (
    BaseKnowledgeNode,
    SearchableEntity,
    TimestampedEntity,
    BaseRelationship,
    Priority as CommonPriority,
    Status
)


class Sentiment(str, Enum):
    """Sentiment classification for feedback."""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    MIXED = "mixed"


# Use common Priority enum
Priority = CommonPriority


class SourceType(str, Enum):
    """Types of feedback sources."""
    SURVEY = "survey"
    SUPPORT_TICKET = "support_ticket"
    INTERVIEW = "interview"
    APP_REVIEW = "app_review"
    SOCIAL_MEDIA = "social_media"
    SALES_CALL = "sales_call"
    CUSTOMER_MEETING = "customer_meeting"
    BETA_FEEDBACK = "beta_feedback"
    OTHER = "other"


class StakeholderType(str, Enum):
    """Types of stakeholders."""
    EXECUTIVE = "executive"
    PRODUCT = "product"
    ENGINEERING = "engineering"
    DESIGN = "design"
    MARKETING = "marketing"
    SALES = "sales"
    CUSTOMER_SUCCESS = "customer_success"
    FINANCE = "finance"
    LEGAL = "legal"
    CUSTOMER = "customer"
    PARTNER = "partner"
    OTHER = "other"


class Feedback(SearchableEntity):
    """Customer feedback model."""
    source: SourceType
    source_id: Optional[str] = None
    customer_id: Optional[str] = None
    customer_segment: Optional[str] = None
    sentiment: Optional[Sentiment] = None
    themes: List[str] = Field(default_factory=list)
    cluster_id: Optional[int] = None
    impact_score: Optional[float] = None
    
    def __init__(self, content: str = "", title: str = "", **kwargs):
        # If title is not provided but content is, derive title from content
        if not title and content:
            title = content[:50] + "..." if len(content) > 50 else content
        # If content is not provided but title is, use title as content
        elif not content and title:
            content = title
        
        super().__init__(title=title, content=content, **kwargs)


class Theme(SearchableEntity):
    """Extracted theme from feedback."""
    name: str
    description: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    frequency: int = 0
    impact_score: float = 0.0
    sentiment_distribution: Dict[Sentiment, int] = Field(default_factory=dict)
    feedback_ids: List[UUID] = Field(default_factory=list)
    
    def __init__(self, name: str, title: str = "", content: str = "", **kwargs):
        # Use name as title if not provided
        if not title:
            title = name
        # Use description as content if not provided
        if not content:
            content = kwargs.get('description', '')
        
        # Add name to kwargs for proper initialization
        kwargs['name'] = name
        
        super().__init__(title=title, content=content, **kwargs)
        
    def get_searchable_content(self) -> str:
        """Get all searchable text content from this theme."""
        parts = [self.name]
        if self.description:
            parts.append(self.description)
        parts.extend(self.keywords)
        parts.extend(self.tags)
        return " ".join(parts).lower()


class FeedbackCluster(BaseModel):
    """Cluster of related feedback items."""
    id: int
    name: str
    description: Optional[str] = None
    centroid: List[float] = Field(default_factory=list)
    feedback_ids: List[UUID] = Field(default_factory=list)
    themes: List[str] = Field(default_factory=list)
    sentiment_distribution: Dict[Sentiment, int] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class StrategicGoal(SearchableEntity):
    """Strategic business objective."""
    name: str
    description: str
    priority: Priority
    metrics: List[str] = Field(default_factory=list)
    
    def __init__(self, name: str, description: str, title: str = "", content: str = "", **kwargs):
        # Use name as title if not provided
        if not title:
            title = name
        # Use description as content if not provided
        if not content:
            content = description
        
        # Add required fields to kwargs
        kwargs['name'] = name
        kwargs['description'] = description
        
        super().__init__(title=title, content=content, **kwargs)


class Feature(SearchableEntity):
    """Product feature for prioritization."""
    name: str
    description: str
    status: str = "proposed"
    priority: Optional[Priority] = None
    effort_estimate: Optional[float] = None
    value_estimate: Optional[float] = None
    risk_level: Optional[float] = None
    dependencies: List[UUID] = Field(default_factory=list)
    themes: List[str] = Field(default_factory=list)
    strategic_alignment: Dict[UUID, float] = Field(default_factory=dict)
    feedback_ids: List[UUID] = Field(default_factory=list)
    
    def __init__(self, name: str, description: str, title: str = "", content: str = "", **kwargs):
        # Use name as title if not provided
        if not title:
            title = name
        # Use description as content if not provided
        if not content:
            content = description
        
        # Add required fields to kwargs
        kwargs['name'] = name
        kwargs['description'] = description
        
        super().__init__(title=title, content=content, **kwargs)


class Competitor(SearchableEntity):
    """Competitor profile."""
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    market_share: Optional[float] = None
    target_segments: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    feature_comparison: Dict[str, bool] = Field(default_factory=dict)
    price_points: Dict[str, float] = Field(default_factory=dict)
    
    def __init__(self, name: str, title: str = "", content: str = "", description: Optional[str] = None, **kwargs):
        # Use name as title if not provided
        if not title:
            title = name
        # Use description as content if not provided
        if not content:
            content = description or ""
        
        # Add name and description to kwargs for proper initialization
        kwargs['name'] = name
        kwargs['description'] = description
        
        super().__init__(title=title, content=content, **kwargs)


class CompetitiveFeature(BaseModel):
    """Feature for competitive analysis."""
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    category: str
    importance: float = 1.0
    our_implementation: Optional[str] = None
    our_rating: Optional[float] = None
    competitor_implementations: Dict[str, Optional[str]] = Field(default_factory=dict)
    competitor_ratings: Dict[str, Optional[float]] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class MarketGap(BaseModel):
    """Identified gap in the market."""
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    size_estimate: Optional[float] = None
    opportunity_score: float = 0.0
    related_feedback: List[UUID] = Field(default_factory=list)
    competing_solutions: List[UUID] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)


class Alternative(BaseModel):
    """Alternative option for a decision."""
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    pros: List[str] = Field(default_factory=list)
    cons: List[str] = Field(default_factory=list)
    estimated_cost: Optional[float] = None
    estimated_benefit: Optional[float] = None
    estimated_risk: Optional[float] = None
    score: Optional[float] = None


class Decision(SearchableEntity):
    """Product decision with context and rationale."""
    context: str
    problem_statement: str
    decision_date: datetime
    decision_maker: str
    chosen_alternative: UUID
    alternatives: List[Alternative] = Field(default_factory=list)
    rationale: str
    success_criteria: List[str] = Field(default_factory=list)
    related_decisions: List[UUID] = Field(default_factory=list)
    related_feedback: List[UUID] = Field(default_factory=list)
    related_features: List[UUID] = Field(default_factory=list)
    status: str = "decided"
    outcome_assessment: Optional[str] = None
    
    def get_searchable_content(self) -> str:
        """Get all searchable text content from this decision."""
        parts = [self.title, self.content, self.context, self.problem_statement, self.rationale]
        if self.outcome_assessment:
            parts.append(self.outcome_assessment)
        parts.extend(self.success_criteria)
        parts.extend(self.tags)
        return " ".join(str(p) for p in parts if p).lower()


class Perspective(BaseModel):
    """Stakeholder perspective on a topic."""
    id: UUID = Field(default_factory=uuid4)
    topic: str
    content: str
    priority: Priority
    influence_level: float = 1.0
    agreement_level: float = 0.0
    stakeholder_id: UUID


class Stakeholder(SearchableEntity):
    """Stakeholder profile."""
    name: str
    job_title: str  # Renamed to avoid conflict with inherited title
    department: str
    type: StakeholderType
    influence_level: float = 1.0
    perspectives: List[UUID] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)
    
    def __init__(self, name: str, job_title: str, department: str, title: str = "", content: str = "", **kwargs):
        # Use name as title if not provided
        if not title:
            title = name
        # Generate content from job info if not provided
        if not content:
            content = f"{job_title} in {department}"
        
        # Add required fields to kwargs before removing duplicates
        kwargs['name'] = name
        kwargs['job_title'] = job_title
        kwargs['department'] = department
        
        super().__init__(title=title, content=content, **kwargs)
        
    def get_searchable_content(self) -> str:
        """Get all searchable text content from this stakeholder."""
        parts = [self.name, self.job_title, self.department]
        parts.extend(self.interests)
        parts.extend(self.tags)
        return " ".join(parts).lower()


class StakeholderRelationship(BaseRelationship):
    """Relationship between stakeholders."""
    alignment_level: float = 0.0
    notes: Optional[str] = None
    stakeholder1_id: UUID  # Additional field for backward compatibility
    stakeholder2_id: UUID  # Additional field for backward compatibility
    
    def __init__(self, stakeholder1_id: UUID, stakeholder2_id: UUID, relationship_type: str, **kwargs):
        super().__init__(
            source_id=stakeholder1_id,
            target_id=stakeholder2_id,
            relationship_type=relationship_type,
            **kwargs
        )
        self.stakeholder1_id = stakeholder1_id
        self.stakeholder2_id = stakeholder2_id
        self.alignment_level = kwargs.get('alignment_level', 0.0)
        self.notes = kwargs.get('notes')