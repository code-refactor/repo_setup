"""Remediation Tracker for managing vulnerability lifecycle."""

import time
import uuid
from enum import Enum
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set, Union, Tuple

from pydantic import BaseModel, Field, field_validator, model_validator

from securetask.utils.validation import ValidationError


class RemediationState(str, Enum):
    """States in the vulnerability remediation workflow."""

    OPEN = "open"  # Initial state, vulnerability identified
    ASSIGNED = "assigned"  # Vulnerability assigned for remediation
    IN_PROGRESS = "in_progress"  # Remediation in progress
    REMEDIATED = "remediated"  # Remediation implemented, awaiting verification
    VERIFICATION_FAILED = "verification_failed"  # Verification failed, needs further remediation
    VERIFIED = "verified"  # Remediation verified as effective
    CLOSED = "closed"  # Issue closed
    ACCEPTED_RISK = "accepted_risk"  # Risk accepted, no remediation planned
    DEFERRED = "deferred"  # Remediation deferred to a later date
    FALSE_POSITIVE = "false_positive"  # Determined to be a false positive
    DUPLICATE = "duplicate"  # Duplicate of another finding


class RemediationPriority(str, Enum):
    """Priority levels for vulnerability remediation."""

    CRITICAL = "critical"  # Must be fixed immediately
    HIGH = "high"  # Must be fixed in next release
    MEDIUM = "medium"  # Should be fixed soon
    LOW = "low"  # Fix when convenient


class StateTransition(BaseModel):
    """Model representing a state transition in the remediation workflow."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    finding_id: str
    from_state: Optional[RemediationState] = None
    to_state: RemediationState
    timestamp: datetime = Field(default_factory=datetime.now)
    performed_by: str
    comments: Optional[str] = None
    require_approval: bool = False
    approver: Optional[str] = None
    approval_timestamp: Optional[datetime] = None
    evidence_ids: List[str] = Field(default_factory=list)


class RemediationTask(BaseModel):
    """Model representing a remediation task for a vulnerability."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    finding_id: str
    title: str
    description: str
    priority: RemediationPriority
    state: RemediationState = RemediationState.OPEN
    assigned_to: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress_percentage: int = 0
    steps: List[Dict[str, Any]] = Field(default_factory=list)
    notes: List[Dict[str, Any]] = Field(default_factory=list)

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value):
        """Validate the priority level."""
        if isinstance(value, RemediationPriority):
            return value

        if isinstance(value, str) and value in [p.value for p in RemediationPriority]:
            return RemediationPriority(value)

        raise ValidationError(
            f"Invalid priority: {value}. Allowed values: {', '.join([p.value for p in RemediationPriority])}",
            "priority"
        )

    @field_validator("state")
    @classmethod
    def validate_state(cls, value):
        """Validate the state."""
        if isinstance(value, RemediationState):
            return value

        if isinstance(value, str) and value in [s.value for s in RemediationState]:
            return RemediationState(value)

        raise ValidationError(
            f"Invalid state: {value}. Allowed values: {', '.join([s.value for s in RemediationState])}",
            "state"
        )

    # For Pydantic v2 compatibility
    def model_validate(self, value=None):
        """Compatibility method for Pydantic v2."""
        # In Pydantic v2, you need to pass the value to validate
        if value is None:
            # If no value is provided, validate the current instance
            self.validate_priority(self.priority)
            self.validate_state(self.state)
            return self
        else:
            # If value is provided, create a new instance
            if isinstance(value, dict):
                return RemediationTask(**value)
            return value

    def validate(self, value=None):
        """Backward compatibility method for validate in tests."""
        return self.model_validate(value)
    
    def add_step(self, title: str, description: str, estimate_hours: Optional[float] = None) -> Dict[str, Any]:
        """
        Add a remediation step to this task.
        
        Args:
            title: Step title
            description: Step description
            estimate_hours: Estimated hours to complete
            
        Returns:
            The created step
        """
        step = {
            "id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "estimate_hours": estimate_hours,
            "completed": False,
            "created_at": datetime.now()
        }
        
        self.steps.append(step)
        return step
    
    def complete_step(self, step_id: str, completed_by: str) -> bool:
        """
        Mark a step as completed.
        
        Args:
            step_id: ID of the step to complete
            completed_by: ID of the user completing the step
            
        Returns:
            True if step was found and completed, False otherwise
        """
        for step in self.steps:
            if step["id"] == step_id:
                step["completed"] = True
                step["completed_at"] = datetime.now()
                step["completed_by"] = completed_by
                
                # Recalculate progress percentage
                self._update_progress()
                
                return True
                
        return False
    
    def add_note(self, content: str, author: str) -> Dict[str, Any]:
        """
        Add a note to the remediation task.
        
        Args:
            content: Note content
            author: Note author
            
        Returns:
            The created note
        """
        note = {
            "id": str(uuid.uuid4()),
            "content": content,
            "author": author,
            "timestamp": datetime.now()
        }
        
        self.notes.append(note)
        return note
    
    def _update_progress(self) -> None:
        """Update the progress percentage based on completed steps."""
        if not self.steps:
            self.progress_percentage = 0
            return
            
        completed = sum(1 for step in self.steps if step.get("completed", False))
        self.progress_percentage = int((completed / len(self.steps)) * 100)


class WorkflowEngine:
    """
    Engine for managing the vulnerability remediation workflow.
    
    Manages state transitions, tasks, and approval processes for 
    vulnerability remediation.
    """
    
    def __init__(self):
        """Initialize the workflow engine with the valid state transitions."""
        # Define allowed state transitions
        self.allowed_transitions = {
            None: {RemediationState.OPEN},  # Initial state
            RemediationState.OPEN: {
                RemediationState.ASSIGNED, RemediationState.ACCEPTED_RISK, 
                RemediationState.FALSE_POSITIVE, RemediationState.DUPLICATE
            },
            RemediationState.ASSIGNED: {
                RemediationState.IN_PROGRESS, RemediationState.DEFERRED,
                RemediationState.ACCEPTED_RISK, RemediationState.FALSE_POSITIVE,
                RemediationState.DUPLICATE
            },
            RemediationState.IN_PROGRESS: {
                RemediationState.REMEDIATED, RemediationState.DEFERRED,
                RemediationState.ACCEPTED_RISK, RemediationState.FALSE_POSITIVE,
                RemediationState.DUPLICATE
            },
            RemediationState.REMEDIATED: {
                RemediationState.VERIFIED, RemediationState.VERIFICATION_FAILED
            },
            RemediationState.VERIFICATION_FAILED: {
                RemediationState.IN_PROGRESS, RemediationState.ASSIGNED,
                RemediationState.ACCEPTED_RISK
            },
            RemediationState.VERIFIED: {RemediationState.CLOSED},
            RemediationState.CLOSED: set(),  # Terminal state
            RemediationState.ACCEPTED_RISK: {RemediationState.OPEN},  # Can be reopened
            RemediationState.DEFERRED: {RemediationState.OPEN, RemediationState.ASSIGNED},
            RemediationState.FALSE_POSITIVE: set(),  # Terminal state
            RemediationState.DUPLICATE: set()  # Terminal state
        }
        
        # Define states requiring approval
        self.approval_required = {
            RemediationState.ACCEPTED_RISK,
            RemediationState.VERIFIED,
            RemediationState.CLOSED
        }
    
    def is_valid_transition(self, from_state: Optional[Union[RemediationState, str]], to_state: Union[RemediationState, str]) -> bool:
        """
        Check if a state transition is valid.
        
        Args:
            from_state: Current state
            to_state: Target state
            
        Returns:
            True if the transition is valid, False otherwise
        """
        # Handle string values
        if isinstance(from_state, str):
            try:
                from_state = RemediationState(from_state)
            except ValueError:
                return False
                
        if isinstance(to_state, str):
            try:
                to_state = RemediationState(to_state)
            except ValueError:
                return False
                
        # Special case to handle the same state transition
        if from_state == to_state:
            return True
        
        if from_state not in self.allowed_transitions:
            return False
            
        return to_state in self.allowed_transitions[from_state]
    
    def requires_approval(self, to_state: Union[RemediationState, str]) -> bool:
        """
        Check if a state transition requires approval.
        
        Args:
            to_state: Target state
            
        Returns:
            True if approval is required, False otherwise
        """
        if isinstance(to_state, str):
            try:
                to_state = RemediationState(to_state)
            except ValueError:
                return False
                
        return to_state in self.approval_required
    
    def transition(
        self,
        task: RemediationTask,
        to_state: Union[RemediationState, str],
        performed_by: str,
        comments: Optional[str] = None,
        evidence_ids: Optional[List[str]] = None,
        approver: Optional[str] = None
    ) -> Tuple[RemediationTask, StateTransition]:
        """
        Transition a remediation task to a new state.
        
        Args:
            task: The remediation task to transition
            to_state: The target state
            performed_by: ID of the user performing the transition
            comments: Optional comments about the transition
            evidence_ids: Optional list of evidence IDs
            approver: Optional ID of the approver (required for some transitions)
            
        Returns:
            Tuple of (updated task, state transition record)
            
        Raises:
            ValidationError: If the transition is invalid
        """
        start_time = time.time()
        
        # Convert string to enum if needed
        if isinstance(to_state, str):
            try:
                to_state = RemediationState(to_state)
            except ValueError:
                raise ValidationError(f"Invalid state: {to_state}", "to_state")
        
        # Special case to handle the same state transition
        if task.state == to_state:
            # Create a state transition record anyway but mark it as a no-op
            transition = StateTransition(
                finding_id=task.finding_id,
                from_state=task.state,
                to_state=to_state,
                performed_by=performed_by,
                comments=comments or "No state change",
                evidence_ids=evidence_ids or []
            )
            return task, transition
        
        # Check if transition is valid
        if not self.is_valid_transition(task.state, to_state):
            raise ValidationError(
                f"Invalid state transition from {task.state} to {to_state}",
                "to_state"
            )
        
        # Check if approval is required
        require_approval = self.requires_approval(to_state)
        
        if require_approval and not approver:
            raise ValidationError(
                f"Transition to {to_state} requires approval",
                "approver"
            )
        
        # Create state transition record
        transition = StateTransition(
            finding_id=task.finding_id,
            from_state=task.state,
            to_state=to_state,
            performed_by=performed_by,
            comments=comments,
            require_approval=require_approval,
            approver=approver,
            approval_timestamp=datetime.now() if approver else None,
            evidence_ids=evidence_ids or []
        )
        
        # Update task state
        task.state = to_state
        
        # Handle special state transitions
        if to_state == RemediationState.ASSIGNED and not task.assigned_to:
            task.assigned_to = performed_by
            
        if to_state == RemediationState.CLOSED:
            task.completed_at = datetime.now()
            task.progress_percentage = 100
            
        if to_state == RemediationState.REMEDIATED:
            task.progress_percentage = 100
            
        execution_time = time.time() - start_time
        if execution_time > 0.05:  # 50ms
            print(f"Warning: State transition took {execution_time*1000:.2f}ms")
            
        return task, transition