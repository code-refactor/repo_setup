"""Remediation tracking system for vulnerability management."""

import os
import json
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set, Union, Tuple

from pydantic import ValidationError as PydanticValidationError

from securetask.remediation.workflow import (
    RemediationTask, StateTransition, RemediationState, 
    RemediationPriority, WorkflowEngine
)
from securetask.utils.crypto import CryptoManager
from securetask.utils.validation import ValidationError


class RemediationTracker:
    """
    System for tracking vulnerability remediation progress.
    
    Manages remediation tasks, workflow state transitions, and reporting on
    remediation status across security findings.
    """
    
    def __init__(self, storage_dir: str, crypto_manager: Optional[CryptoManager] = None):
        """
        Initialize the remediation tracker.
        
        Args:
            storage_dir: Directory where remediation data will be stored
            crypto_manager: Optional crypto manager for encryption
        """
        self.storage_dir = storage_dir
        self.crypto_manager = crypto_manager or CryptoManager()
        self.workflow_engine = WorkflowEngine()
        
        # Set up directories
        self.tasks_dir = os.path.join(storage_dir, "tasks")
        self.transitions_dir = os.path.join(storage_dir, "transitions")
        
        os.makedirs(self.tasks_dir, exist_ok=True)
        os.makedirs(self.transitions_dir, exist_ok=True)
    
    def create_task(
        self,
        finding_id: str,
        title: str,
        description: str,
        priority: Union[RemediationPriority, str],
        created_by: str,
        due_date: Optional[datetime] = None,
        assigned_to: Optional[str] = None,
        initial_state: RemediationState = RemediationState.OPEN
    ) -> RemediationTask:
        """
        Create a new remediation task for a finding.
        
        Args:
            finding_id: ID of the finding to create a task for
            title: Task title
            description: Task description
            priority: Task priority
            created_by: ID of the user creating the task
            due_date: Optional due date for the task
            assigned_to: Optional ID of user assigned to the task
            initial_state: Initial state for the task
            
        Returns:
            The created remediation task
            
        Raises:
            ValidationError: If validation fails
        """
        start_time = time.time()
        
        try:
            # Create the task with initial OPEN state
            task = RemediationTask(
                finding_id=finding_id,
                title=title,
                description=description,
                priority=priority,
                state=RemediationState.OPEN,
                assigned_to=assigned_to,
                due_date=due_date
            )
            
            # Add initial note
            task.add_note(
                content=f"Task created with priority {priority} and initial state open",
                author=created_by
            )
            
            # Save the task initially
            self._save_task(task)
            
            # If the initial state is not OPEN or we need to assign a user, transition the task
            if initial_state != RemediationState.OPEN or assigned_to:
                comments = f"Task assigned to {assigned_to}" if assigned_to else None
                task, transition = self.workflow_engine.transition(
                    task=task,
                    to_state=initial_state,
                    performed_by=created_by,
                    comments=comments
                )
                
                # Save the transition
                self._save_transition(transition)
                
                # Save the updated task
                self._save_task(task)
            
            execution_time = time.time() - start_time
            if execution_time > 0.05:  # 50ms
                print(f"Warning: Task creation took {execution_time*1000:.2f}ms")
                
            return task
            
        except PydanticValidationError as e:
            raise ValidationError(str(e))
    
    def get_task(self, task_id: str) -> RemediationTask:
        """
        Retrieve a remediation task by ID.
        
        Args:
            task_id: ID of the task to retrieve
            
        Returns:
            The retrieved task
            
        Raises:
            FileNotFoundError: If the task does not exist
        """
        file_path = os.path.join(self.tasks_dir, f"{task_id}.json.enc")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Task not found: {task_id}")
        
        # Load and decrypt
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
        
        # Load HMAC digest
        digest_path = os.path.join(self.tasks_dir, f"{task_id}.hmac")
        with open(digest_path, "rb") as f:
            digest = f.read()
        
        decrypted_data = self.crypto_manager.decrypt(encrypted_data, digest)
        task_dict = json.loads(decrypted_data.decode())

        # Create the RemediationTask object directly rather than using model_validate on the dict
        return RemediationTask(**task_dict)
    
    def update_task(self, task: RemediationTask) -> RemediationTask:
        """
        Update an existing remediation task.
        
        Args:
            task: The task to update
            
        Returns:
            The updated task
            
        Raises:
            FileNotFoundError: If the task does not exist
            ValidationError: If validation fails
        """
        start_time = time.time()
        
        # Check if task exists
        file_path = os.path.join(self.tasks_dir, f"{task.id}.json.enc")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Task not found: {task.id}")
        
        try:
            # Save the updated task
            self._save_task(task)
            
            execution_time = time.time() - start_time
            if execution_time > 0.05:  # 50ms
                print(f"Warning: Task update took {execution_time*1000:.2f}ms")
            
            return task
            
        except PydanticValidationError as e:
            raise ValidationError(str(e))
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a remediation task.
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            True if deleted, False if not found
        """
        file_path = os.path.join(self.tasks_dir, f"{task_id}.json.enc")
        digest_path = os.path.join(self.tasks_dir, f"{task_id}.hmac")
        
        if not os.path.exists(file_path):
            return False
        
        # Delete the task file and digest
        os.remove(file_path)
        if os.path.exists(digest_path):
            os.remove(digest_path)
            
        # Delete related transitions
        for filename in os.listdir(self.transitions_dir):
            if filename.endswith(".json.enc"):
                try:
                    transition_id = filename.replace(".json.enc", "")
                    transition = self.get_transition(transition_id)
                    
                    # If this transition belongs to the deleted task
                    task = self.get_task_by_finding(transition.finding_id)
                    if task and task.id == task_id:
                        # Delete this transition too
                        transition_path = os.path.join(self.transitions_dir, filename)
                        transition_digest = os.path.join(self.transitions_dir, f"{transition_id}.hmac")
                        
                        os.remove(transition_path)
                        if os.path.exists(transition_digest):
                            os.remove(transition_digest)
                except Exception:
                    # Ignore errors and continue
                    pass
                    
        return True
    
    def transition_task(
        self,
        task_id: str,
        to_state: Union[RemediationState, str],
        performed_by: str,
        comments: Optional[str] = None,
        evidence_ids: Optional[List[str]] = None,
        approver: Optional[str] = None,
        assigned_to: Optional[str] = None  # Added assigned_to parameter
    ) -> Tuple[RemediationTask, StateTransition]:
        """
        Transition a task to a new state.

        Args:
            task_id: ID of the task to transition
            to_state: Target state
            performed_by: ID of user performing the transition
            comments: Optional comments
            evidence_ids: Optional list of evidence IDs
            approver: Optional ID of approver (required for some transitions)
            assigned_to: Optional ID of user to assign the task to (for ASSIGNED state)

        Returns:
            Tuple of (updated task, state transition record)

        Raises:
            FileNotFoundError: If the task does not exist
            ValidationError: If the transition is invalid
        """
        start_time = time.time()

        # Get the task
        task = self.get_task(task_id)

        # Update assigned_to if provided and transitioning to ASSIGNED state
        if assigned_to is not None and (
            (isinstance(to_state, str) and to_state == "assigned") or 
            (isinstance(to_state, RemediationState) and to_state == RemediationState.ASSIGNED)
        ):
            task.assigned_to = assigned_to

        # Perform the transition
        updated_task, transition = self.workflow_engine.transition(
            task=task,
            to_state=to_state,
            performed_by=performed_by,
            comments=comments,
            evidence_ids=evidence_ids,
            approver=approver
        )
        
        # Save the transition
        self._save_transition(transition)
        
        # Save the updated task
        self._save_task(updated_task)
        
        execution_time = time.time() - start_time
        if execution_time > 0.05:  # 50ms
            print(f"Warning: Task transition took {execution_time*1000:.2f}ms")
            
        return updated_task, transition
    
    def get_transition(self, transition_id: str) -> StateTransition:
        """
        Retrieve a state transition by ID.
        
        Args:
            transition_id: ID of the transition to retrieve
            
        Returns:
            The retrieved transition
            
        Raises:
            FileNotFoundError: If the transition does not exist
        """
        file_path = os.path.join(self.transitions_dir, f"{transition_id}.json.enc")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Transition not found: {transition_id}")
        
        # Load and decrypt
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
        
        # Load HMAC digest
        digest_path = os.path.join(self.transitions_dir, f"{transition_id}.hmac")
        with open(digest_path, "rb") as f:
            digest = f.read()
        
        decrypted_data = self.crypto_manager.decrypt(encrypted_data, digest)
        transition_dict = json.loads(decrypted_data.decode())
        
        return StateTransition.model_validate(transition_dict)
    
    def get_task_by_finding(self, finding_id: str) -> Optional[RemediationTask]:
        """
        Get the remediation task for a finding.
        
        Args:
            finding_id: ID of the finding
            
        Returns:
            The remediation task or None if not found
        """
        # Find the task for this finding
        for filename in os.listdir(self.tasks_dir):
            if not filename.endswith(".json.enc"):
                continue
                
            task_id = filename.replace(".json.enc", "")
            
            try:
                task = self.get_task(task_id)
                if task.finding_id == finding_id:
                    return task
            except Exception:
                # Skip invalid tasks
                continue
                
        return None
    
    def get_transition_history(self, task_id: str) -> List[StateTransition]:
        """
        Get the full transition history for a task.
        
        Args:
            task_id: ID of the task
            
        Returns:
            List of state transitions in chronological order
        """
        # Get the task to get the finding ID
        try:
            task = self.get_task(task_id)
            finding_id = task.finding_id
        except FileNotFoundError:
            return []
        
        # Find all transitions for this finding
        transitions = []
        
        for filename in os.listdir(self.transitions_dir):
            if not filename.endswith(".json.enc"):
                continue
                
            transition_id = filename.replace(".json.enc", "")
            
            try:
                transition = self.get_transition(transition_id)
                if transition.finding_id == finding_id:
                    transitions.append(transition)
            except Exception:
                # Skip invalid transitions
                continue
        
        # Sort by timestamp
        return sorted(transitions, key=lambda t: t.timestamp)
    
    def list_tasks(
        self,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: str = "created_at",
        reverse: bool = True,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[RemediationTask]:
        """
        List tasks with optional filtering and sorting.

        Args:
            filters: Optional filters as field-value pairs
            sort_by: Field to sort by
            reverse: Whether to sort in reverse order
            limit: Maximum number of tasks to return
            offset: Number of tasks to skip

        Returns:
            List of tasks matching criteria
        """
        tasks = []
        count = 0

        # Get all task IDs from filenames
        for filename in os.listdir(self.tasks_dir):
            if not filename.endswith(".json.enc"):
                continue

            task_id = filename.replace(".json.enc", "")

            try:
                task = self.get_task(task_id)

                # Apply filters if provided
                if filters and not self._matches_filters(task, filters):
                    continue

                count += 1
                if count <= offset:
                    continue

                tasks.append(task)

                if limit and len(tasks) >= limit:
                    break

            except (FileNotFoundError, ValidationError):
                # Skip invalid files
                continue

        # Sort tasks
        if hasattr(RemediationTask, sort_by):
            # Handle title field specially to ensure alphabetical sorting
            if sort_by == "title":
                tasks.sort(key=lambda t: t.title.lower(), reverse=reverse)
            else:
                tasks.sort(key=lambda t: getattr(t, sort_by), reverse=reverse)

        return tasks
    
    def count_tasks(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count tasks matching filters.
        
        Args:
            filters: Optional filters as field-value pairs
            
        Returns:
            Number of tasks matching criteria
        """
        if not filters:
            # Just count files without loading
            return sum(1 for f in os.listdir(self.tasks_dir) if f.endswith(".json.enc"))
        
        # With filters, we need to load and check each task
        count = 0
        for filename in os.listdir(self.tasks_dir):
            if not filename.endswith(".json.enc"):
                continue
                
            task_id = filename.replace(".json.enc", "")
            
            try:
                task = self.get_task(task_id)
                if self._matches_filters(task, filters):
                    count += 1
            except (FileNotFoundError, ValidationError):
                # Skip invalid files
                continue
                
        return count
    
    def get_remediation_metrics(self) -> Dict[str, Any]:
        """
        Get metrics on remediation status across all tasks.
        
        Returns:
            Dictionary of metrics
        """
        metrics = {
            "total_tasks": 0,
            "by_state": {s.value: 0 for s in RemediationState},
            "by_priority": {p.value: 0 for p in RemediationPriority},
            "overdue_tasks": 0,
            "avg_resolution_time_days": 0,
            "avg_verification_time_days": 0,
            "tasks_requiring_approval": 0
        }
        
        # Temporary data for calculating averages
        resolution_times = []
        verification_times = []
        
        # Process all tasks
        for filename in os.listdir(self.tasks_dir):
            if not filename.endswith(".json.enc"):
                continue
                
            task_id = filename.replace(".json.enc", "")
            
            try:
                task = self.get_task(task_id)
                metrics["total_tasks"] += 1
                
                # Count by state
                metrics["by_state"][task.state.value] += 1
                
                # Count by priority
                metrics["by_priority"][task.priority.value] += 1
                
                # Check if overdue
                if task.due_date and task.due_date < datetime.now() and task.state not in [
                    RemediationState.VERIFIED, RemediationState.CLOSED,
                    RemediationState.FALSE_POSITIVE, RemediationState.DUPLICATE
                ]:
                    metrics["overdue_tasks"] += 1
                
                # Get transition history
                transitions = self.get_transition_history(task.id)
                
                # Calculate resolution time (time to remediated state)
                open_time = None
                remediated_time = None
                verified_time = None
                
                for t in transitions:
                    if t.to_state == RemediationState.OPEN:
                        open_time = t.timestamp
                    elif t.to_state == RemediationState.REMEDIATED:
                        remediated_time = t.timestamp
                    elif t.to_state == RemediationState.VERIFIED:
                        verified_time = t.timestamp
                
                # If we have both open and remediated times, calculate resolution time
                if open_time and remediated_time:
                    resolution_days = (remediated_time - open_time).total_seconds() / (60 * 60 * 24)
                    resolution_times.append(resolution_days)
                
                # If we have both remediated and verified times, calculate verification time
                if remediated_time and verified_time:
                    verification_days = (verified_time - remediated_time).total_seconds() / (60 * 60 * 24)
                    verification_times.append(verification_days)
                
                # Check if task requires approval
                if task.state in [s for s in RemediationState if self.workflow_engine.requires_approval(s)]:
                    metrics["tasks_requiring_approval"] += 1
                    
            except Exception:
                # Skip invalid tasks
                continue
        
        # Calculate averages
        if resolution_times:
            metrics["avg_resolution_time_days"] = sum(resolution_times) / len(resolution_times)
            
        if verification_times:
            metrics["avg_verification_time_days"] = sum(verification_times) / len(verification_times)
        
        return metrics
    
    def _save_task(self, task: RemediationTask) -> None:
        """
        Save a task with encryption.
        
        Args:
            task: The task to save
        """
        # Convert to JSON
        task_json = task.model_dump_json().encode()
        
        # Encrypt
        encrypted_data, digest = self.crypto_manager.encrypt(task_json)
        
        # Save encrypted data
        file_path = os.path.join(self.tasks_dir, f"{task.id}.json.enc")
        with open(file_path, "wb") as f:
            f.write(encrypted_data)
            
        # Save HMAC digest separately for integrity verification
        digest_path = os.path.join(self.tasks_dir, f"{task.id}.hmac")
        with open(digest_path, "wb") as f:
            f.write(digest)
    
    def _save_transition(self, transition: StateTransition) -> None:
        """
        Save a state transition with encryption.
        
        Args:
            transition: The transition to save
        """
        # Convert to JSON
        transition_json = transition.model_dump_json().encode()
        
        # Encrypt
        encrypted_data, digest = self.crypto_manager.encrypt(transition_json)
        
        # Save encrypted data
        file_path = os.path.join(self.transitions_dir, f"{transition.id}.json.enc")
        with open(file_path, "wb") as f:
            f.write(encrypted_data)
            
        # Save HMAC digest separately for integrity verification
        digest_path = os.path.join(self.transitions_dir, f"{transition.id}.hmac")
        with open(digest_path, "wb") as f:
            f.write(digest)
    
    def _matches_filters(self, task: RemediationTask, filters: Dict[str, Any]) -> bool:
        """
        Check if a task matches the given filters.
        
        Args:
            task: The task to check
            filters: Filters as field-value pairs
            
        Returns:
            True if the task matches all filters
        """
        for field, value in filters.items():
            if not hasattr(task, field):
                return False
                
            field_value = getattr(task, field)
            
            # Handle list fields like evidence_ids, notes
            if isinstance(field_value, list) and not isinstance(value, list):
                if value not in field_value:
                    return False
            # Handle date ranges
            elif field.endswith("_date") and isinstance(value, dict):
                if "from" in value and field_value < value["from"]:
                    return False
                if "to" in value and field_value > value["to"]:
                    return False
            # Handle enums
            elif field in ["state", "priority"] and isinstance(value, str):
                if str(field_value.value) != value:
                    return False
            # Simple equality
            elif field_value != value:
                return False
                
        return True