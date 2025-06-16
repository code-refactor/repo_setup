from datetime import datetime
from typing import Dict, List, Optional, Set, Union, Any
from uuid import UUID

from pydantic import Field

from common.core.models import BaseEntity, BaseEnum, StatusManagedEntity


class TaskStatus(BaseEnum):
    """Status of a research task."""
    
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class TaskPriority(BaseEnum):
    """Priority level of a research task."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ResearchQuestion(BaseEntity):
    """Model representing a research question."""
    
    text: str
    description: Optional[str] = None
    parent_question_id: Optional[UUID] = None


class ResearchTask(StatusManagedEntity):
    """Model representing a research task with comprehensive metadata."""

    title: str
    description: str
    status: str = TaskStatus.PLANNED.value
    priority: TaskPriority = TaskPriority.MEDIUM
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Associations with research questions and subtasks
    research_question_ids: Set[UUID] = Field(default_factory=set)
    parent_task_id: Optional[UUID] = None
    subtask_ids: Set[UUID] = Field(default_factory=set)

    # Associations with other research artifacts
    reference_ids: Set[UUID] = Field(default_factory=set)  # Bibliographic references
    dataset_ids: Set[UUID] = Field(default_factory=set)    # Dataset versions
    environment_ids: Set[UUID] = Field(default_factory=set)  # Computational environments
    experiment_ids: Set[UUID] = Field(default_factory=set)  # Experiments
    
    # Additional properties for integration tests
    # These aren't persisted, but used for convenience in tests
    research_questions: List[Any] = Field(default_factory=list, exclude=True)
    references: List[Any] = Field(default_factory=list, exclude=True)
    datasets: List[Any] = Field(default_factory=list, exclude=True)
    environments: List[Any] = Field(default_factory=list, exclude=True)
    experiments: List[Any] = Field(default_factory=list, exclude=True)
    
    def update(self, **kwargs) -> None:
        """Update task fields with research-specific logic."""
        # Handle status updates specially to use status management
        if 'status' in kwargs:
            old_status = self.status
            new_status = kwargs.pop('status')
            # Use the enhanced status management
            self.update_status(new_status)
        
        # Call parent update method for other fields
        super().update(**kwargs)
        
        # Update completion timestamp if status changed to completed
        if self.status == TaskStatus.COMPLETED.value and not self.completed_at:
            self.completed_at = datetime.now()
    
    def add_research_question(self, question_id: UUID) -> None:
        """Associate a research question with this task."""
        self.research_question_ids.add(question_id)
        self.updated_at = datetime.now()
    
    def remove_research_question(self, question_id: UUID) -> None:
        """Remove association with a research question."""
        if question_id in self.research_question_ids:
            self.research_question_ids.remove(question_id)
            self.updated_at = datetime.now()

    def add_subtask(self, subtask_id: UUID) -> None:
        """Add a subtask to this task."""
        self.subtask_ids.add(subtask_id)
        self.updated_at = datetime.now()

    def remove_subtask(self, subtask_id: UUID) -> None:
        """Remove a subtask from this task."""
        if subtask_id in self.subtask_ids:
            self.subtask_ids.remove(subtask_id)
            self.updated_at = datetime.now()


    # Bibliographic reference association methods
    def add_reference(self, reference_id: UUID) -> None:
        """Associate a bibliographic reference with this task."""
        self.reference_ids.add(reference_id)
        self.updated_at = datetime.now()

    def remove_reference(self, reference_id: UUID) -> None:
        """Remove association with a bibliographic reference."""
        if reference_id in self.reference_ids:
            self.reference_ids.remove(reference_id)
            self.updated_at = datetime.now()

    # Dataset association methods
    def add_dataset(self, dataset_id: UUID) -> None:
        """Associate a dataset with this task."""
        self.dataset_ids.add(dataset_id)
        self.updated_at = datetime.now()

    def remove_dataset(self, dataset_id: UUID) -> None:
        """Remove association with a dataset."""
        if dataset_id in self.dataset_ids:
            self.dataset_ids.remove(dataset_id)
            self.updated_at = datetime.now()

    # Environment association methods
    def add_environment(self, environment_id: UUID) -> None:
        """Associate a computational environment with this task."""
        self.environment_ids.add(environment_id)
        self.updated_at = datetime.now()

    def remove_environment(self, environment_id: UUID) -> None:
        """Remove association with a computational environment."""
        if environment_id in self.environment_ids:
            self.environment_ids.remove(environment_id)
            self.updated_at = datetime.now()

    # Experiment association methods
    def add_experiment(self, experiment_id: UUID) -> None:
        """Associate an experiment with this task."""
        self.experiment_ids.add(experiment_id)
        self.updated_at = datetime.now()

    def remove_experiment(self, experiment_id: UUID) -> None:
        """Remove association with an experiment."""
        if experiment_id in self.experiment_ids:
            self.experiment_ids.remove(experiment_id)
            self.updated_at = datetime.now()