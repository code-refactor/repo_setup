"""Integration layer for common library compatibility in Render Farm Manager."""

import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

from common.core.interfaces import (
    SchedulerInterface as CommonSchedulerInterface,
    ResourceManagerInterface as CommonResourceManagerInterface,
    CheckpointManagerInterface,
    AuditLogInterface,
    FailureDetectorInterface,
    MetricsCollectorInterface
)
from common.core.models import BaseTask, BaseNode, BaseCheckpoint

from render_farm_manager.adapters import TaskAdapter, NodeAdapter, StatusAdapter, PriorityAdapter
from render_farm_manager.core.interfaces import (
    SchedulerInterface as RenderSchedulerInterface,
    ResourceManagerInterface as RenderResourceManagerInterface,
    EnergyOptimizationInterface,
    NodeSpecializationInterface,
    ProgressiveResultInterface,
    AuditInterface as RenderAuditInterface
)
from render_farm_manager.core.models import RenderJob, RenderNode, RenderClient, AuditLogEntry
from render_farm_manager.scheduling.deadline_scheduler import DeadlineScheduler
from render_farm_manager.resource_management.resource_partitioner import ResourcePartitioner
from render_farm_manager.energy_optimization.energy_optimizer import EnergyOptimizer
from render_farm_manager.node_specialization.specialization_manager import NodeSpecializationManager
from render_farm_manager.progressive_result.progressive_renderer import ProgressiveRenderer
from render_farm_manager.utils.logging import AuditLogger, PerformanceMonitor


class RenderFarmSchedulerAdapter(CommonSchedulerInterface):
    """
    Adapter that makes DeadlineScheduler compatible with common library interface.
    """
    
    def __init__(self, deadline_scheduler: DeadlineScheduler):
        """Initialize with existing deadline scheduler."""
        self.deadline_scheduler = deadline_scheduler
        self.logger = logging.getLogger("render_farm.scheduler_adapter")
    
    def schedule_tasks(self, tasks: List[BaseTask], nodes: List[BaseNode]) -> Dict[str, str]:
        """Schedule tasks using render farm deadline scheduler."""
        # Convert to render farm models
        render_jobs = [TaskAdapter.base_task_to_render_job(task) for task in tasks]
        render_nodes = [NodeAdapter.base_node_to_render_node(node) for node in nodes]
        
        # Use render farm scheduler
        result = self.deadline_scheduler.schedule_jobs(render_jobs, render_nodes)
        
        self.logger.info(f"Scheduled {len(result)} tasks via adapter")
        return result
    
    def update_priorities(self, tasks: List[BaseTask]) -> List[BaseTask]:
        """Update priorities using render farm logic."""
        # Convert to render farm models
        render_jobs = [TaskAdapter.base_task_to_render_job(task) for task in tasks]
        
        # Update priorities
        updated_jobs = self.deadline_scheduler.update_priorities(render_jobs)
        
        # Convert back to base tasks
        updated_tasks = []
        for i, task in enumerate(tasks):
            updated_job = updated_jobs[i]
            updated_task = task.model_copy()
            
            # Update priority and status
            updated_task.priority = PriorityAdapter.job_priority_to_common(updated_job.priority)
            updated_task.status = StatusAdapter.render_job_to_task_status(updated_job.status)
            
            # Store updated job data in metadata for future use
            updated_task.metadata = updated_task.metadata or {}
            updated_task.metadata['render_job_cache'] = updated_job
            
            updated_tasks.append(updated_task)
        
        return updated_tasks
    
    def can_meet_deadline(self, task: BaseTask, nodes: List[BaseNode]) -> bool:
        """Check deadline using render farm logic."""
        render_job = TaskAdapter.base_task_to_render_job(task)
        render_nodes = [NodeAdapter.base_node_to_render_node(node) for node in nodes]
        
        return self.deadline_scheduler.can_meet_deadline(render_job, render_nodes)


class RenderFarmResourceManagerAdapter(CommonResourceManagerInterface):
    """
    Adapter that makes render farm resource management compatible with common interface.
    """
    
    def __init__(self, resource_partitioner: ResourcePartitioner, audit_logger: Optional[AuditLogger] = None):
        """Initialize with resource partitioner."""
        self.resource_partitioner = resource_partitioner
        self.audit_logger = audit_logger
        self.logger = logging.getLogger("render_farm.resource_adapter")
    
    def allocate_resources(self, entities: List[Any], nodes: List[BaseNode]) -> Dict[str, Dict[str, float]]:
        """Allocate resources using render farm logic."""
        render_nodes = [NodeAdapter.base_node_to_render_node(node) for node in nodes]
        
        # Handle different entity types
        if not entities:
            return {}
        
        first_entity = entities[0]
        
        if isinstance(first_entity, BaseTask):
            return self._allocate_for_tasks(entities, render_nodes)
        else:
            return self._allocate_for_clients(entities, render_nodes)
    
    def calculate_resource_usage(self, entity_id: str, tasks: List[BaseTask]) -> Dict[str, float]:
        """Calculate resource usage."""
        render_jobs = [TaskAdapter.base_task_to_render_job(task) for task in tasks]
        
        # Filter jobs for this entity
        entity_jobs = [job for job in render_jobs if job.client_id == entity_id or job.id == entity_id]
        
        return {
            'cpu_cores': sum(job.cpu_requirements for job in entity_jobs),
            'memory_gb': sum(job.memory_requirements_gb for job in entity_jobs),
            'gpu_devices': sum(1 for job in entity_jobs if job.requires_gpu),
            'job_count': len(entity_jobs)
        }
    
    def _allocate_for_tasks(self, tasks: List[BaseTask], nodes: List[RenderNode]) -> Dict[str, Dict[str, float]]:
        """Allocate resources for tasks."""
        allocations = {}
        
        for task in tasks:
            render_job = TaskAdapter.base_task_to_render_job(task)
            
            # Find suitable nodes
            suitable_nodes = [
                node for node in nodes
                if (render_job.cpu_requirements <= node.capabilities.cpu_cores and
                    render_job.memory_requirements_gb <= node.capabilities.memory_gb and
                    (not render_job.requires_gpu or node.capabilities.gpu_count > 0))
            ]
            
            if suitable_nodes:
                best_node = max(suitable_nodes, key=lambda n: n.power_efficiency_rating)
                allocations[task.id] = {
                    'cpu_percentage': (render_job.cpu_requirements / best_node.capabilities.cpu_cores) * 100,
                    'memory_percentage': (render_job.memory_requirements_gb / best_node.capabilities.memory_gb) * 100,
                    'node_id': best_node.id
                }
            else:
                allocations[task.id] = {'cpu_percentage': 0.0, 'memory_percentage': 0.0, 'error': 'No suitable node'}
        
        return allocations
    
    def _allocate_for_clients(self, clients: List[Any], nodes: List[RenderNode]) -> Dict[str, Dict[str, float]]:
        """Allocate resources for clients."""
        # Convert to render clients
        render_clients = []
        for client in clients:
            if hasattr(client, 'client_id'):
                render_clients.append(client)
            else:
                from render_farm_manager.core.models import RenderClient, ServiceTier
                render_client = RenderClient(
                    client_id=getattr(client, 'id', str(client)),
                    name=getattr(client, 'name', f"Client {client}"),
                    service_tier=ServiceTier.STANDARD
                )
                render_clients.append(render_client)
        
        # Use resource partitioner if available
        if hasattr(self.resource_partitioner, 'allocate_resources'):
            return self.resource_partitioner.allocate_resources(render_clients, nodes)
        else:
            # Simple equal allocation
            equal_share = 100.0 / len(render_clients) if render_clients else 0.0
            return {
                client.client_id if hasattr(client, 'client_id') else client.id: 
                {'allocated_percentage': equal_share}
                for client in render_clients
            }


class RenderFarmAuditAdapter(AuditLogInterface):
    """Adapter for render farm audit logging to common interface."""
    
    def __init__(self, audit_logger: AuditLogger):
        """Initialize with render farm audit logger."""
        self.audit_logger = audit_logger
        self.logger = logging.getLogger("render_farm.audit_adapter")
    
    def log_event(self, event_type: str, description: str, **details) -> None:
        """Log an audit event."""
        self.audit_logger.log_event(event_type, description, **details)


class RenderFarmFailureDetector(FailureDetectorInterface):
    """Failure detector for render farm jobs and nodes."""
    
    def __init__(self, audit_logger: Optional[AuditLogger] = None):
        """Initialize failure detector."""
        self.audit_logger = audit_logger
        self.logger = logging.getLogger("render_farm.failure_detector")
    
    def detect_failures(self, tasks: List[BaseTask], nodes: List[BaseNode]) -> List[str]:
        """Detect failed tasks or nodes."""
        failed_entities = []
        
        # Check for failed tasks
        for task in tasks:
            render_job = TaskAdapter.base_task_to_render_job(task)
            if render_job.status == render_job.status.FAILED:
                failed_entities.append(task.id)
        
        # Check for failed nodes
        for node in nodes:
            render_node = NodeAdapter.base_node_to_render_node(node)
            if render_node.status == "error" or render_node.status == "offline":
                failed_entities.append(node.id)
        
        if failed_entities and self.audit_logger:
            self.audit_logger.log_event(
                "failures_detected",
                f"Detected {len(failed_entities)} failed entities",
                failed_entities=failed_entities
            )
        
        return failed_entities
    
    def should_retry(self, task: BaseTask) -> bool:
        """Determine if a failed task should be retried."""
        render_job = TaskAdapter.base_task_to_render_job(task)
        
        # Retry if error count is low and job supports retries
        max_retries = 3
        return render_job.error_count < max_retries and render_job.supports_checkpoint


class RenderFarmMetricsCollector(MetricsCollectorInterface):
    """Metrics collector for render farm performance monitoring."""
    
    def __init__(self, performance_monitor: Optional[PerformanceMonitor] = None):
        """Initialize metrics collector."""
        self.performance_monitor = performance_monitor
        self.logger = logging.getLogger("render_farm.metrics")
    
    def collect_metrics(self, entities: List[Any]) -> Dict[str, Any]:
        """Collect performance metrics from entities."""
        metrics = {
            'total_entities': len(entities),
            'timestamp': datetime.now().isoformat(),
            'entity_breakdown': {}
        }
        
        # Analyze entity types
        task_count = 0
        node_count = 0
        
        for entity in entities:
            if isinstance(entity, BaseTask):
                task_count += 1
            elif isinstance(entity, BaseNode):
                node_count += 1
        
        metrics['entity_breakdown'] = {
            'tasks': task_count,
            'nodes': node_count,
            'other': len(entities) - task_count - node_count
        }
        
        # Collect task-specific metrics
        if task_count > 0:
            tasks = [e for e in entities if isinstance(e, BaseTask)]
            render_jobs = [TaskAdapter.base_task_to_render_job(task) for task in tasks]
            
            metrics['task_metrics'] = {
                'total_jobs': len(render_jobs),
                'running_jobs': len([j for j in render_jobs if j.status.value == 'running']),
                'completed_jobs': len([j for j in render_jobs if j.status.value == 'completed']),
                'failed_jobs': len([j for j in render_jobs if j.status.value == 'failed']),
                'average_progress': sum(job.progress for job in render_jobs) / len(render_jobs),
                'gpu_jobs': len([j for j in render_jobs if j.requires_gpu]),
            }
        
        # Collect node-specific metrics
        if node_count > 0:
            nodes = [e for e in entities if isinstance(e, BaseNode)]
            render_nodes = [NodeAdapter.base_node_to_render_node(node) for node in nodes]
            
            total_cpu = sum(node.capabilities.cpu_cores for node in render_nodes)
            total_memory = sum(node.capabilities.memory_gb for node in render_nodes)
            total_gpu = sum(node.capabilities.gpu_count for node in render_nodes)
            online_nodes = len([n for n in render_nodes if n.status == "online"])
            
            metrics['node_metrics'] = {
                'total_nodes': len(render_nodes),
                'online_nodes': online_nodes,
                'offline_nodes': len(render_nodes) - online_nodes,
                'total_cpu_cores': total_cpu,
                'total_memory_gb': total_memory,
                'total_gpu_devices': total_gpu,
                'average_efficiency': sum(node.power_efficiency_rating for node in render_nodes) / len(render_nodes),
            }
        
        return metrics
    
    def record_metric(self, name: str, value: float, tags: Dict[str, str] = None) -> None:
        """Record a single metric."""
        if self.performance_monitor:
            # Use performance monitor if available
            self.performance_monitor.record_metric(name, value)
        
        self.logger.info(f"Metric recorded: {name}={value}, tags={tags}")


class UnifiedRenderFarmManager:
    """
    Unified manager that provides both render farm specific and common library interfaces.
    This allows gradual migration and interoperability.
    """
    
    def __init__(
        self,
        audit_logger: AuditLogger,
        performance_monitor: PerformanceMonitor,
        deadline_safety_margin_hours: float = 2.0,
        enable_preemption: bool = True,
    ):
        """Initialize unified manager with render farm components."""
        # Core render farm components
        self.deadline_scheduler = DeadlineScheduler(
            audit_logger=audit_logger,
            performance_monitor=performance_monitor,
            deadline_safety_margin_hours=deadline_safety_margin_hours,
            enable_preemption=enable_preemption
        )
        
        self.resource_partitioner = ResourcePartitioner(audit_logger=audit_logger)
        self.energy_optimizer = EnergyOptimizer(audit_logger=audit_logger, performance_monitor=performance_monitor)
        self.node_specialization = NodeSpecializationManager(audit_logger=audit_logger, performance_monitor=performance_monitor)
        self.progressive_renderer = ProgressiveRenderer(audit_logger=audit_logger)
        
        # Common library adapters
        self.common_scheduler = RenderFarmSchedulerAdapter(self.deadline_scheduler)
        self.common_resource_manager = RenderFarmResourceManagerAdapter(self.resource_partitioner, audit_logger)
        self.common_audit = RenderFarmAuditAdapter(audit_logger)
        self.common_failure_detector = RenderFarmFailureDetector(audit_logger)
        self.common_metrics = RenderFarmMetricsCollector(performance_monitor)
        
        self.logger = logging.getLogger("render_farm.unified_manager")
    
    # Render farm specific interface methods
    def schedule_render_jobs(self, jobs: List[RenderJob], nodes: List[RenderNode]) -> Dict[str, str]:
        """Schedule render jobs using domain-specific logic."""
        return self.deadline_scheduler.schedule_jobs(jobs, nodes)
    
    def optimize_energy_usage(self, jobs: List[RenderJob], nodes: List[RenderNode]) -> Dict[str, str]:
        """Optimize energy usage for render jobs."""
        return self.energy_optimizer.optimize_energy_usage(jobs, nodes)
    
    def match_job_to_specialized_node(self, job: RenderJob, nodes: List[RenderNode]) -> Optional[str]:
        """Match job to specialized node."""
        return self.node_specialization.match_job_to_node(job, nodes)
    
    # Common library interface methods
    def schedule_tasks(self, tasks: List[BaseTask], nodes: List[BaseNode]) -> Dict[str, str]:
        """Schedule tasks using common library interface."""
        return self.common_scheduler.schedule_tasks(tasks, nodes)
    
    def allocate_resources(self, entities: List[Any], nodes: List[BaseNode]) -> Dict[str, Dict[str, float]]:
        """Allocate resources using common library interface."""
        return self.common_resource_manager.allocate_resources(entities, nodes)
    
    def detect_failures(self, tasks: List[BaseTask], nodes: List[BaseNode]) -> List[str]:
        """Detect failures using common library interface."""
        return self.common_failure_detector.detect_failures(tasks, nodes)
    
    def collect_metrics(self, entities: List[Any]) -> Dict[str, Any]:
        """Collect metrics using common library interface."""
        return self.common_metrics.collect_metrics(entities)