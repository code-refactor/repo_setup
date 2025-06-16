"""Common library compatible resource manager for Render Farm Manager."""

import logging
from typing import Dict, List, Any
from common.core.interfaces import ResourceManagerInterface
from common.core.models import BaseTask, BaseNode
from render_farm_manager.adapters import TaskAdapter, NodeAdapter, ResourceAdapter
from render_farm_manager.core.models import RenderJob, RenderNode, Client
from render_farm_manager.resource_management.resource_partitioner import ResourcePartitioner
from render_farm_manager.utils.logging import AuditLogger


class CommonResourceManager(ResourceManagerInterface):
    """
    Resource manager that implements common library interface while preserving
    render farm specific resource allocation logic.
    """
    
    def __init__(
        self,
        resource_partitioner: ResourcePartitioner,
        audit_logger: AuditLogger = None,
    ):
        """
        Initialize the common resource manager.
        
        Args:
            resource_partitioner: Render farm specific resource partitioner
            audit_logger: Optional audit logger for tracking resource events
        """
        self.resource_partitioner = resource_partitioner
        self.audit_logger = audit_logger
        self.logger = logging.getLogger("render_farm.common_resource_manager")
    
    def allocate_resources(self, entities: List[Any], nodes: List[BaseNode]) -> Dict[str, Dict[str, float]]:
        """
        Allocate resources to entities using render farm logic.
        
        Args:
            entities: List of entities (BaseTask instances or Client instances)
            nodes: List of BaseNode instances
            
        Returns:
            Dictionary mapping entity IDs to their resource allocations
        """
        # Convert nodes to render farm format
        render_nodes = [NodeAdapter.base_node_to_render_node(node) for node in nodes]
        
        # Handle different entity types
        if not entities:
            return {}
        
        # Check if entities are tasks or clients
        first_entity = entities[0]
        
        if isinstance(first_entity, BaseTask):
            return self._allocate_resources_for_tasks(entities, render_nodes)
        elif hasattr(first_entity, 'client_id') or hasattr(first_entity, 'id'):
            # Assume these are client-like entities
            return self._allocate_resources_for_clients(entities, render_nodes)
        else:
            # Generic allocation based on entity IDs
            return self._allocate_resources_generic(entities, render_nodes)
    
    def calculate_resource_usage(self, entity_id: str, tasks: List[BaseTask]) -> Dict[str, float]:
        """
        Calculate resource usage for an entity.
        
        Args:
            entity_id: ID of the entity (client, job, etc.)
            tasks: List of BaseTask instances to analyze
            
        Returns:
            Dictionary of resource usage by type
        """
        # Convert tasks to render jobs
        render_jobs = [TaskAdapter.base_task_to_render_job(task) for task in tasks]
        
        # Filter jobs for this entity (could be client_id or job grouping)
        entity_jobs = []
        for job in render_jobs:
            if (job.client_id == entity_id or 
                job.id == entity_id or
                job.id.startswith(entity_id)):
                entity_jobs.append(job)
        
        # Calculate usage
        total_cpu = sum(job.cpu_requirements for job in entity_jobs)
        total_memory = sum(job.memory_requirements_gb for job in entity_jobs)
        total_gpu = sum(1 for job in entity_jobs if job.requires_gpu)
        
        # Calculate percentages if we have node information
        usage = {
            'cpu_cores': float(total_cpu),
            'memory_gb': float(total_memory),
            'gpu_devices': float(total_gpu),
            'job_count': float(len(entity_jobs))
        }
        
        if self.audit_logger:
            self.audit_logger.log_event(
                "resource_usage_calculated",
                f"Resource usage calculated for entity {entity_id}",
                entity_id=entity_id,
                usage=usage,
                job_count=len(entity_jobs)
            )
        
        return usage
    
    def _allocate_resources_for_tasks(self, tasks: List[BaseTask], nodes: List[RenderNode]) -> Dict[str, Dict[str, float]]:
        """Allocate resources for task entities."""
        allocations = {}
        
        # Convert tasks to render jobs
        render_jobs = [TaskAdapter.base_task_to_render_job(task) for task in tasks]
        
        # Group jobs by client for render farm allocation logic
        jobs_by_client = {}
        for job in render_jobs:
            client_id = job.client_id
            if client_id not in jobs_by_client:
                jobs_by_client[client_id] = []
            jobs_by_client[client_id].append(job)
        
        # Calculate allocations for each task
        for task, job in zip(tasks, render_jobs):
            # Find best matching node for resource calculation
            suitable_nodes = []
            for node in nodes:
                if (job.cpu_requirements <= node.capabilities.cpu_cores and
                    job.memory_requirements_gb <= node.capabilities.memory_gb and
                    (not job.requires_gpu or node.capabilities.gpu_count > 0)):
                    suitable_nodes.append(node)
            
            if suitable_nodes:
                # Use the most efficient suitable node for allocation calculation
                best_node = max(suitable_nodes, key=lambda n: n.power_efficiency_rating)
                
                allocations[task.id] = {
                    'cpu_percentage': (job.cpu_requirements / best_node.capabilities.cpu_cores) * 100,
                    'memory_percentage': (job.memory_requirements_gb / best_node.capabilities.memory_gb) * 100,
                    'gpu_percentage': (100.0 if job.requires_gpu and best_node.capabilities.gpu_count > 0 else 0.0),
                    'node_id': best_node.id,
                    'estimated_duration_hours': job.estimated_duration_hours
                }
            else:
                # No suitable node found
                allocations[task.id] = {
                    'cpu_percentage': 0.0,
                    'memory_percentage': 0.0,
                    'gpu_percentage': 0.0,
                    'node_id': None,
                    'error': 'No suitable node found'
                }
        
        return allocations
    
    def _allocate_resources_for_clients(self, clients: List[Any], nodes: List[RenderNode]) -> Dict[str, Dict[str, float]]:
        """Allocate resources for client entities using render farm partitioner."""
        allocations = {}
        
        # Convert to Client objects if needed
        render_clients = []
        for client in clients:
            if hasattr(client, 'client_id'):
                # Already a render farm client
                render_clients.append(client)
            else:
                # Create minimal client from entity
                from render_farm_manager.core.models import RenderClient, ServiceTier
                render_client = RenderClient(
                    client_id=getattr(client, 'id', str(client)),
                    name=getattr(client, 'name', f"Client {client}"),
                    service_tier=ServiceTier.STANDARD,
                    guaranteed_resources=getattr(client, 'guaranteed_resources', 20),
                    max_resources=getattr(client, 'max_resources', 100)
                )
                render_clients.append(render_client)
        
        # Use resource partitioner to allocate
        if hasattr(self.resource_partitioner, 'allocate_resources'):
            partition_result = self.resource_partitioner.allocate_resources(render_clients, nodes)
            
            # Convert result to expected format
            for client in render_clients:
                client_id = client.client_id if hasattr(client, 'client_id') else client.id
                if client_id in partition_result:
                    allocation = partition_result[client_id]
                    allocations[client_id] = {
                        'allocated_percentage': allocation.allocated_percentage,
                        'allocated_nodes': len(allocation.allocated_nodes),
                        'borrowed_percentage': allocation.borrowed_percentage,
                        'lent_percentage': allocation.lent_percentage,
                        'guaranteed_resources': client.guaranteed_resources,
                        'max_resources': client.max_resources,
                    }
                else:
                    # Default allocation
                    allocations[client_id] = {
                        'allocated_percentage': client.guaranteed_resources,
                        'allocated_nodes': 0,
                        'borrowed_percentage': 0.0,
                        'lent_percentage': 0.0,
                        'guaranteed_resources': client.guaranteed_resources,
                        'max_resources': client.max_resources,
                    }
        else:
            # Fallback: simple equal allocation
            equal_share = 100.0 / len(render_clients) if render_clients else 0.0
            for client in render_clients:
                client_id = client.client_id if hasattr(client, 'client_id') else client.id
                allocations[client_id] = {
                    'allocated_percentage': min(equal_share, client.max_resources),
                    'allocated_nodes': len(nodes) // len(render_clients),
                    'borrowed_percentage': 0.0,
                    'lent_percentage': 0.0,
                    'guaranteed_resources': client.guaranteed_resources,
                    'max_resources': client.max_resources,
                }
        
        return allocations
    
    def _allocate_resources_generic(self, entities: List[Any], nodes: List[RenderNode]) -> Dict[str, Dict[str, float]]:
        """Generic resource allocation for unknown entity types."""
        allocations = {}
        
        # Simple equal allocation strategy
        equal_cpu_share = sum(node.capabilities.cpu_cores for node in nodes) / len(entities) if entities else 0
        equal_memory_share = sum(node.capabilities.memory_gb for node in nodes) / len(entities) if entities else 0
        equal_gpu_share = sum(node.capabilities.gpu_count for node in nodes) / len(entities) if entities else 0
        
        for entity in entities:
            entity_id = getattr(entity, 'id', str(entity))
            allocations[entity_id] = {
                'cpu_cores': equal_cpu_share,
                'memory_gb': equal_memory_share,
                'gpu_devices': equal_gpu_share,
                'allocation_strategy': 'equal_share'
            }
        
        return allocations