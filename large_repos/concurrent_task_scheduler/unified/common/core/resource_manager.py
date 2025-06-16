from typing import Dict, List, Any
from .models import BaseNode, BaseTask, ResourceType, TaskStatus
from .interfaces import ResourceManagerInterface


class BaseResourceManager(ResourceManagerInterface):
    """Base resource manager with common allocation logic"""
    
    def allocate_resources(self, entities: List[Any], nodes: List[BaseNode]) -> Dict[str, Dict[str, float]]:
        """Fair resource allocation across entities"""
        total_resources = self._calculate_total_resources(nodes)
        allocations = {}
        
        # Simple equal allocation
        if entities:
            per_entity_allocation = {
                resource_type: total / len(entities) 
                for resource_type, total in total_resources.items()
            }
            
            for entity in entities:
                entity_id = getattr(entity, 'id', str(entity))
                allocations[entity_id] = per_entity_allocation
        
        return allocations
    
    def calculate_resource_usage(self, entity_id: str, tasks: List[BaseTask]) -> Dict[str, float]:
        """Calculate current resource usage for an entity"""
        usage = {resource_type.value: 0.0 for resource_type in ResourceType}
        
        for task in tasks:
            if task.status == TaskStatus.RUNNING:
                # Extract resource requirements from metadata
                requirements = task.metadata.get('resource_requirements', {})
                for resource_type, amount in requirements.items():
                    if resource_type in usage:
                        usage[resource_type] += amount
        
        return usage
    
    def can_allocate_resources(self, task: BaseTask, node: BaseNode) -> bool:
        """Check if a node can accommodate a task's resource requirements"""
        requirements = task.metadata.get('resource_requirements', {})
        
        # Check CPU
        if 'cpu' in requirements:
            available_cpu = node.cpu_cores - node.current_load.get(ResourceType.CPU, 0)
            if requirements['cpu'] > available_cpu:
                return False
        
        # Check Memory
        if 'memory' in requirements:
            available_memory = node.memory_gb - node.current_load.get(ResourceType.MEMORY, 0)
            if requirements['memory'] > available_memory:
                return False
        
        # Check GPU
        if 'gpu' in requirements:
            available_gpu = node.gpu_count - node.current_load.get(ResourceType.GPU, 0)
            if requirements['gpu'] > available_gpu:
                return False
        
        return True
    
    def update_node_load(self, node: BaseNode, task: BaseTask, operation: str) -> None:
        """Update node load when adding or removing a task"""
        requirements = task.metadata.get('resource_requirements', {})
        multiplier = 1 if operation == 'add' else -1
        
        for resource_type_str, amount in requirements.items():
            try:
                resource_type = ResourceType(resource_type_str)
                current_load = node.current_load.get(resource_type, 0.0)
                node.current_load[resource_type] = max(0.0, current_load + (amount * multiplier))
            except ValueError:
                # Skip unknown resource types
                continue
    
    def get_node_utilization(self, node: BaseNode) -> Dict[str, float]:
        """Calculate utilization percentage for each resource type on a node"""
        utilization = {}
        
        # CPU utilization
        cpu_load = node.current_load.get(ResourceType.CPU, 0.0)
        utilization['cpu'] = (cpu_load / node.cpu_cores) * 100 if node.cpu_cores > 0 else 0
        
        # Memory utilization
        memory_load = node.current_load.get(ResourceType.MEMORY, 0.0)
        utilization['memory'] = (memory_load / node.memory_gb) * 100 if node.memory_gb > 0 else 0
        
        # GPU utilization
        gpu_load = node.current_load.get(ResourceType.GPU, 0.0)
        utilization['gpu'] = (gpu_load / node.gpu_count) * 100 if node.gpu_count > 0 else 0
        
        return utilization
    
    def find_best_node(self, task: BaseTask, nodes: List[BaseNode]) -> BaseNode:
        """Find the best node for a task based on resource requirements and load"""
        suitable_nodes = [node for node in nodes 
                         if node.status.value == "online" and 
                         self.can_allocate_resources(task, node)]
        
        if not suitable_nodes:
            return None
        
        # Prefer nodes with lowest overall utilization
        best_node = min(suitable_nodes, 
                       key=lambda n: sum(self.get_node_utilization(n).values()))
        
        return best_node
    
    def _calculate_total_resources(self, nodes: List[BaseNode]) -> Dict[str, float]:
        """Calculate total available resources across all nodes"""
        totals = {
            ResourceType.CPU.value: 0.0,
            ResourceType.MEMORY.value: 0.0,
            ResourceType.GPU.value: 0.0
        }
        
        for node in nodes:
            if node.status.value == "online":
                totals[ResourceType.CPU.value] += node.cpu_cores
                totals[ResourceType.MEMORY.value] += node.memory_gb
                totals[ResourceType.GPU.value] += node.gpu_count
        
        return totals