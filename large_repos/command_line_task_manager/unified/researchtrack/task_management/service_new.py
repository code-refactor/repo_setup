from datetime import datetime
from typing import Dict, List, Optional, Set, Union, Any
from uuid import UUID

from common.core.service import BaseService, StatusManagedService
from common.core.storage import BaseStorageInterface
from common.core.exceptions import EntityNotFoundError, ValidationError

from .models import ResearchQuestion, ResearchTask, TaskPriority, TaskStatus
from .storage import TaskStorageInterface


class ResearchTaskService(StatusManagedService):
    """Service for managing research tasks using the enhanced StatusManagedService."""

    def __init__(self, storage: BaseStorageInterface[ResearchTask]):
        super().__init__(storage, "ResearchTask")
        
        # Setup status transition validation
        self._setup_status_validation()
        self._setup_status_hooks()
        
        # Validation callbacks for external references
        self._validate_reference_callback = None
        self._validate_dataset_callback = None
        self._validate_environment_callback = None
        self._validate_experiment_callback = None
    
    def _setup_status_validation(self):
        """Setup status transition validation rules."""
        # Define valid transitions
        valid_transitions = {
            (TaskStatus.PLANNED.value, TaskStatus.IN_PROGRESS.value): lambda f, t: True,
            (TaskStatus.IN_PROGRESS.value, TaskStatus.COMPLETED.value): lambda f, t: True,
            (TaskStatus.IN_PROGRESS.value, TaskStatus.PLANNED.value): lambda f, t: True,
            (TaskStatus.COMPLETED.value, TaskStatus.ARCHIVED.value): lambda f, t: True,
            (TaskStatus.PLANNED.value, TaskStatus.ARCHIVED.value): lambda f, t: True,
        }
        
        for (from_status, to_status), validator in valid_transitions.items():
            self.register_status_validator(from_status, to_status, validator)
    
    def _setup_status_hooks(self):
        """Setup hooks for status transitions."""
        def on_completion(entity, old_status, new_status):
            """Hook for when task is completed."""
            if new_status == TaskStatus.COMPLETED.value and not entity.completed_at:
                entity.completed_at = datetime.now()
                # Update in storage
                self._storage.update(entity)
        
        self.register_status_transition_hook(
            TaskStatus.IN_PROGRESS.value, 
            TaskStatus.COMPLETED.value, 
            on_completion
        )

    def set_reference_validator(self, validator_callback):
        """Set a callback function to validate reference IDs."""
        self._validate_reference_callback = validator_callback

    def set_dataset_validator(self, validator_callback):
        """Set a callback function to validate dataset IDs."""
        self._validate_dataset_callback = validator_callback

    def set_environment_validator(self, validator_callback):
        """Set a callback function to validate environment IDs."""
        self._validate_environment_callback = validator_callback

    def set_experiment_validator(self, validator_callback):
        """Set a callback function to validate experiment IDs."""
        self._validate_experiment_callback = validator_callback

    def create_task(
        self,
        title: str,
        description: str,
        status: TaskStatus = TaskStatus.PLANNED,
        priority: TaskPriority = TaskPriority.MEDIUM,
        estimated_hours: Optional[float] = None,
        due_date: Optional[datetime] = None,
        parent_task_id: Optional[UUID] = None,
        research_question_ids: Optional[Set[UUID]] = None,
        tags: Optional[Set[str]] = None,
        custom_metadata: Optional[Dict[str, Union[str, int, float, bool, list, dict]]] = None,
    ) -> ResearchTask:
        """Create a new research task."""
        
        # Build the task data
        task_data = {
            "title": title,
            "description": description,
            "status": status,
            "priority": priority,
            "estimated_hours": estimated_hours,
            "due_date": due_date,
            "parent_task_id": parent_task_id,
            "research_question_ids": research_question_ids or set(),
            "tags": tags or set(),
            "custom_metadata": custom_metadata or {},
        }
        
        # Create using the base service
        return self.create(task_data, ResearchTask)

    def _validate_create_data(self, data: Dict[str, Any]) -> None:
        """Validate data before task creation."""
        # Validate parent task if provided
        if "parent_task_id" in data and data["parent_task_id"] is not None:
            parent_task = self.get(data["parent_task_id"])
            if not parent_task:
                raise ValidationError(f"Parent task with ID {data['parent_task_id']} does not exist")
        
        # Validate research questions if provided
        if "research_question_ids" in data and data["research_question_ids"]:
            # This would require a reference to the question service
            # For now, we'll skip this validation
            pass

    def update_task_status(self, task_id: UUID, status: str, user: Optional[str] = None, note: Optional[str] = None) -> bool:
        """Update task status with validation and history tracking."""
        return self.update_status(task_id, status, user, note)
    
    def get_tasks_by_status(self, status: str) -> List[ResearchTask]:
        """Get all tasks with a specific status."""
        return self.get_by_status(status)
    
    def get_active_tasks(self) -> List[ResearchTask]:
        """Get all active (non-archived, non-completed) tasks."""
        active_statuses = [TaskStatus.PLANNED.value, TaskStatus.IN_PROGRESS.value]
        return self.get_by_statuses(active_statuses)
    
    def get_completed_tasks(self) -> List[ResearchTask]:
        """Get all completed tasks."""
        return self.get_by_status(TaskStatus.COMPLETED.value)

    def add_reference_to_task(self, task_id: UUID, reference_id: UUID) -> bool:
        """Associate a bibliographic reference with a task."""
        # Validate reference if validator is set
        if self._validate_reference_callback and not self._validate_reference_callback(reference_id):
            raise ValidationError(f"Reference with ID {reference_id} does not exist")

        task = self.get_or_raise(task_id)
        task.add_reference(reference_id)
        return self._storage.update(task)

    def remove_reference_from_task(self, task_id: UUID, reference_id: UUID) -> bool:
        """Remove association between a bibliographic reference and a task."""
        task = self.get_or_raise(task_id)
        task.remove_reference(reference_id)
        return self._storage.update(task)

    def add_dataset_to_task(self, task_id: UUID, dataset_id: UUID) -> bool:
        """Associate a dataset with a task."""
        # Validate dataset if validator is set
        if self._validate_dataset_callback and not self._validate_dataset_callback(dataset_id):
            raise ValidationError(f"Dataset with ID {dataset_id} does not exist")

        task = self.get_or_raise(task_id)
        task.add_dataset(dataset_id)
        return self._storage.update(task)

    def remove_dataset_from_task(self, task_id: UUID, dataset_id: UUID) -> bool:
        """Remove association between a dataset and a task."""
        task = self.get_or_raise(task_id)
        task.remove_dataset(dataset_id)
        return self._storage.update(task)

    def add_environment_to_task(self, task_id: UUID, environment_id: UUID) -> bool:
        """Associate a computational environment with a task."""
        # Validate environment if validator is set
        if self._validate_environment_callback and not self._validate_environment_callback(environment_id):
            raise ValidationError(f"Environment with ID {environment_id} does not exist")

        task = self.get_or_raise(task_id)
        task.add_environment(environment_id)
        return self._storage.update(task)

    def remove_environment_from_task(self, task_id: UUID, environment_id: UUID) -> bool:
        """Remove association between a computational environment and a task."""
        task = self.get_or_raise(task_id)
        task.remove_environment(environment_id)
        return self._storage.update(task)

    def add_experiment_to_task(self, task_id: UUID, experiment_id: UUID) -> bool:
        """Associate an experiment with a task."""
        # Validate experiment if validator is set
        if self._validate_experiment_callback and not self._validate_experiment_callback(experiment_id):
            raise ValidationError(f"Experiment with ID {experiment_id} does not exist")

        task = self.get_or_raise(task_id)
        task.add_experiment(experiment_id)
        return self._storage.update(task)

    def remove_experiment_from_task(self, task_id: UUID, experiment_id: UUID) -> bool:
        """Remove association between an experiment and a task."""
        task = self.get_or_raise(task_id)
        task.remove_experiment(experiment_id)
        return self._storage.update(task)

    def get_subtasks(self, parent_task_id: UUID) -> List[ResearchTask]:
        """Get all subtasks of a parent task."""
        return self.list(filters={"parent_task_id": parent_task_id})

    def list_by_status(self, status: TaskStatus) -> List[ResearchTask]:
        """List tasks by status."""
        return self.list(filters={"status": status})

    def list_by_priority(self, priority: TaskPriority) -> List[ResearchTask]:
        """List tasks by priority."""
        return self.list(filters={"priority": priority})


class ResearchQuestionService(BaseService[ResearchQuestion]):
    """Service for managing research questions using the common BaseService."""

    def __init__(self, storage: BaseStorageInterface[ResearchQuestion]):
        super().__init__(storage, "ResearchQuestion")

    def create_question(
        self,
        text: str,
        description: Optional[str] = None,
        parent_question_id: Optional[UUID] = None,
        tags: Optional[Set[str]] = None,
        custom_metadata: Optional[Dict[str, Union[str, int, float, bool, list, dict]]] = None,
    ) -> ResearchQuestion:
        """Create a new research question."""
        
        question_data = {
            "text": text,
            "description": description,
            "parent_question_id": parent_question_id,
            "tags": tags or set(),
            "custom_metadata": custom_metadata or {},
        }
        
        return self.create(question_data, ResearchQuestion)

    def _validate_create_data(self, data: Dict[str, Any]) -> None:
        """Validate data before question creation."""
        # Validate parent question if provided
        if "parent_question_id" in data and data["parent_question_id"] is not None:
            parent_question = self.get(data["parent_question_id"])
            if not parent_question:
                raise ValidationError(f"Parent question with ID {data['parent_question_id']} does not exist")

    def list_top_level_questions(self) -> List[ResearchQuestion]:
        """List questions that have no parent."""
        return self.list(filters={"parent_question_id": None})

    def get_sub_questions(self, parent_question_id: UUID) -> List[ResearchQuestion]:
        """Get all sub-questions of a parent question."""
        return self.list(filters={"parent_question_id": parent_question_id})


# Legacy compatibility service
class TaskManagementService:
    """Legacy compatibility wrapper for the original service interface."""

    def __init__(self, storage: TaskStorageInterface):
        # Create new-style services using adapter storage
        self._task_storage = TaskStorageAdapter(storage)
        self._question_storage = QuestionStorageAdapter(storage)
        
        self._task_service = ResearchTaskService(self._task_storage)
        self._question_service = ResearchQuestionService(self._question_storage)

    def create_task(self, *args, **kwargs) -> UUID:
        """Create a task and return its ID (legacy interface)."""
        task = self._task_service.create_task(*args, **kwargs)
        return task.id

    def get_task(self, task_id: UUID) -> Optional[ResearchTask]:
        """Get a task by ID."""
        return self._task_service.get(task_id)

    def update_task(self, task_id: UUID, **kwargs) -> bool:
        """Update a task."""
        return self._task_service.update(task_id, kwargs)

    def delete_task(self, task_id: UUID) -> bool:
        """Delete a task."""
        return self._task_service.delete(task_id)

    def list_tasks(self, **kwargs) -> List[ResearchTask]:
        """List tasks with filters."""
        return self._task_service.list(filters=kwargs)

    def create_research_question(self, *args, **kwargs) -> UUID:
        """Create a research question and return its ID (legacy interface)."""
        question = self._question_service.create_question(*args, **kwargs)
        return question.id

    def get_research_question(self, question_id: UUID) -> Optional[ResearchQuestion]:
        """Get a research question by ID."""
        return self._question_service.get(question_id)

    def update_research_question(self, question_id: UUID, **kwargs) -> bool:
        """Update a research question."""
        return self._question_service.update(question_id, kwargs)

    def delete_research_question(self, question_id: UUID) -> bool:
        """Delete a research question."""
        return self._question_service.delete(question_id)

    def list_research_questions(self, **kwargs) -> List[ResearchQuestion]:
        """List research questions with filters."""
        return self._question_service.list(filters=kwargs)

    # Add delegation for all other methods...
    def set_reference_validator(self, validator_callback):
        self._task_service.set_reference_validator(validator_callback)

    def set_dataset_validator(self, validator_callback):
        self._task_service.set_dataset_validator(validator_callback)

    def set_environment_validator(self, validator_callback):
        self._task_service.set_environment_validator(validator_callback)

    def set_experiment_validator(self, validator_callback):
        self._task_service.set_experiment_validator(validator_callback)

    def add_reference_to_task(self, task_id: UUID, reference_id: UUID) -> bool:
        return self._task_service.add_reference_to_task(task_id, reference_id)

    def remove_reference_from_task(self, task_id: UUID, reference_id: UUID) -> bool:
        return self._task_service.remove_reference_from_task(task_id, reference_id)

    def get_task_references(self, task_id: UUID) -> Set[UUID]:
        task = self._task_service.get_or_raise(task_id)
        return task.reference_ids

    def add_dataset_to_task(self, task_id: UUID, dataset_id: UUID) -> bool:
        return self._task_service.add_dataset_to_task(task_id, dataset_id)

    def remove_dataset_from_task(self, task_id: UUID, dataset_id: UUID) -> bool:
        return self._task_service.remove_dataset_from_task(task_id, dataset_id)

    def get_task_datasets(self, task_id: UUID) -> Set[UUID]:
        task = self._task_service.get_or_raise(task_id)
        return task.dataset_ids

    def add_environment_to_task(self, task_id: UUID, environment_id: UUID) -> bool:
        return self._task_service.add_environment_to_task(task_id, environment_id)

    def remove_environment_from_task(self, task_id: UUID, environment_id: UUID) -> bool:
        return self._task_service.remove_environment_from_task(task_id, environment_id)

    def get_task_environments(self, task_id: UUID) -> Set[UUID]:
        task = self._task_service.get_or_raise(task_id)
        return task.environment_ids

    def add_experiment_to_task(self, task_id: UUID, experiment_id: UUID) -> bool:
        return self._task_service.add_experiment_to_task(task_id, experiment_id)

    def remove_experiment_from_task(self, task_id: UUID, experiment_id: UUID) -> bool:
        return self._task_service.remove_experiment_from_task(task_id, experiment_id)

    def get_task_experiments(self, task_id: UUID) -> Set[UUID]:
        task = self._task_service.get_or_raise(task_id)
        return task.experiment_ids

    def get_subtasks(self, parent_task_id: UUID) -> List[ResearchTask]:
        return self._task_service.get_subtasks(parent_task_id)


# Storage adapters to bridge old and new interfaces
class TaskStorageAdapter(BaseStorageInterface[ResearchTask]):
    """Adapter to make legacy TaskStorageInterface work with BaseStorageInterface."""

    def __init__(self, legacy_storage: TaskStorageInterface):
        self._storage = legacy_storage

    def create(self, entity: ResearchTask) -> UUID:
        return self._storage.create_task(entity)

    def get(self, entity_id: UUID) -> Optional[ResearchTask]:
        return self._storage.get_task(entity_id)

    def update(self, entity: ResearchTask) -> bool:
        return self._storage.update_task(entity)

    def delete(self, entity_id: UUID) -> bool:
        return self._storage.delete_task(entity_id)

    def list(self, query=None) -> List[ResearchTask]:
        if query and query.filters:
            return self._storage.list_tasks(**query.filters)
        return self._storage.list_tasks()

    def count(self, query=None) -> int:
        entities = self.list(query)
        return len(entities)

    def exists(self, entity_id: UUID) -> bool:
        return self.get(entity_id) is not None


class QuestionStorageAdapter(BaseStorageInterface[ResearchQuestion]):
    """Adapter to make legacy TaskStorageInterface work with BaseStorageInterface for questions."""

    def __init__(self, legacy_storage: TaskStorageInterface):
        self._storage = legacy_storage

    def create(self, entity: ResearchQuestion) -> UUID:
        return self._storage.create_research_question(entity)

    def get(self, entity_id: UUID) -> Optional[ResearchQuestion]:
        return self._storage.get_research_question(entity_id)

    def update(self, entity: ResearchQuestion) -> bool:
        return self._storage.update_research_question(entity)

    def delete(self, entity_id: UUID) -> bool:
        return self._storage.delete_research_question(entity_id)

    def list(self, query=None) -> List[ResearchQuestion]:
        if query and query.filters:
            return self._storage.list_research_questions(**query.filters)
        return self._storage.list_research_questions()

    def count(self, query=None) -> int:
        entities = self.list(query)
        return len(entities)

    def exists(self, entity_id: UUID) -> bool:
        return self.get(entity_id) is not None