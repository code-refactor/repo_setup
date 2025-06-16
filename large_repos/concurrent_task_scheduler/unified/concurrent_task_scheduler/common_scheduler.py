"""Common library compatible scheduler for Scientific Computing implementation."""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from common.core.scheduler import BaseScheduler
from common.core.models import BaseTask, BaseNode, Priority, TaskStatus
from .adapters import TaskAdapter, NodeAdapter, StatusAdapter
from .models.simulation import Simulation, SimulationStage, ComputeNode, SimulationPriority


class ScientificComputingScheduler(BaseScheduler):
    """
    Scientific computing scheduler that extends common library BaseScheduler.
    
    This scheduler bridges scientific computing specific logic with common library interfaces
    while preserving all domain-specific optimizations like research prioritization,
    long-running job management, and resource forecasting.
    """
    
    def __init__(
        self,
        enable_preemption: bool = True,
        research_priority_weight: float = 0.3,
        deadline_awareness: bool = True
    ):
        """
        Initialize the scientific computing scheduler.
        
        Args:
            enable_preemption: Whether to enable job preemption
            research_priority_weight: Weight for scientific promise in scheduling decisions
            deadline_awareness: Whether to consider deadlines in scheduling
        """
        super().__init__()
        self.enable_preemption = enable_preemption
        self.research_priority_weight = research_priority_weight
        self.deadline_awareness = deadline_awareness
        self.logger = logging.getLogger("scientific_computing.common_scheduler")
        
        # Override priority weights to include scientific computing priorities
        self.priority_weights.update({
            Priority.LOW: 1,
            Priority.MEDIUM: 2,
            Priority.HIGH: 3,
            Priority.CRITICAL: 4
        })
    
    def schedule_tasks(self, tasks: List[BaseTask], nodes: List[BaseNode]) -> Dict[str, str]:
        """
        Schedule tasks using scientific computing specific logic with common library models.
        
        Args:
            tasks: List of BaseTask instances to schedule
            nodes: List of BaseNode instances available for scheduling
            
        Returns:
            Dictionary mapping task IDs to node IDs
        """
        # Convert to scientific computing models for domain-specific logic
        compute_nodes = [self._base_node_to_compute_node(node) for node in nodes]
        
        # Separate simulation-level tasks from stage-level tasks
        simulation_tasks = []
        stage_tasks = []
        
        for task in tasks:
            if task.metadata.get('entity_type') == 'simulation':
                simulation_tasks.append(task)
            else:
                stage_tasks.append(task)
        
        # Schedule stages first (they are the actual work units)
        stage_scheduling = self._schedule_stages(stage_tasks, compute_nodes)
        
        # Handle simulation-level scheduling if needed
        simulation_scheduling = self._schedule_simulations(simulation_tasks, compute_nodes)
        
        # Combine results
        scheduling_result = {**stage_scheduling, **simulation_scheduling}
        
        self.logger.info(f"Scheduled {len(scheduling_result)} tasks to {len(nodes)} nodes")
        return scheduling_result
    
    def update_priorities(self, tasks: List[BaseTask]) -> List[BaseTask]:
        """
        Update task priorities using scientific computing specific logic.
        
        Args:
            tasks: List of BaseTask instances
            
        Returns:
            List of updated BaseTask instances with adjusted priorities
        """
        updated_tasks = []
        
        for task in tasks:
            updated_task = task.model_copy()
            
            # Apply scientific promise boost
            scientific_promise = task.metadata.get('scientific_promise', 0.5)
            if scientific_promise > 0.8:  # High scientific promise
                if task.priority != Priority.CRITICAL:
                    updated_task.priority = Priority(min(task.priority.value + 1, 4))
            elif scientific_promise < 0.2:  # Low scientific promise
                if task.priority != Priority.LOW:
                    updated_task.priority = Priority(max(task.priority.value - 1, 1))
            
            # Apply aging for waiting tasks
            if task.status == TaskStatus.QUEUED:
                wait_time = (datetime.now() - task.submission_time).total_seconds()
                if wait_time > 2 * 3600:  # 2 hours
                    if task.priority != Priority.CRITICAL:
                        updated_task.priority = Priority(min(task.priority.value + 1, 4))
            
            updated_tasks.append(updated_task)
        
        return updated_tasks
    
    def can_meet_deadline(self, task: BaseTask, nodes: List[BaseNode]) -> bool:
        """
        Check if a task can meet its deadline using scientific computing logic.
        
        Args:
            task: The BaseTask to evaluate
            nodes: List of available BaseNode instances
            
        Returns:
            True if the deadline can be met, False otherwise
        """
        if not self.deadline_awareness:
            return True
        
        # Check if task has a deadline
        if 'deadline' not in task.metadata:
            return True
        
        try:
            deadline = datetime.fromisoformat(task.metadata['deadline'])
            time_until_deadline = (deadline - datetime.now()).total_seconds()
            
            # Add safety margin for scientific computing (30% extra time)
            estimated_time_with_margin = task.estimated_duration.total_seconds() * 1.3
            
            return estimated_time_with_margin <= time_until_deadline
        except (ValueError, TypeError):
            # If deadline parsing fails, assume it can be met
            return True
    
    def should_preempt(self, running_task: BaseTask, pending_task: BaseTask) -> bool:
        """
        Determine if a running task should be preempted using scientific computing logic.
        
        Args:
            running_task: The currently running BaseTask
            pending_task: The BaseTask that might preempt the running task
            
        Returns:
            True if the running task should be preempted, False otherwise
        """
        if not self.enable_preemption:
            return False
        
        # Critical tasks can preempt non-critical tasks
        if (pending_task.priority == Priority.CRITICAL and 
            running_task.priority != Priority.CRITICAL):
            return True
        
        # High scientific promise can preempt lower promise work
        pending_promise = pending_task.metadata.get('scientific_promise', 0.5)
        running_promise = running_task.metadata.get('scientific_promise', 0.5)
        
        if (pending_promise > 0.9 and running_promise < 0.3 and
            pending_task.priority.value >= running_task.priority.value):
            return True
        
        # Don't preempt tasks that are nearly complete
        if running_task.progress > 0.8:
            return False
        
        return False
    
    def _schedule_stages(self, stage_tasks: List[BaseTask], nodes: List[ComputeNode]) -> Dict[str, str]:
        """Schedule simulation stages to compute nodes."""
        scheduling = {}
        available_nodes = [node for node in nodes if node.is_available()]
        
        # Sort tasks by priority and scientific promise
        def task_score(task):
            base_score = self.priority_weights[task.priority]
            scientific_promise = task.metadata.get('scientific_promise', 0.5)
            return base_score + (scientific_promise * self.research_priority_weight)
        
        sorted_tasks = sorted(stage_tasks, key=task_score, reverse=True)
        
        for task in sorted_tasks:
            # Skip tasks that aren't ready to run
            if task.status not in [TaskStatus.PENDING, TaskStatus.QUEUED]:
                continue
            
            # Find best node for this task
            best_node = self._find_best_node_for_task(task, available_nodes)
            if best_node:
                scheduling[task.id] = best_node.id
                # Remove node from available list (simplified - could track partial allocation)
                available_nodes = [n for n in available_nodes if n.id != best_node.id]
        
        return scheduling
    
    def _schedule_simulations(self, simulation_tasks: List[BaseTask], nodes: List[ComputeNode]) -> Dict[str, str]:
        """Handle simulation-level scheduling (mostly informational)."""
        # For now, simulation-level tasks are not directly scheduled to nodes
        # They represent collections of stages
        return {}
    
    def _find_best_node_for_task(self, task: BaseTask, nodes: List[ComputeNode]) -> Optional[ComputeNode]:
        """Find the best node for a task based on resource requirements and characteristics."""
        suitable_nodes = []
        
        # Get resource requirements from metadata
        resource_requirements = task.metadata.get('resource_requirements', {})
        
        for node in nodes:
            # Check basic resource availability
            if not self._node_can_accommodate_task(node, resource_requirements):
                continue
            
            # Check if node is reliable enough for long-running tasks
            if node.reliability_score < 0.7:  # Require high reliability
                continue
            
            suitable_nodes.append(node)
        
        if not suitable_nodes:
            return None
        
        # Sort by reliability and resource availability
        def node_score(node):
            reliability_score = node.reliability_score
            # Prefer nodes with more available resources
            available_resources = node.get_available_resources()
            resource_score = (
                available_resources.get('cpu', 0) +
                available_resources.get('memory', 0) * 0.1 +
                available_resources.get('gpu', 0) * 2
            )
            return reliability_score * 100 + resource_score
        
        return max(suitable_nodes, key=node_score)
    
    def _node_can_accommodate_task(self, node: ComputeNode, resource_requirements: Dict[str, float]) -> bool:
        """Check if a node can accommodate a task's resource requirements."""
        available = node.get_available_resources()
        
        for resource_type, required_amount in resource_requirements.items():
            # Map to scientific computing resource types
            resource_map = {
                'cpu': 'cpu',
                'memory': 'memory',
                'gpu': 'gpu',
                'storage': 'storage'
            }
            
            if resource_type in resource_map:
                available_amount = available.get(resource_map[resource_type], 0)
                if available_amount < required_amount:
                    return False
        
        return True
    
    def _base_node_to_compute_node(self, base_node: BaseNode) -> ComputeNode:
        """Convert BaseNode to ComputeNode for scientific computing logic."""
        return NodeAdapter.base_node_to_compute_node(base_node)
    
    def calculate_task_score(self, task: BaseTask) -> float:
        """Calculate enhanced scoring that includes scientific computing factors."""
        base_score = super().calculate_task_score(task)
        
        # Add scientific promise factor
        scientific_promise = task.metadata.get('scientific_promise', 0.5)
        promise_bonus = scientific_promise * self.research_priority_weight * 10
        
        # Add project priority factor
        project = task.metadata.get('project', '')
        project_bonus = 5 if project.startswith('critical_') else 0
        
        return base_score + promise_bonus + project_bonus