# Unified Concurrent Task Scheduler Architecture Plan

## Executive Summary

This document outlines the architecture for creating a unified library from two persona-specific task scheduler implementations: Scientific Computing and Render Farm Manager. The goal is to extract common functionality while preserving domain-specific capabilities.

## Analysis Summary

### Common Patterns Identified

**Core Models:**
- **Task/Job Models**: Both use similar entities with id, name, status, priority, dependencies, and resource requirements
- **Node/Resource Models**: Both represent compute resources with CPU, memory, GPU capabilities and status tracking
- **Status Enums**: Similar status hierarchies (pending, running, completed, failed, etc.)
- **Priority Systems**: Multi-level priority schemes with inheritance and aging
- **Checkpoint Systems**: State preservation, validation, and restoration capabilities

**Scheduling Algorithms:**
- **Priority-based Scheduling**: Both use priority queues with multiple criteria
- **Deadline Awareness**: Time-sensitive scheduling with urgency calculations
- **Resource Matching**: Assignment based on resource requirements and node capabilities
- **Dependency Resolution**: Topological sorting and dependency chain handling
- **Preemption Support**: Higher priority job interruption with state preservation

**Resource Management:**
- **Allocation Strategies**: Fair-share, guaranteed minimums, and dynamic rebalancing
- **Resource Borrowing**: Inter-entity resource sharing with tracking
- **Utilization Monitoring**: Real-time usage tracking and historical analysis
- **Capacity Planning**: Resource forecasting and demand prediction

**Failure Handling:**
- **Detection Systems**: Multi-layered monitoring (heartbeat, metrics, predictive)
- **Recovery Strategies**: Restart, migration, checkpoint restoration
- **Resilience Coordination**: Centralized failure management and learning

**Utility Functions:**
- **Time Management**: Duration calculations, scheduling, timezone handling
- **ID Generation**: Unique identifiers with prefixes and collision avoidance
- **Serialization**: JSON encoding/decoding with datetime support
- **Validation**: Input validation and configuration checks
- **Audit Logging**: Event tracking with timestamps and metadata

### Domain-Specific Differences

**Scientific Computing Specializations:**
- **Simulation Stages**: Multi-stage workflows with complex dependencies
- **Research Metrics**: Scientific objectives, confidence scores, and evaluation criteria
- **Long-term Forecasting**: Resource projection for grant proposals and planning
- **Scenario Management**: Research scenario prioritization and comparative analysis
- **Advanced Failure Analysis**: Predictive failure detection and pattern learning

**Render Farm Manager Specializations:**
- **Render Deadlines**: Strict time constraints with urgency-based scheduling
- **Energy Optimization**: Power-aware scheduling with time-of-day pricing
- **Client SLAs**: Service level agreements with guaranteed resource allocations
- **Progressive Rendering**: Incremental output generation at configurable quality levels
- **Node Specialization**: Hardware-specific job placement (GPU rendering, simulation)

## Unified Library Architecture

### Directory Structure

```
common/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── models.py           # Base models and data structures
│   ├── interfaces.py       # Abstract interfaces
│   ├── scheduler.py        # Core scheduling algorithms
│   ├── resource_manager.py # Resource allocation and management
│   ├── checkpoint.py       # Checkpoint management
│   ├── dependency.py       # Dependency resolution
│   ├── failure_recovery.py # Failure detection and recovery
│   └── utils.py           # Utility functions
├── monitoring/
│   ├── __init__.py
│   ├── metrics.py         # Performance metrics
│   └── audit.py           # Audit logging
└── exceptions.py          # Common exception classes
```

## Core Components Design

### 1. Base Models (`common/core/models.py`)

```python
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pydantic import BaseModel

class TaskStatus(Enum):
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class NodeStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"
    ERROR = "error"

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class ResourceType(Enum):
    CPU = "cpu"
    MEMORY = "memory"
    GPU = "gpu"
    STORAGE = "storage"

class BaseTask(BaseModel):
    """Base task model with common fields across all personas"""
    id: str
    name: str
    status: TaskStatus
    priority: Priority
    submission_time: datetime
    estimated_duration: timedelta
    progress: float = 0.0
    dependencies: List[str] = []
    metadata: Dict[str, Any] = {}
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            timedelta: lambda v: v.total_seconds()
        }

class BaseNode(BaseModel):
    """Base node model with common fields across all personas"""
    id: str
    name: str
    status: NodeStatus
    cpu_cores: int
    memory_gb: float
    gpu_count: int = 0
    current_load: Dict[ResourceType, float] = {}
    
class ResourceRequirement(BaseModel):
    resource_type: ResourceType
    amount: float
    unit: str

class ResourceCapability(BaseModel):
    resource_type: ResourceType
    total_amount: float
    available_amount: float
    unit: str

class CheckpointMetadata(BaseModel):
    creation_time: datetime
    size_bytes: int
    checksum: str
    entity_type: str
    entity_id: str

class BaseCheckpoint(BaseModel):
    id: str
    metadata: CheckpointMetadata
    status: str
    path: str
    data: Dict[str, Any] = {}
```

### 2. Core Interfaces (`common/core/interfaces.py`)

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from .models import BaseTask, BaseNode, BaseCheckpoint, ResourceRequirement

class SchedulerInterface(ABC):
    """Abstract interface for task scheduling"""
    
    @abstractmethod
    def schedule_tasks(self, tasks: List[BaseTask], nodes: List[BaseNode]) -> Dict[str, str]:
        """Schedule tasks to nodes. Returns mapping of task_id -> node_id"""
        pass
    
    @abstractmethod
    def update_priorities(self, tasks: List[BaseTask]) -> List[BaseTask]:
        """Update task priorities based on scheduling policies"""
        pass
    
    @abstractmethod
    def can_meet_deadline(self, task: BaseTask, nodes: List[BaseNode]) -> bool:
        """Check if task can meet its deadline"""
        pass

class ResourceManagerInterface(ABC):
    """Abstract interface for resource management"""
    
    @abstractmethod
    def allocate_resources(self, entities: List[Any], nodes: List[BaseNode]) -> Dict[str, Dict[str, float]]:
        """Allocate resources to entities"""
        pass
    
    @abstractmethod
    def calculate_resource_usage(self, entity_id: str, tasks: List[BaseTask]) -> Dict[str, float]:
        """Calculate resource usage for an entity"""
        pass

class CheckpointManagerInterface(ABC):
    """Abstract interface for checkpoint management"""
    
    @abstractmethod
    def create_checkpoint(self, entity: Any, checkpoint_type: str) -> BaseCheckpoint:
        """Create a checkpoint for an entity"""
        pass
    
    @abstractmethod
    def validate_checkpoint(self, checkpoint_id: str) -> bool:
        """Validate a checkpoint"""
        pass
    
    @abstractmethod
    def restore_from_checkpoint(self, checkpoint_id: str) -> bool:
        """Restore from a checkpoint"""
        pass

class AuditLogInterface(ABC):
    """Abstract interface for audit logging"""
    
    @abstractmethod
    def log_event(self, event_type: str, description: str, **details) -> None:
        """Log an audit event"""
        pass
```

### 3. Core Scheduler (`common/core/scheduler.py`)

```python
from typing import Dict, List, Optional
from .models import BaseTask, BaseNode, Priority, TaskStatus
from .interfaces import SchedulerInterface

class BaseScheduler(SchedulerInterface):
    """Base scheduler implementation with common scheduling logic"""
    
    def __init__(self):
        self.priority_weights = {
            Priority.LOW: 1,
            Priority.MEDIUM: 2,
            Priority.HIGH: 3,
            Priority.CRITICAL: 4
        }
    
    def schedule_tasks(self, tasks: List[BaseTask], nodes: List[BaseNode]) -> Dict[str, str]:
        """Basic priority-based scheduling algorithm"""
        # Sort tasks by priority and submission time
        sorted_tasks = sorted(
            tasks, 
            key=lambda t: (self.priority_weights[t.priority], t.submission_time),
            reverse=True
        )
        
        # Simple round-robin assignment to available nodes
        available_nodes = [n for n in nodes if n.status.value == "online"]
        schedule = {}
        
        for i, task in enumerate(sorted_tasks):
            if available_nodes:
                node = available_nodes[i % len(available_nodes)]
                schedule[task.id] = node.id
        
        return schedule
    
    def update_priorities(self, tasks: List[BaseTask]) -> List[BaseTask]:
        """Update task priorities based on aging and dependencies"""
        # Simple aging algorithm - increase priority for waiting tasks
        for task in tasks:
            if task.status == TaskStatus.QUEUED:
                # Age tasks that have been waiting
                wait_time = (datetime.now() - task.submission_time).total_seconds()
                if wait_time > 3600:  # 1 hour
                    if task.priority != Priority.CRITICAL:
                        task.priority = Priority(min(task.priority.value + 1, 4))
        
        return tasks
    
    def can_meet_deadline(self, task: BaseTask, nodes: List[BaseNode]) -> bool:
        """Basic deadline checking"""
        if 'deadline' not in task.metadata:
            return True
        
        deadline = datetime.fromisoformat(task.metadata['deadline'])
        available_time = (deadline - datetime.now()).total_seconds()
        
        return available_time >= task.estimated_duration.total_seconds()
```

### 4. Resource Manager (`common/core/resource_manager.py`)

```python
from typing import Dict, List, Any
from .models import BaseNode, BaseTask, ResourceType
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
            if task.status.value == "running":
                # Extract resource requirements from metadata
                requirements = task.metadata.get('resource_requirements', {})
                for resource_type, amount in requirements.items():
                    if resource_type in usage:
                        usage[resource_type] += amount
        
        return usage
    
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
```

### 5. Dependency Manager (`common/core/dependency.py`)

```python
from typing import Dict, List, Set
from collections import defaultdict, deque
from .models import BaseTask

class DependencyResolver:
    """Handles dependency resolution and topological sorting"""
    
    def resolve_dependencies(self, tasks: List[BaseTask]) -> List[BaseTask]:
        """Resolve task dependencies using topological sort"""
        # Build dependency graph
        graph = defaultdict(list)
        in_degree = defaultdict(int)
        task_map = {task.id: task for task in tasks}
        
        for task in tasks:
            for dep_id in task.dependencies:
                if dep_id in task_map:
                    graph[dep_id].append(task.id)
                    in_degree[task.id] += 1
        
        # Topological sort
        queue = deque([task_id for task_id in task_map.keys() if in_degree[task_id] == 0])
        sorted_tasks = []
        
        while queue:
            current_id = queue.popleft()
            sorted_tasks.append(task_map[current_id])
            
            for neighbor in graph[current_id]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Check for cycles
        if len(sorted_tasks) != len(tasks):
            raise ValueError("Circular dependency detected")
        
        return sorted_tasks
    
    def check_dependencies_ready(self, task: BaseTask, completed_tasks: Set[str]) -> bool:
        """Check if all dependencies for a task are completed"""
        return all(dep_id in completed_tasks for dep_id in task.dependencies)
```

### 6. Utilities (`common/core/utils.py`)

```python
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import uuid4

def generate_id(prefix: str = "") -> str:
    """Generate a unique ID with optional prefix"""
    return f"{prefix}{uuid4().hex[:8]}" if prefix else uuid4().hex[:8]

def datetime_parser(json_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Parse datetime strings in JSON dictionaries"""
    for key, value in json_dict.items():
        if isinstance(value, str) and key.endswith('_time'):
            try:
                json_dict[key] = datetime.fromisoformat(value)
            except ValueError:
                pass
    return json_dict

class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder for datetime objects"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def calculate_checksum(data: bytes) -> str:
    """Calculate SHA-256 checksum of data"""
    return hashlib.sha256(data).hexdigest()

class Result:
    """Result wrapper for error handling"""
    def __init__(self, value: Any = None, error: Exception = None):
        self.value = value
        self.error = error
        self.is_success = error is None
    
    def unwrap(self):
        if self.error:
            raise self.error
        return self.value
    
    @classmethod
    def ok(cls, value: Any):
        return cls(value=value)
    
    @classmethod
    def error(cls, error: Exception):
        return cls(error=error)
```

## Migration Strategy

### Phase 1: Common Library Implementation
1. Create base models and interfaces
2. Implement core scheduling and resource management
3. Add utility functions and monitoring
4. Create comprehensive tests for common functionality

### Phase 2: Scientific Computing Migration
1. Extend base models for simulation-specific fields
2. Implement specialized schedulers inheriting from BaseScheduler
3. Create simulation-specific resource managers
4. Migrate existing code to use common library
5. Verify all tests pass

### Phase 3: Render Farm Manager Migration
1. Extend base models for render-specific fields
2. Implement render-specific schedulers and resource managers
3. Add energy optimization and progressive rendering
4. Migrate existing code to use common library
5. Verify all tests pass

### Phase 4: Integration Testing
1. Run comprehensive test suite
2. Performance benchmarking
3. Generate final report.json
4. Update documentation

## Extension Points

### For Scientific Computing:
- `ScientificTask(BaseTask)` - adds simulation-specific fields
- `ScientificScheduler(BaseScheduler)` - adds research priority logic
- `SimulationResourceManager(BaseResourceManager)` - adds forecasting

### For Render Farm Manager:
- `RenderTask(BaseTask)` - adds render-specific fields
- `RenderScheduler(BaseScheduler)` - adds deadline and energy optimization
- `RenderResourceManager(BaseResourceManager)` - adds client SLA handling

## Benefits of This Architecture

1. **Code Reuse**: ~60% of code can be shared between personas
2. **Maintainability**: Common bugs fixed once, benefit both personas
3. **Extensibility**: New personas can be added easily
4. **Testing**: Shared components have comprehensive test coverage
5. **Performance**: Optimizations in common library benefit all personas

## Implementation Priority

1. **High Priority**: Base models, interfaces, scheduler, resource manager
2. **Medium Priority**: Dependency resolution, checkpoint management, utilities
3. **Low Priority**: Advanced monitoring, audit logging, performance optimization

This architecture provides a solid foundation for the unified library while maintaining the flexibility needed for domain-specific extensions.