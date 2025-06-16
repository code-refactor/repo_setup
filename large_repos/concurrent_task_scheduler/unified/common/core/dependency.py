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
        
        # Initialize in_degree for all tasks
        for task_id in task_map.keys():
            if task_id not in in_degree:
                in_degree[task_id] = 0
        
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
    
    def get_ready_tasks(self, tasks: List[BaseTask], completed_tasks: Set[str]) -> List[BaseTask]:
        """Get all tasks that are ready to run (dependencies satisfied)"""
        ready_tasks = []
        for task in tasks:
            if (task.status.value in ["pending", "queued"] and 
                self.check_dependencies_ready(task, completed_tasks)):
                ready_tasks.append(task)
        return ready_tasks
    
    def find_circular_dependencies(self, tasks: List[BaseTask]) -> List[List[str]]:
        """Find circular dependencies in the task graph"""
        task_map = {task.id: task for task in tasks}
        visited = set()
        rec_stack = set()
        cycles = []
        
        def dfs(task_id: str, path: List[str]) -> None:
            if task_id in rec_stack:
                # Found a cycle
                cycle_start = path.index(task_id)
                cycles.append(path[cycle_start:] + [task_id])
                return
            
            if task_id in visited:
                return
            
            visited.add(task_id)
            rec_stack.add(task_id)
            path.append(task_id)
            
            if task_id in task_map:
                for dep_id in task_map[task_id].dependencies:
                    if dep_id in task_map:
                        dfs(dep_id, path.copy())
            
            rec_stack.remove(task_id)
        
        for task in tasks:
            if task.id not in visited:
                dfs(task.id, [])
        
        return cycles
    
    def get_dependency_chain(self, task_id: str, tasks: List[BaseTask]) -> List[str]:
        """Get the full dependency chain for a task"""
        task_map = {task.id: task for task in tasks}
        if task_id not in task_map:
            return []
        
        visited = set()
        chain = []
        
        def build_chain(current_id: str) -> None:
            if current_id in visited or current_id not in task_map:
                return
            
            visited.add(current_id)
            task = task_map[current_id]
            
            # First add dependencies
            for dep_id in task.dependencies:
                build_chain(dep_id)
            
            # Then add current task
            chain.append(current_id)
        
        build_chain(task_id)
        return chain
    
    def calculate_critical_path(self, tasks: List[BaseTask]) -> List[str]:
        """Calculate the critical path (longest path) through the dependency graph"""
        task_map = {task.id: task for task in tasks}
        
        # Calculate earliest start times
        earliest_start = {}
        
        def calculate_earliest_start(task_id: str) -> float:
            if task_id in earliest_start:
                return earliest_start[task_id]
            
            if task_id not in task_map:
                return 0.0
            
            task = task_map[task_id]
            max_dep_time = 0.0
            
            for dep_id in task.dependencies:
                dep_end_time = (calculate_earliest_start(dep_id) + 
                               task_map[dep_id].estimated_duration.total_seconds())
                max_dep_time = max(max_dep_time, dep_end_time)
            
            earliest_start[task_id] = max_dep_time
            return max_dep_time
        
        # Calculate for all tasks
        for task in tasks:
            calculate_earliest_start(task.id)
        
        # Find the task with the latest end time
        latest_end_time = 0.0
        end_task = None
        
        for task in tasks:
            end_time = earliest_start[task.id] + task.estimated_duration.total_seconds()
            if end_time > latest_end_time:
                latest_end_time = end_time
                end_task = task.id
        
        # Trace back the critical path
        if not end_task:
            return []
        
        return self.get_dependency_chain(end_task, tasks)