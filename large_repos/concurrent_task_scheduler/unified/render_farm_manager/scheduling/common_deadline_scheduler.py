"""Common library compatible deadline scheduler for Render Farm Manager."""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from common.core.scheduler import BaseScheduler
from common.core.models import BaseTask, BaseNode
from render_farm_manager.adapters import TaskAdapter, NodeAdapter
from render_farm_manager.core.models import JobPriority, RenderJob, RenderJobStatus, RenderNode
from render_farm_manager.utils.logging import AuditLogger, PerformanceMonitor


class CommonDeadlineScheduler(BaseScheduler):
    """
    Deadline-driven scheduler that extends common library BaseScheduler.
    
    This scheduler bridges render farm specific logic with common library interfaces
    while preserving all domain-specific optimizations like energy awareness,
    deadline handling, and preemption logic.
    """
    
    def __init__(
        self, 
        audit_logger: Optional[AuditLogger] = None,
        performance_monitor: Optional[PerformanceMonitor] = None,
        deadline_safety_margin_hours: float = 2.0,
        enable_preemption: bool = True,
    ):
        """
        Initialize the common deadline scheduler.
        
        Args:
            audit_logger: Logger for audit trail events (render farm specific)
            performance_monitor: Monitor for tracking scheduler performance
            deadline_safety_margin_hours: Safety margin to add to estimated job duration
            enable_preemption: Whether to enable job preemption
        """
        super().__init__()
        self.audit_logger = audit_logger
        self.performance_monitor = performance_monitor
        self.deadline_safety_margin_hours = deadline_safety_margin_hours
        self.enable_preemption = enable_preemption
        self.logger = logging.getLogger("render_farm.common_scheduler")
        
        # Store effective priorities for priority inheritance
        self._effective_priorities = {}
    
    def schedule_tasks(self, tasks: List[BaseTask], nodes: List[BaseNode]) -> Dict[str, str]:
        """
        Schedule tasks using render farm specific logic with common library models.
        
        Args:
            tasks: List of BaseTask instances to schedule
            nodes: List of BaseNode instances available for scheduling
            
        Returns:
            Dictionary mapping task IDs to node IDs
        """
        # Convert to render farm models for domain-specific logic
        render_jobs = [self._base_task_to_render_job(task) for task in tasks]
        render_nodes = [self._base_node_to_render_node(node) for node in nodes]
        
        # Use render farm specific scheduling logic
        job_to_node_mapping = self._schedule_render_jobs(render_jobs, render_nodes)
        
        # Log scheduling results if audit logger is available
        if self.audit_logger:
            for job_id, node_id in job_to_node_mapping.items():
                self.audit_logger.log_event(
                    "common_job_scheduled",
                    f"Job {job_id} scheduled to node {node_id} via common scheduler",
                    job_id=job_id,
                    node_id=node_id,
                )
        
        return job_to_node_mapping
    
    def update_priorities(self, tasks: List[BaseTask]) -> List[BaseTask]:
        """
        Update task priorities using render farm specific logic.
        
        Args:
            tasks: List of BaseTask instances
            
        Returns:
            List of updated BaseTask instances with adjusted priorities
        """
        # Convert to render farm models
        render_jobs = [self._base_task_to_render_job(task) for task in tasks]
        
        # Apply render farm priority logic
        updated_jobs = self._update_render_job_priorities(render_jobs)
        
        # Convert back to BaseTask and update original tasks
        updated_tasks = []
        for i, task in enumerate(tasks):
            updated_job = updated_jobs[i]
            # Update the original task with new priority and metadata
            updated_task = task.model_copy()
            updated_task.priority = TaskAdapter.render_job_to_base_task(updated_job).priority
            updated_task.metadata = TaskAdapter.render_job_to_base_task(updated_job).metadata
            updated_tasks.append(updated_task)
        
        return updated_tasks
    
    def can_meet_deadline(self, task: BaseTask, nodes: List[BaseNode]) -> bool:
        """
        Check if a task can meet its deadline using render farm logic.
        
        Args:
            task: The BaseTask to evaluate
            nodes: List of available BaseNode instances
            
        Returns:
            True if the deadline can be met, False otherwise
        """
        # Convert to render farm models
        render_job = self._base_task_to_render_job(task)
        render_nodes = [self._base_node_to_render_node(node) for node in nodes]
        
        # Use render farm deadline checking logic
        return self._can_meet_render_deadline(render_job, render_nodes)
    
    def should_preempt(self, running_task: BaseTask, pending_task: BaseTask) -> bool:
        """
        Determine if a running task should be preempted using render farm logic.
        
        Args:
            running_task: The currently running BaseTask
            pending_task: The BaseTask that might preempt the running task
            
        Returns:
            True if the running task should be preempted, False otherwise
        """
        if not self.enable_preemption:
            return False
        
        # Convert to render farm models
        running_job = self._base_task_to_render_job(running_task)
        pending_job = self._base_task_to_render_job(pending_task)
        
        # Use render farm preemption logic
        return self._should_preempt_render_job(running_job, pending_job)
    
    def _base_task_to_render_job(self, task: BaseTask) -> RenderJob:
        """Convert BaseTask to RenderJob for domain-specific processing."""
        # Try to get from metadata if it exists
        if 'render_job_cache' in task.metadata:
            # If we have a cached version, use task adapter to update it
            cached_job = task.metadata['render_job_cache']
            return TaskAdapter.base_task_to_render_job(task, cached_job)
        else:
            # Create new render job from task
            return TaskAdapter.base_task_to_render_job(task)
    
    def _base_node_to_render_node(self, node: BaseNode) -> RenderNode:
        """Convert BaseNode to RenderNode for domain-specific processing."""
        # Try to get from cache if available
        if hasattr(node, '_render_node_cache'):
            cached_node = node._render_node_cache
            return NodeAdapter.base_node_to_render_node(node, cached_node)
        else:
            return NodeAdapter.base_node_to_render_node(node)
    
    def _schedule_render_jobs(self, jobs: List[RenderJob], nodes: List[RenderNode]) -> Dict[str, str]:
        """
        Core render farm scheduling logic adapted from DeadlineScheduler.
        This preserves all the domain-specific logic while working with common models.
        """
        # Update job priorities based on deadlines
        updated_jobs = self._update_render_job_priorities(jobs)
        
        # Filter jobs by eligibility (similar to original logic)
        eligible_jobs = []
        for job in updated_jobs:
            # Skip jobs that aren't pending or queued
            if job.status not in [RenderJobStatus.PENDING, RenderJobStatus.QUEUED]:
                continue
            
            # Check dependencies
            if job.dependencies:
                all_deps_completed = True
                for dep_id in job.dependencies:
                    dep_job = next((j for j in jobs if j.id == dep_id), None)
                    if dep_job is None:
                        continue
                    
                    # Use same dependency logic as original scheduler
                    if dep_job.status == RenderJobStatus.RUNNING and dep_job.progress >= 50.0:
                        continue
                    if dep_job.status != RenderJobStatus.COMPLETED:
                        all_deps_completed = False
                        break
                
                if not all_deps_completed:
                    continue
            
            eligible_jobs.append(job)
        
        # Sort by priority and deadline (preserve effective priorities)
        def get_effective_priority(job):
            if job.id in self._effective_priorities:
                return self._get_priority_value(self._effective_priorities[job.id])
            return self._get_priority_value(job.priority)
        
        sorted_jobs = sorted(
            eligible_jobs,
            key=lambda j: (
                get_effective_priority(j),
                (j.deadline - datetime.now()).total_seconds(),
            ),
            reverse=True,
        )
        
        # Get available nodes
        available_nodes = [
            node for node in nodes 
            if node.status == "online" and node.current_job_id is None
        ]
        
        # Schedule jobs
        scheduled_jobs: Dict[str, str] = {}
        
        for job in sorted_jobs:
            assigned_node = self._find_suitable_node(job, available_nodes)
            
            if assigned_node:
                scheduled_jobs[job.id] = assigned_node.id
                available_nodes = [node for node in available_nodes if node.id != assigned_node.id]
        
        return scheduled_jobs
    
    def _update_render_job_priorities(self, jobs: List[RenderJob]) -> List[RenderJob]:
        """Update render job priorities with deadline and dependency logic."""
        now = datetime.now()
        updated_jobs = []
        jobs_by_id = {job.id: job for job in jobs}
        
        for job in jobs:
            if job.status in [RenderJobStatus.COMPLETED, RenderJobStatus.FAILED, RenderJobStatus.CANCELLED]:
                updated_jobs.append(job)
                continue
            
            original_priority = job.priority
            time_until_deadline = (job.deadline - now).total_seconds()
            estimated_time_needed = job.estimated_duration_hours * 3600 * (1 - job.progress / 100)
            
            # Add safety margin
            estimated_time_with_margin = estimated_time_needed + (self.deadline_safety_margin_hours * 3600)
            
            # Adjust priority based on deadline proximity
            if estimated_time_with_margin >= time_until_deadline:
                if job.priority == JobPriority.HIGH:
                    job.priority = JobPriority.CRITICAL
                elif job.priority == JobPriority.MEDIUM:
                    job.priority = JobPriority.HIGH
                elif job.priority == JobPriority.LOW:
                    job.priority = JobPriority.MEDIUM
            elif time_until_deadline < 24 * 3600:  # Less than 24 hours
                if job.priority == JobPriority.MEDIUM:
                    job.priority = JobPriority.HIGH
                elif job.priority == JobPriority.LOW:
                    job.priority = JobPriority.MEDIUM
            
            # Priority inheritance from dependencies
            if job.dependencies:
                parent_priorities = []
                for dep_id in job.dependencies:
                    if dep_id in jobs_by_id:
                        parent_job = jobs_by_id[dep_id]
                        parent_priorities.append(parent_job.priority)
                
                if parent_priorities:
                    parent_priorities.sort(key=self._get_priority_value, reverse=True)
                    highest_parent_priority = parent_priorities[0]
                    
                    if self._get_priority_value(highest_parent_priority) > self._get_priority_value(job.priority):
                        self._effective_priorities[job.id] = highest_parent_priority
            
            updated_jobs.append(job)
        
        return updated_jobs
    
    def _can_meet_render_deadline(self, job: RenderJob, available_nodes: List[RenderNode]) -> bool:
        """Check if render job can meet deadline."""
        now = datetime.now()
        time_until_deadline = (job.deadline - now).total_seconds() / 3600
        estimated_duration = job.estimated_duration_hours * (1 - job.progress / 100)
        
        estimated_duration_with_margin = estimated_duration + self.deadline_safety_margin_hours
        
        if estimated_duration_with_margin > time_until_deadline:
            return False
        
        suitable_node = self._find_suitable_node(job, available_nodes)
        return suitable_node is not None
    
    def _should_preempt_render_job(self, running_job: RenderJob, pending_job: RenderJob) -> bool:
        """Determine if render job should be preempted."""
        if not running_job.can_be_preempted:
            return False
        
        # Critical jobs can preempt lower priority jobs
        if pending_job.priority == JobPriority.CRITICAL and running_job.priority != JobPriority.CRITICAL:
            return True
        
        # Check deadline urgency
        now = datetime.now()
        pending_deadline_time = (pending_job.deadline - now).total_seconds() / 3600
        pending_estimated_time = pending_job.estimated_duration_hours * (1 - pending_job.progress / 100)
        
        running_deadline_time = (running_job.deadline - now).total_seconds() / 3600
        running_estimated_time = running_job.estimated_duration_hours * (1 - running_job.progress / 100)
        
        pending_will_miss = pending_estimated_time + self.deadline_safety_margin_hours > pending_deadline_time
        running_will_complete = running_estimated_time + self.deadline_safety_margin_hours < running_deadline_time
        
        if (self._get_priority_value(pending_job.priority) > self._get_priority_value(running_job.priority) 
                and pending_will_miss):
            return True
        
        return False
    
    def _find_suitable_node(self, job: RenderJob, nodes: List[RenderNode]) -> Optional[RenderNode]:
        """Find suitable node for job based on requirements."""
        suitable_nodes = []
        
        for node in nodes:
            # Check GPU requirement
            if job.requires_gpu and (node.capabilities.gpu_count == 0 or not node.capabilities.gpu_model):
                continue
            
            # Check memory requirement
            if job.memory_requirements_gb > node.capabilities.memory_gb:
                continue
            
            # Check CPU requirement
            if job.cpu_requirements > node.capabilities.cpu_cores:
                continue
            
            suitable_nodes.append(node)
        
        if not suitable_nodes:
            return None
        
        # Sort by power efficiency
        suitable_nodes.sort(key=lambda n: n.power_efficiency_rating, reverse=True)
        return suitable_nodes[0]
    
    def _get_priority_value(self, priority: JobPriority) -> int:
        """Get numeric value for priority."""
        priority_values = {
            JobPriority.CRITICAL: 4,
            JobPriority.HIGH: 3,
            JobPriority.MEDIUM: 2,
            JobPriority.LOW: 1,
        }
        return priority_values.get(priority, 0)