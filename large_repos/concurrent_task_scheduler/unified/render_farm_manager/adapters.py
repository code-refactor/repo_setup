"""Compatibility adapters for render farm manager integration with common library."""

from typing import Dict, Any, List
from datetime import datetime, timedelta


def _import_common_models():
    """Lazy import of common library models to avoid circular imports."""
    from common.core.models import TaskStatus, Priority, BaseTask, BaseNode, ResourceType as CommonResourceType
    return TaskStatus, Priority, BaseTask, BaseNode, CommonResourceType


def _import_render_models():
    """Lazy import of render farm models."""
    from .core.models import RenderJobStatus, JobPriority, NodeStatus
    return RenderJobStatus, JobPriority, NodeStatus


class StatusAdapter:
    """Adapter for status enum conversions."""
    
    @staticmethod
    def render_job_to_task_status(job_status):
        """Convert RenderJobStatus to TaskStatus."""
        TaskStatus, _, _, _, _ = _import_common_models()
        RenderJobStatus, _, _ = _import_render_models()
        
        mapping = {
            RenderJobStatus.PENDING: TaskStatus.PENDING,
            RenderJobStatus.QUEUED: TaskStatus.QUEUED,
            RenderJobStatus.RUNNING: TaskStatus.RUNNING,
            RenderJobStatus.PAUSED: TaskStatus.PAUSED,
            RenderJobStatus.COMPLETED: TaskStatus.COMPLETED,
            RenderJobStatus.FAILED: TaskStatus.FAILED,
            RenderJobStatus.CANCELLED: TaskStatus.CANCELLED,
        }
        return mapping.get(job_status, TaskStatus.PENDING)
    
    @staticmethod
    def task_to_render_job_status(task_status):
        """Convert TaskStatus back to RenderJobStatus."""
        TaskStatus, _, _, _, _ = _import_common_models()
        RenderJobStatus, _, _ = _import_render_models()
        
        mapping = {
            TaskStatus.PENDING: RenderJobStatus.PENDING,
            TaskStatus.QUEUED: RenderJobStatus.QUEUED,
            TaskStatus.RUNNING: RenderJobStatus.RUNNING,
            TaskStatus.PAUSED: RenderJobStatus.PAUSED,
            TaskStatus.COMPLETED: RenderJobStatus.COMPLETED,
            TaskStatus.FAILED: RenderJobStatus.FAILED,
            TaskStatus.CANCELLED: RenderJobStatus.CANCELLED,
        }
        return mapping.get(task_status, RenderJobStatus.PENDING)
    
    @staticmethod
    def render_node_to_node_status(node_status):
        """Convert render farm NodeStatus to common NodeStatus."""
        from common.core.models import NodeStatus as CommonNodeStatus
        _, _, NodeStatus = _import_render_models()
        
        mapping = {
            NodeStatus.ONLINE: CommonNodeStatus.ONLINE,
            NodeStatus.OFFLINE: CommonNodeStatus.OFFLINE,
            NodeStatus.MAINTENANCE: CommonNodeStatus.MAINTENANCE,
            NodeStatus.ERROR: CommonNodeStatus.ERROR,
            NodeStatus.STARTING: CommonNodeStatus.OFFLINE,  # Map to offline
            NodeStatus.STOPPING: CommonNodeStatus.OFFLINE,  # Map to offline
        }
        return mapping.get(node_status, CommonNodeStatus.OFFLINE)
    
    @staticmethod
    def node_to_render_node_status(node_status):
        """Convert common NodeStatus back to render farm NodeStatus."""
        from common.core.models import NodeStatus as CommonNodeStatus
        _, _, NodeStatus = _import_render_models()
        
        mapping = {
            CommonNodeStatus.ONLINE: NodeStatus.ONLINE,
            CommonNodeStatus.OFFLINE: NodeStatus.OFFLINE,
            CommonNodeStatus.MAINTENANCE: NodeStatus.MAINTENANCE,
            CommonNodeStatus.ERROR: NodeStatus.ERROR,
        }
        return mapping.get(node_status, NodeStatus.OFFLINE)


class PriorityAdapter:
    """Adapter for priority conversions."""
    
    @staticmethod
    def job_priority_to_common(job_priority):
        """Convert JobPriority to common Priority."""
        _, Priority, _, _, _ = _import_common_models()
        _, JobPriority, _ = _import_render_models()
        
        mapping = {
            JobPriority.LOW: Priority.LOW,
            JobPriority.MEDIUM: Priority.MEDIUM,
            JobPriority.HIGH: Priority.HIGH,
            JobPriority.CRITICAL: Priority.CRITICAL,
        }
        return mapping.get(job_priority, Priority.MEDIUM)
    
    @staticmethod
    def common_to_job_priority(priority):
        """Convert common Priority back to JobPriority."""
        _, Priority, _, _, _ = _import_common_models()
        _, JobPriority, _ = _import_render_models()
        
        mapping = {
            Priority.LOW: JobPriority.LOW,
            Priority.MEDIUM: JobPriority.MEDIUM,
            Priority.HIGH: JobPriority.HIGH,
            Priority.CRITICAL: JobPriority.CRITICAL,
        }
        return mapping.get(priority, JobPriority.MEDIUM)


class TaskAdapter:
    """Adapter for converting render jobs to BaseTask format."""
    
    @staticmethod
    def render_job_to_base_task(render_job):
        """Convert RenderJob to BaseTask instance."""
        _, Priority, BaseTask, _, _ = _import_common_models()
        
        return BaseTask(
            id=render_job.id,
            name=render_job.name,
            status=StatusAdapter.render_job_to_task_status(render_job.status),
            priority=PriorityAdapter.job_priority_to_common(render_job.priority),
            submission_time=render_job.submission_time,
            estimated_duration=timedelta(hours=render_job.estimated_duration_hours),
            progress=render_job.progress / 100.0,  # Convert from percentage to 0-1
            dependencies=render_job.dependencies,
            metadata={
                'client_id': render_job.client_id,
                'job_type': render_job.job_type,
                'deadline': render_job.deadline.isoformat(),
                'requires_gpu': render_job.requires_gpu,
                'memory_requirements_gb': render_job.memory_requirements_gb,
                'cpu_requirements': render_job.cpu_requirements,
                'scene_complexity': render_job.scene_complexity,
                'assigned_node_id': render_job.assigned_node_id,
                'output_path': render_job.output_path,
                'error_count': render_job.error_count,
                'can_be_preempted': render_job.can_be_preempted,
                'supports_progressive_output': render_job.supports_progressive_output,
                'supports_checkpoint': render_job.supports_checkpoint,
                'last_checkpoint_time': render_job.last_checkpoint_time.isoformat() if render_job.last_checkpoint_time else None,
                'last_progressive_output_time': render_job.last_progressive_output_time.isoformat() if render_job.last_progressive_output_time else None,
                'energy_intensive': render_job.energy_intensive,
                'original_status': render_job.status.value,
                'original_priority': render_job.priority.value,
                'resource_requirements': {
                    'cpu': render_job.cpu_requirements,
                    'memory': render_job.memory_requirements_gb,
                    'gpu': 1 if render_job.requires_gpu else 0
                }
            }
        )
    
    @staticmethod
    def base_task_to_render_job(base_task):
        """Convert BaseTask back to RenderJob instance."""
        from .core.models import RenderJob
        
        metadata = base_task.metadata
        
        return RenderJob(
            id=base_task.id,
            name=base_task.name,
            client_id=metadata.get('client_id', 'unknown'),
            status=StatusAdapter.task_to_render_job_status(base_task.status),
            job_type=metadata.get('job_type', 'render'),
            priority=PriorityAdapter.common_to_job_priority(base_task.priority),
            submission_time=base_task.submission_time,
            deadline=datetime.fromisoformat(metadata['deadline']) if 'deadline' in metadata else base_task.submission_time + base_task.estimated_duration,
            estimated_duration_hours=base_task.estimated_duration.total_seconds() / 3600,
            progress=base_task.progress * 100.0,  # Convert from 0-1 to percentage
            requires_gpu=metadata.get('requires_gpu', False),
            memory_requirements_gb=metadata.get('memory_requirements_gb', 8),
            cpu_requirements=metadata.get('cpu_requirements', 1),
            scene_complexity=metadata.get('scene_complexity', 5),
            dependencies=base_task.dependencies,
            assigned_node_id=metadata.get('assigned_node_id'),
            output_path=metadata.get('output_path', f'/tmp/{base_task.id}'),
            error_count=metadata.get('error_count', 0),
            can_be_preempted=metadata.get('can_be_preempted', True),
            supports_progressive_output=metadata.get('supports_progressive_output', False),
            supports_checkpoint=metadata.get('supports_checkpoint', False),
            last_checkpoint_time=datetime.fromisoformat(metadata['last_checkpoint_time']) if metadata.get('last_checkpoint_time') else None,
            last_progressive_output_time=datetime.fromisoformat(metadata['last_progressive_output_time']) if metadata.get('last_progressive_output_time') else None,
            energy_intensive=metadata.get('energy_intensive', False)
        )
    
    @staticmethod
    def update_render_job_from_task(render_job, base_task):
        """Update RenderJob object from BaseTask."""
        render_job.status = StatusAdapter.task_to_render_job_status(base_task.status)
        render_job.priority = PriorityAdapter.common_to_job_priority(base_task.priority)
        render_job.progress = base_task.progress * 100.0  # Convert from 0-1 to percentage
        
        if base_task.metadata:
            metadata = base_task.metadata
            if 'assigned_node_id' in metadata:
                render_job.assigned_node_id = metadata['assigned_node_id']
            if 'error_count' in metadata:
                render_job.error_count = metadata['error_count']
            if 'last_checkpoint_time' in metadata and metadata['last_checkpoint_time']:
                render_job.last_checkpoint_time = datetime.fromisoformat(metadata['last_checkpoint_time'])
            if 'last_progressive_output_time' in metadata and metadata['last_progressive_output_time']:
                render_job.last_progressive_output_time = datetime.fromisoformat(metadata['last_progressive_output_time'])


class NodeAdapter:
    """Adapter for converting render nodes to BaseNode format."""
    
    @staticmethod
    def render_node_to_base_node(render_node):
        """Convert RenderNode to BaseNode instance."""
        from common.core.models import ResourceType as CommonResourceType
        _, _, _, BaseNode, _ = _import_common_models()
        
        # Estimate current load based on whether node has a job assigned
        current_load = {}
        if render_node.current_job_id:
            # Estimate load - this is approximate since we don't have exact job resource usage
            current_load = {
                CommonResourceType.CPU: render_node.capabilities.cpu_cores * 0.8,  # Assume 80% utilization
                CommonResourceType.MEMORY: render_node.capabilities.memory_gb * 0.7,  # Assume 70% utilization
                CommonResourceType.GPU: render_node.capabilities.gpu_count * 0.9 if render_node.capabilities.gpu_count > 0 else 0,
            }
        else:
            current_load = {
                CommonResourceType.CPU: 0.0,
                CommonResourceType.MEMORY: 0.0,
                CommonResourceType.GPU: 0.0,
            }
        
        return BaseNode(
            id=render_node.id,
            name=render_node.name,
            status=StatusAdapter.render_node_to_node_status(render_node.status),
            cpu_cores=render_node.capabilities.cpu_cores,
            memory_gb=render_node.capabilities.memory_gb,
            gpu_count=render_node.capabilities.gpu_count,
            current_load=current_load
        )
    
    @staticmethod
    def update_render_node_from_base_node(render_node, base_node):
        """Update RenderNode object from BaseNode."""
        render_node.status = StatusAdapter.node_to_render_node_status(base_node.status)
        
        # Update capabilities if they've changed
        render_node.capabilities.cpu_cores = base_node.cpu_cores
        render_node.capabilities.memory_gb = base_node.memory_gb
        render_node.capabilities.gpu_count = base_node.gpu_count
        
        # Estimate if node is busy based on current load
        from common.core.models import ResourceType as CommonResourceType
        cpu_utilization = base_node.current_load.get(CommonResourceType.CPU, 0) / base_node.cpu_cores if base_node.cpu_cores > 0 else 0
        if cpu_utilization > 0.5:  # If more than 50% CPU utilized, assume node has a job
            if not render_node.current_job_id:
                render_node.current_job_id = f"estimated_job_{render_node.id}"
        else:
            render_node.current_job_id = None


class ResourceAdapter:
    """Adapter for resource requirement/capability conversions."""
    
    @staticmethod
    def extract_resource_requirements(render_job):
        """Extract resource requirements from RenderJob in common format."""
        from common.core.models import ResourceRequirement, ResourceType as CommonResourceType
        
        requirements = []
        
        # CPU requirements
        requirements.append(ResourceRequirement(
            resource_type=CommonResourceType.CPU,
            amount=float(render_job.cpu_requirements),
            unit="cores"
        ))
        
        # Memory requirements
        requirements.append(ResourceRequirement(
            resource_type=CommonResourceType.MEMORY,
            amount=float(render_job.memory_requirements_gb),
            unit="GB"
        ))
        
        # GPU requirements
        if render_job.requires_gpu:
            requirements.append(ResourceRequirement(
                resource_type=CommonResourceType.GPU,
                amount=1.0,
                unit="devices"
            ))
        
        return requirements
    
    @staticmethod
    def extract_node_capabilities(render_node):
        """Extract node capabilities in common format."""
        from common.core.models import ResourceCapability, ResourceType as CommonResourceType
        
        capabilities = []
        
        # CPU capability
        capabilities.append(ResourceCapability(
            resource_type=CommonResourceType.CPU,
            total_amount=float(render_node.capabilities.cpu_cores),
            available_amount=float(render_node.capabilities.cpu_cores),  # Will be updated based on load
            unit="cores"
        ))
        
        # Memory capability
        capabilities.append(ResourceCapability(
            resource_type=CommonResourceType.MEMORY,
            total_amount=float(render_node.capabilities.memory_gb),
            available_amount=float(render_node.capabilities.memory_gb),  # Will be updated based on load
            unit="GB"
        ))
        
        # GPU capability
        if render_node.capabilities.gpu_count > 0:
            capabilities.append(ResourceCapability(
                resource_type=CommonResourceType.GPU,
                total_amount=float(render_node.capabilities.gpu_count),
                available_amount=float(render_node.capabilities.gpu_count),  # Will be updated based on load
                unit="devices"
            ))
        
        return capabilities