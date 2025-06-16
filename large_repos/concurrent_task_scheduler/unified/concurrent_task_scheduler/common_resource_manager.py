"""Common library compatible resource manager for Scientific Computing implementation."""

import logging
from typing import Dict, List, Any, Optional

from common.core.interfaces import ResourceManagerInterface
from common.core.models import BaseTask, BaseNode, TaskStatus
from .adapters import TaskAdapter, NodeAdapter
from .models.simulation import ComputeNode, Simulation, SimulationStage


class ScientificComputingResourceManager(ResourceManagerInterface):
    """
    Resource manager that implements common library interface while preserving
    scientific computing specific resource allocation logic.
    """
    
    def __init__(self, forecast_enabled: bool = True):
        """
        Initialize the scientific computing resource manager.
        
        Args:
            forecast_enabled: Whether to enable resource forecasting
        """
        self.forecast_enabled = forecast_enabled
        self.logger = logging.getLogger("scientific_computing.common_resource_manager")
        
        # Track historical usage for forecasting
        self.usage_history = {}
    
    def allocate_resources(self, entities: List[Any], nodes: List[BaseNode]) -> Dict[str, Dict[str, float]]:
        """
        Allocate resources to entities using scientific computing logic.
        
        Args:
            entities: List of entities (BaseTask instances, simulations, or projects)
            nodes: List of BaseNode instances
            
        Returns:
            Dictionary mapping entity IDs to their resource allocations
        """
        # Convert nodes to scientific computing format
        compute_nodes = [NodeAdapter.base_node_to_compute_node(node) for node in nodes]
        
        # Calculate total available resources
        total_resources = self._calculate_total_resources(compute_nodes)
        
        if not entities:
            return {}
        
        # Determine entity type and allocate accordingly
        first_entity = entities[0]
        
        if isinstance(first_entity, BaseTask):
            return self._allocate_resources_for_tasks(entities, compute_nodes, total_resources)
        elif hasattr(first_entity, 'stages'):  # Simulation-like entity
            return self._allocate_resources_for_simulations(entities, compute_nodes, total_resources)
        else:
            # Generic allocation for unknown entity types (projects, users, etc.)
            return self._allocate_resources_generic(entities, compute_nodes, total_resources)
    
    def calculate_resource_usage(self, entity_id: str, tasks: List[BaseTask]) -> Dict[str, float]:
        """
        Calculate resource usage for an entity.
        
        Args:
            entity_id: ID of the entity (simulation, project, user, etc.)
            tasks: List of BaseTask instances to analyze
            
        Returns:
            Dictionary of resource usage by type
        """
        usage = {
            'cpu_hours': 0.0,
            'memory_gb_hours': 0.0,
            'gpu_hours': 0.0,
            'storage_gb': 0.0,
            'active_tasks': 0,
            'total_tasks': len(tasks)
        }
        
        for task in tasks:
            # Get resource requirements from metadata
            resource_requirements = task.metadata.get('resource_requirements', {})
            
            # Calculate usage based on task progress and estimated duration
            if task.status == TaskStatus.RUNNING:
                # For running tasks, calculate usage based on elapsed time
                elapsed_hours = (datetime.now() - task.submission_time).total_seconds() / 3600
                usage['cpu_hours'] += resource_requirements.get('cpu', 0) * elapsed_hours
                usage['memory_gb_hours'] += resource_requirements.get('memory', 0) * elapsed_hours
                usage['gpu_hours'] += resource_requirements.get('gpu', 0) * elapsed_hours
                usage['active_tasks'] += 1
            
            elif task.status == TaskStatus.COMPLETED:
                # For completed tasks, use full estimated duration
                duration_hours = task.estimated_duration.total_seconds() / 3600
                usage['cpu_hours'] += resource_requirements.get('cpu', 0) * duration_hours
                usage['memory_gb_hours'] += resource_requirements.get('memory', 0) * duration_hours
                usage['gpu_hours'] += resource_requirements.get('gpu', 0) * duration_hours
            
            # Add storage requirements
            usage['storage_gb'] += resource_requirements.get('storage', 0)
        
        # Store usage in history for forecasting
        if entity_id not in self.usage_history:
            self.usage_history[entity_id] = []
        
        from datetime import datetime
        self.usage_history[entity_id].append({
            'timestamp': datetime.now().isoformat(),
            'usage': usage.copy()
        })
        
        # Keep only recent history (last 100 records)
        if len(self.usage_history[entity_id]) > 100:
            self.usage_history[entity_id] = self.usage_history[entity_id][-100:]
        
        return usage
    
    def _allocate_resources_for_tasks(self, tasks: List[BaseTask], nodes: List[ComputeNode], 
                                    total_resources: Dict[str, float]) -> Dict[str, Dict[str, float]]:
        """Allocate resources for task entities."""
        allocations = {}
        
        # Group tasks by project/owner for fair allocation
        task_groups = {}
        for task in tasks:
            group_key = task.metadata.get('project', task.metadata.get('owner', 'default'))
            if group_key not in task_groups:
                task_groups[group_key] = []
            task_groups[group_key].append(task)
        
        # Calculate fair share per group
        fair_share_percentage = 100.0 / len(task_groups) if task_groups else 0
        
        for group_key, group_tasks in task_groups.items():
            # Calculate group's resource allocation
            group_allocation = {
                resource_type: (fair_share_percentage / 100.0) * total_amount
                for resource_type, total_amount in total_resources.items()
            }
            
            # Distribute group allocation among tasks
            for task in group_tasks:
                resource_requirements = task.metadata.get('resource_requirements', {})
                
                # Find suitable nodes for this task
                suitable_nodes = []
                for node in nodes:
                    if self._node_can_accommodate_task(node, resource_requirements):
                        suitable_nodes.append(node)
                
                if suitable_nodes:
                    # Choose best node based on scientific computing criteria
                    best_node = max(suitable_nodes, key=lambda n: n.reliability_score)
                    
                    # Calculate allocation as percentage of node resources
                    allocations[task.id] = {
                        'cpu_percentage': (resource_requirements.get('cpu', 0) / best_node.cpu_cores) * 100,
                        'memory_percentage': (resource_requirements.get('memory', 0) / best_node.memory_gb) * 100,
                        'gpu_percentage': (resource_requirements.get('gpu', 0) / max(best_node.gpu_count, 1)) * 100,
                        'estimated_node_id': best_node.id,
                        'estimated_duration_hours': task.estimated_duration.total_seconds() / 3600,
                        'scientific_promise': task.metadata.get('scientific_promise', 0.5),
                        'project': task.metadata.get('project', 'unknown'),
                        'fair_share_group': group_key
                    }
                else:
                    # No suitable node found
                    allocations[task.id] = {
                        'cpu_percentage': 0.0,
                        'memory_percentage': 0.0,
                        'gpu_percentage': 0.0,
                        'estimated_node_id': None,
                        'error': 'No suitable node found',
                        'required_resources': resource_requirements
                    }
        
        return allocations
    
    def _allocate_resources_for_simulations(self, simulations: List[Any], nodes: List[ComputeNode],
                                          total_resources: Dict[str, float]) -> Dict[str, Dict[str, float]]:
        """Allocate resources for simulation entities."""
        allocations = {}
        
        for simulation in simulations:
            simulation_id = getattr(simulation, 'id', str(simulation))
            
            # Calculate total resource needs for all stages
            total_cpu_needed = 0
            total_memory_needed = 0
            total_gpu_needed = 0
            stage_count = 0
            
            if hasattr(simulation, 'stages'):
                for stage in simulation.stages.values():
                    stage_count += 1
                    for req in stage.resource_requirements:
                        if req.resource_type.value == 'cpu':
                            total_cpu_needed += req.amount
                        elif req.resource_type.value == 'memory':
                            total_memory_needed += req.amount
                        elif req.resource_type.value == 'gpu':
                            total_gpu_needed += req.amount
            
            # Calculate allocation as percentage of total cluster resources
            allocations[simulation_id] = {
                'cpu_percentage': (total_cpu_needed / total_resources.get('cpu', 1)) * 100,
                'memory_percentage': (total_memory_needed / total_resources.get('memory', 1)) * 100,
                'gpu_percentage': (total_gpu_needed / total_resources.get('gpu', 1)) * 100,
                'stage_count': stage_count,
                'estimated_total_duration_hours': getattr(simulation, 'estimated_total_duration', timedelta(days=1)).total_seconds() / 3600,
                'scientific_promise': getattr(simulation, 'scientific_promise', 0.5),
                'project': getattr(simulation, 'project', 'unknown'),
                'owner': getattr(simulation, 'owner', 'unknown')
            }
        
        return allocations
    
    def _allocate_resources_generic(self, entities: List[Any], nodes: List[ComputeNode],
                                  total_resources: Dict[str, float]) -> Dict[str, Dict[str, float]]:
        """Generic resource allocation for unknown entity types."""
        allocations = {}
        
        # Simple equal allocation strategy for unknown entities
        equal_share_percentage = 100.0 / len(entities) if entities else 0
        
        for entity in entities:
            entity_id = getattr(entity, 'id', str(entity))
            allocations[entity_id] = {
                'cpu_percentage': equal_share_percentage,
                'memory_percentage': equal_share_percentage,
                'gpu_percentage': equal_share_percentage,
                'allocation_strategy': 'equal_share',
                'estimated_cpu_cores': (equal_share_percentage / 100.0) * total_resources.get('cpu', 0),
                'estimated_memory_gb': (equal_share_percentage / 100.0) * total_resources.get('memory', 0),
                'estimated_gpu_count': (equal_share_percentage / 100.0) * total_resources.get('gpu', 0)
            }
        
        return allocations
    
    def _calculate_total_resources(self, nodes: List[ComputeNode]) -> Dict[str, float]:
        """Calculate total available resources across all nodes."""
        totals = {
            'cpu': 0.0,
            'memory': 0.0,
            'gpu': 0.0,
            'storage': 0.0,
            'network': 0.0
        }
        
        for node in nodes:
            if node.status.value == "online":
                totals['cpu'] += node.cpu_cores
                totals['memory'] += node.memory_gb
                totals['gpu'] += node.gpu_count
                totals['storage'] += node.storage_gb
                totals['network'] += node.network_bandwidth_gbps
        
        return totals
    
    def _node_can_accommodate_task(self, node: ComputeNode, resource_requirements: Dict[str, float]) -> bool:
        """Check if a node can accommodate a task's resource requirements."""
        available_resources = node.get_available_resources()
        
        for resource_type, required_amount in resource_requirements.items():
            # Map resource types to node attributes
            resource_map = {
                'cpu': 'cpu',
                'memory': 'memory',
                'gpu': 'gpu',
                'storage': 'storage'
            }
            
            if resource_type in resource_map:
                available_amount = available_resources.get(resource_map[resource_type], 0)
                if available_amount < required_amount:
                    return False
        
        return True
    
    def get_resource_forecast(self, entity_id: str, forecast_hours: int = 24) -> Dict[str, float]:
        """
        Generate resource usage forecast for an entity.
        
        Args:
            entity_id: ID of the entity to forecast
            forecast_hours: Number of hours to forecast ahead
            
        Returns:
            Dictionary with forecasted resource usage
        """
        if not self.forecast_enabled or entity_id not in self.usage_history:
            return {}
        
        history = self.usage_history[entity_id]
        if len(history) < 2:
            return {}
        
        # Simple linear trend forecasting
        recent_usage = history[-1]['usage']
        older_usage = history[-min(len(history), 10)]['usage']  # Look back up to 10 records
        
        forecast = {}
        for resource_type in recent_usage:
            if resource_type in older_usage:
                # Calculate trend
                trend = (recent_usage[resource_type] - older_usage[resource_type]) / min(len(history), 10)
                forecasted_value = recent_usage[resource_type] + (trend * forecast_hours)
                forecast[f"forecasted_{resource_type}"] = max(0, forecasted_value)
        
        return forecast