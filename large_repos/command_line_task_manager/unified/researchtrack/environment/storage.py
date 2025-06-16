from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Set, Union
from uuid import UUID

from .models import (
    EnvironmentSnapshot, 
    PackageInfo, 
    ComputeResource, 
    TaskEnvironmentLink
)


class EnvironmentStorageInterface(ABC):
    """Abstract interface for environment snapshot storage implementations."""
    
    @abstractmethod
    def create_environment(self, environment: EnvironmentSnapshot) -> UUID:
        """
        Create a new environment snapshot.
        
        Args:
            environment: The environment to create
            
        Returns:
            UUID: The ID of the created environment
        """
        pass
    
    @abstractmethod
    def get_environment(self, environment_id: UUID) -> Optional[EnvironmentSnapshot]:
        """
        Retrieve an environment by ID.
        
        Args:
            environment_id: The ID of the environment to retrieve
            
        Returns:
            Optional[EnvironmentSnapshot]: The environment if found, None otherwise
        """
        pass
    
    @abstractmethod
    def update_environment(self, environment: EnvironmentSnapshot) -> bool:
        """
        Update an existing environment.
        
        Args:
            environment: The environment with updated fields
            
        Returns:
            bool: True if update successful, False otherwise
        """
        pass
    
    @abstractmethod
    def delete_environment(self, environment_id: UUID) -> bool:
        """
        Delete an environment by ID.
        
        Args:
            environment_id: The ID of the environment to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        pass
    
    @abstractmethod
    def list_environments(
        self, type: Optional[str] = None, tags: Optional[Set[str]] = None
    ) -> List[EnvironmentSnapshot]:
        """
        List environments with optional filtering.
        
        Args:
            type: Filter by environment type
            tags: Filter by tags (environments must have all specified tags)
            
        Returns:
            List[EnvironmentSnapshot]: List of environments matching the criteria
        """
        pass
    
    @abstractmethod
    def create_task_environment_link(self, link: TaskEnvironmentLink) -> UUID:
        """
        Create a link between a task and an environment snapshot.
        
        Args:
            link: The link to create
            
        Returns:
            UUID: The ID of the created link
        """
        pass
    
    @abstractmethod
    def get_task_environment_link(self, link_id: UUID) -> Optional[TaskEnvironmentLink]:
        """
        Retrieve a task-environment link by ID.
        
        Args:
            link_id: The ID of the link to retrieve
            
        Returns:
            Optional[TaskEnvironmentLink]: The link if found, None otherwise
        """
        pass
    
    @abstractmethod
    def update_task_environment_link(self, link: TaskEnvironmentLink) -> bool:
        """
        Update an existing task-environment link.
        
        Args:
            link: The link with updated fields
            
        Returns:
            bool: True if update successful, False otherwise
        """
        pass
    
    @abstractmethod
    def delete_task_environment_link(self, link_id: UUID) -> bool:
        """
        Delete a task-environment link by ID.
        
        Args:
            link_id: The ID of the link to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_environments_by_task(self, task_id: UUID) -> List[EnvironmentSnapshot]:
        """
        Get all environment snapshots associated with a task.
        
        Args:
            task_id: The ID of the task
            
        Returns:
            List[EnvironmentSnapshot]: List of associated environments
        """
        pass
    
    @abstractmethod
    def get_tasks_by_environment(self, environment_id: UUID) -> List[UUID]:
        """
        Get all task IDs associated with an environment.
        
        Args:
            environment_id: The ID of the environment
            
        Returns:
            List[UUID]: List of associated task IDs
        """
        pass
        
    @abstractmethod
    def get_links_by_task(self, task_id: UUID) -> List[TaskEnvironmentLink]:
        """
        Get all environment links for a specific task.
        
        Args:
            task_id: The ID of the task
            
        Returns:
            List[TaskEnvironmentLink]: List of task-environment links for this task
        """
        pass


class InMemoryEnvironmentStorage(EnvironmentStorageInterface):
    """In-memory implementation of environment snapshot storage."""
    
    def __init__(self):
        self._environments: Dict[UUID, EnvironmentSnapshot] = {}
        self._task_environment_links: Dict[UUID, TaskEnvironmentLink] = {}
    
    def create_environment(self, environment: EnvironmentSnapshot) -> UUID:
        self._environments[environment.id] = environment
        return environment.id
    
    def get_environment(self, environment_id: UUID) -> Optional[EnvironmentSnapshot]:
        return self._environments.get(environment_id)
    
    def update_environment(self, environment: EnvironmentSnapshot) -> bool:
        if environment.id not in self._environments:
            return False
        self._environments[environment.id] = environment
        return True
    
    def delete_environment(self, environment_id: UUID) -> bool:
        if environment_id not in self._environments:
            return False
        
        # Delete the environment
        del self._environments[environment_id]
        
        # Delete any links that reference this environment
        links_to_delete = [
            link_id for link_id, link in self._task_environment_links.items()
            if link.environment_id == environment_id
        ]
        for link_id in links_to_delete:
            self.delete_task_environment_link(link_id)
        
        return True
    
    def list_environments(
        self, type: Optional[str] = None, tags: Optional[Set[str]] = None
    ) -> List[EnvironmentSnapshot]:
        environments = list(self._environments.values())
        
        if type:
            environments = [
                env for env in environments if env.type == type
            ]
        
        if tags:
            environments = [
                env for env in environments
                if all(tag in env.tags for tag in tags)
            ]
        
        return environments
    
    def create_task_environment_link(self, link: TaskEnvironmentLink) -> UUID:
        self._task_environment_links[link.id] = link
        return link.id
    
    def get_task_environment_link(self, link_id: UUID) -> Optional[TaskEnvironmentLink]:
        return self._task_environment_links.get(link_id)
    
    def update_task_environment_link(self, link: TaskEnvironmentLink) -> bool:
        if link.id not in self._task_environment_links:
            return False
        self._task_environment_links[link.id] = link
        return True
    
    def delete_task_environment_link(self, link_id: UUID) -> bool:
        if link_id not in self._task_environment_links:
            return False
        del self._task_environment_links[link_id]
        return True
    
    def get_environments_by_task(self, task_id: UUID) -> List[EnvironmentSnapshot]:
        # Get all links for this task
        links = [
            link for link in self._task_environment_links.values()
            if link.task_id == task_id
        ]
        
        # Get all associated environments
        environments = []
        for link in links:
            environment = self.get_environment(link.environment_id)
            if environment:
                environments.append(environment)
        
        return environments
    
    def get_tasks_by_environment(self, environment_id: UUID) -> List[UUID]:
        # Get all links for this environment
        links = [
            link for link in self._task_environment_links.values()
            if link.environment_id == environment_id
        ]
        
        # Return task IDs
        return [link.task_id for link in links]
        
    def get_links_by_task(self, task_id: UUID) -> List[TaskEnvironmentLink]:
        # Get all links for this task
        return [
            link for link in self._task_environment_links.values()
            if link.task_id == task_id
        ]