"""Compatibility adapters for common library integration."""

from typing import Dict, Any, List
from datetime import datetime, timedelta


def _import_common_models():
    """Lazy import of common library models to avoid circular imports."""
    from common.core.models import TaskStatus, Priority, BaseTask, BaseNode, ResourceType as CommonResourceType
    return TaskStatus, Priority, BaseTask, BaseNode, CommonResourceType


def _import_simulation_models():
    """Lazy import of simulation models."""
    from .models.simulation import SimulationStatus, SimulationPriority, SimulationStageStatus, ResourceType
    return SimulationStatus, SimulationPriority, SimulationStageStatus, ResourceType


class StatusAdapter:
    """Adapter for status enum conversions."""
    
    @staticmethod
    def simulation_to_task_status(sim_status):
        """Convert SimulationStatus to TaskStatus."""
        TaskStatus, _, _, _, _ = _import_common_models()
        SimulationStatus, _, _, _ = _import_simulation_models()
        
        mapping = {
            SimulationStatus.DEFINED: TaskStatus.PENDING,
            SimulationStatus.SCHEDULED: TaskStatus.QUEUED,
            SimulationStatus.RUNNING: TaskStatus.RUNNING,
            SimulationStatus.PAUSED: TaskStatus.PAUSED,
            SimulationStatus.COMPLETED: TaskStatus.COMPLETED,
            SimulationStatus.FAILED: TaskStatus.FAILED,
        }
        return mapping.get(sim_status, TaskStatus.PENDING)
    
    @staticmethod
    def stage_to_task_status(stage_status):
        """Convert SimulationStageStatus to TaskStatus."""
        TaskStatus, _, _, _, _ = _import_common_models()
        _, _, SimulationStageStatus, _ = _import_simulation_models()
        
        mapping = {
            SimulationStageStatus.PENDING: TaskStatus.PENDING,
            SimulationStageStatus.QUEUED: TaskStatus.QUEUED,
            SimulationStageStatus.RUNNING: TaskStatus.RUNNING,
            SimulationStageStatus.PAUSED: TaskStatus.PAUSED,
            SimulationStageStatus.COMPLETED: TaskStatus.COMPLETED,
            SimulationStageStatus.FAILED: TaskStatus.FAILED,
        }
        return mapping.get(stage_status, TaskStatus.PENDING)
    
    @staticmethod
    def task_to_simulation_status(task_status):
        """Convert TaskStatus back to SimulationStatus."""
        TaskStatus, _, _, _, _ = _import_common_models()
        SimulationStatus, _, _, _ = _import_simulation_models()
        
        mapping = {
            TaskStatus.PENDING: SimulationStatus.DEFINED,
            TaskStatus.QUEUED: SimulationStatus.SCHEDULED,
            TaskStatus.RUNNING: SimulationStatus.RUNNING,
            TaskStatus.PAUSED: SimulationStatus.PAUSED,
            TaskStatus.COMPLETED: SimulationStatus.COMPLETED,
            TaskStatus.FAILED: SimulationStatus.FAILED,
            TaskStatus.CANCELLED: SimulationStatus.FAILED,
        }
        return mapping.get(task_status, SimulationStatus.DEFINED)
    
    @staticmethod
    def task_to_stage_status(task_status):
        """Convert TaskStatus back to SimulationStageStatus."""
        TaskStatus, _, _, _, _ = _import_common_models()
        _, _, SimulationStageStatus, _ = _import_simulation_models()
        
        mapping = {
            TaskStatus.PENDING: SimulationStageStatus.PENDING,
            TaskStatus.QUEUED: SimulationStageStatus.QUEUED,
            TaskStatus.RUNNING: SimulationStageStatus.RUNNING,
            TaskStatus.PAUSED: SimulationStageStatus.PAUSED,
            TaskStatus.COMPLETED: SimulationStageStatus.COMPLETED,
            TaskStatus.FAILED: SimulationStageStatus.FAILED,
            TaskStatus.CANCELLED: SimulationStageStatus.FAILED,
        }
        return mapping.get(task_status, SimulationStageStatus.PENDING)
    
    @staticmethod
    def priority_to_common(sim_priority):
        """Convert SimulationPriority to common Priority."""
        _, Priority, _, _, _ = _import_common_models()
        _, SimulationPriority, _, _ = _import_simulation_models()
        
        mapping = {
            SimulationPriority.BACKGROUND: Priority.LOW,
            SimulationPriority.LOW: Priority.LOW,
            SimulationPriority.MEDIUM: Priority.MEDIUM,
            SimulationPriority.HIGH: Priority.HIGH,
            SimulationPriority.CRITICAL: Priority.CRITICAL,
        }
        return mapping.get(sim_priority, Priority.MEDIUM)
    
    @staticmethod
    def priority_from_common(priority):
        """Convert common Priority back to SimulationPriority."""
        _, Priority, _, _, _ = _import_common_models()
        _, SimulationPriority, _, _ = _import_simulation_models()
        
        mapping = {
            Priority.LOW: SimulationPriority.LOW,
            Priority.MEDIUM: SimulationPriority.MEDIUM,
            Priority.HIGH: SimulationPriority.HIGH,
            Priority.CRITICAL: SimulationPriority.CRITICAL,
        }
        return mapping.get(priority, SimulationPriority.MEDIUM)


class ResourceAdapter:
    """Adapter for resource type conversions."""
    
    @staticmethod
    def resource_to_common(resource_type):
        """Convert scientific computing ResourceType to common ResourceType."""
        _, _, _, _, CommonResourceType = _import_common_models()
        _, _, _, ResourceType = _import_simulation_models()
        
        mapping = {
            ResourceType.CPU: CommonResourceType.CPU,
            ResourceType.MEMORY: CommonResourceType.MEMORY,
            ResourceType.GPU: CommonResourceType.GPU,
            ResourceType.STORAGE: CommonResourceType.STORAGE,
            # NETWORK doesn't exist in common, map to STORAGE as fallback
            ResourceType.NETWORK: CommonResourceType.STORAGE,
        }
        return mapping.get(resource_type, CommonResourceType.CPU)
    
    @staticmethod
    def resource_from_common(resource_type):
        """Convert common ResourceType to scientific computing ResourceType."""
        _, _, _, _, CommonResourceType = _import_common_models()
        _, _, _, ResourceType = _import_simulation_models()
        
        mapping = {
            CommonResourceType.CPU: ResourceType.CPU,
            CommonResourceType.MEMORY: ResourceType.MEMORY,
            CommonResourceType.GPU: ResourceType.GPU,
            CommonResourceType.STORAGE: ResourceType.STORAGE,
        }
        return mapping.get(resource_type, ResourceType.CPU)


class TaskAdapter:
    """Adapter for converting simulations to BaseTask format."""
    
    @staticmethod
    def simulation_to_base_task(simulation):
        """Convert Simulation to BaseTask instance."""
        _, Priority, BaseTask, _, _ = _import_common_models()
        
        return BaseTask(
            id=simulation.id,
            name=simulation.name,
            status=StatusAdapter.simulation_to_task_status(simulation.status),
            priority=StatusAdapter.priority_to_common(simulation.priority),
            submission_time=simulation.creation_time,
            estimated_duration=simulation.estimated_total_duration,
            progress=simulation.total_progress(),
            dependencies=[],  # Dependencies are handled at stage level
            metadata={
                'owner': simulation.owner,
                'project': simulation.project,
                'tags': simulation.tags,
                'scientific_promise': simulation.scientific_promise,
                'description': simulation.description,
                'result_path': simulation.result_path,
                'original_status': simulation.status.value,
                'original_priority': simulation.priority.value,
                **simulation.metadata
            }
        )
    
    @staticmethod
    def stage_to_base_task(stage):
        """Convert SimulationStage to BaseTask instance."""
        _, Priority, BaseTask, _, _ = _import_common_models()
        
        return BaseTask(
            id=stage.id,
            name=stage.name,
            status=StatusAdapter.stage_to_task_status(stage.status),
            priority=Priority.MEDIUM,  # Stages inherit priority from parent simulation
            submission_time=stage.start_time or datetime.now(),
            estimated_duration=stage.estimated_duration,
            progress=stage.progress,
            dependencies=list(stage.dependencies),
            metadata={
                'description': stage.description,
                'checkpoint_frequency': stage.checkpoint_frequency.total_seconds(),
                'last_checkpoint_time': stage.last_checkpoint_time.isoformat() if stage.last_checkpoint_time else None,
                'checkpoint_path': stage.checkpoint_path,
                'error_message': stage.error_message,
                'resource_requirements': [
                    {
                        'resource_type': req.resource_type.value,
                        'amount': req.amount,
                        'unit': req.unit
                    }
                    for req in stage.resource_requirements
                ],
                'original_status': stage.status.value,
                'start_time': stage.start_time.isoformat() if stage.start_time else None,
                'end_time': stage.end_time.isoformat() if stage.end_time else None,
            }
        )
    
    @staticmethod
    def update_simulation_from_task(simulation, task):
        """Update Simulation object from BaseTask."""
        simulation.status = StatusAdapter.task_to_simulation_status(task.status)
        simulation.priority = StatusAdapter.priority_from_common(task.priority)
        
        # Store progress in metadata to maintain compatibility
        if 'progress' not in simulation.metadata:
            simulation.metadata['progress'] = task.progress
        
        # Update other fields from metadata
        if task.metadata:
            if 'result_path' in task.metadata:
                simulation.result_path = task.metadata['result_path']
    
    @staticmethod
    def update_stage_from_task(stage, task):
        """Update SimulationStage object from BaseTask.""" 
        stage.status = StatusAdapter.task_to_stage_status(task.status)
        stage.progress = task.progress
        
        if task.metadata:
            if 'error_message' in task.metadata:
                stage.error_message = task.metadata['error_message']
            if 'checkpoint_path' in task.metadata:
                stage.checkpoint_path = task.metadata['checkpoint_path']
            if 'last_checkpoint_time' in task.metadata and task.metadata['last_checkpoint_time']:
                stage.last_checkpoint_time = datetime.fromisoformat(task.metadata['last_checkpoint_time'])


class NodeAdapter:
    """Adapter for converting ComputeNode to BaseNode format."""
    
    @staticmethod
    def compute_node_to_base_node(compute_node):
        """Convert ComputeNode to BaseNode instance."""
        from .models.simulation import NodeStatus as ScientificNodeStatus
        _, _, _, BaseNode, CommonResourceType = _import_common_models()
        from common.core.models import NodeStatus as CommonNodeStatus
        
        # Map scientific computing node statuses to common node statuses
        status_mapping = {
            ScientificNodeStatus.ONLINE: CommonNodeStatus.ONLINE,
            ScientificNodeStatus.OFFLINE: CommonNodeStatus.OFFLINE,
            ScientificNodeStatus.MAINTENANCE: CommonNodeStatus.MAINTENANCE,
            ScientificNodeStatus.RESERVED: CommonNodeStatus.ONLINE,  # Map reserved to online
        }
        
        # Convert current_load to use common ResourceType
        current_load = {}
        for resource_type, load in compute_node.current_load.items():
            common_resource_type = ResourceAdapter.resource_to_common(resource_type)
            current_load[common_resource_type] = load
        
        return BaseNode(
            id=compute_node.id,
            name=compute_node.name,
            status=status_mapping.get(compute_node.status, CommonNodeStatus.OFFLINE),
            cpu_cores=compute_node.cpu_cores,
            memory_gb=compute_node.memory_gb,
            gpu_count=compute_node.gpu_count,
            current_load=current_load
        )
    
    @staticmethod
    def update_compute_node_from_base_node(compute_node, base_node):
        """Update ComputeNode object from BaseNode."""
        from .models.simulation import NodeStatus as ScientificNodeStatus
        from common.core.models import NodeStatus as CommonNodeStatus
        
        # Map common node status back to scientific computing status
        status_mapping = {
            CommonNodeStatus.ONLINE: ScientificNodeStatus.ONLINE,
            CommonNodeStatus.OFFLINE: ScientificNodeStatus.OFFLINE,
            CommonNodeStatus.MAINTENANCE: ScientificNodeStatus.MAINTENANCE,
            CommonNodeStatus.ERROR: ScientificNodeStatus.OFFLINE,
        }
        compute_node.status = status_mapping.get(base_node.status, ScientificNodeStatus.OFFLINE)
        
        # Convert current_load back to scientific computing ResourceType
        current_load = {}
        for resource_type, load in base_node.current_load.items():
            scientific_resource_type = ResourceAdapter.resource_from_common(resource_type)
            current_load[scientific_resource_type] = load
        compute_node.current_load = current_load