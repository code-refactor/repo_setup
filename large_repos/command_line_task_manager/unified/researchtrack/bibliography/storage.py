from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Set, Union
from uuid import UUID

from .models import Author, Reference, TaskReferenceLink


class BibliographyStorageInterface(ABC):
    """Abstract interface for bibliography storage implementations."""
    
    @abstractmethod
    def create_reference(self, reference: Reference) -> UUID:
        """
        Create a new reference.
        
        Args:
            reference: The reference to create
            
        Returns:
            UUID: The ID of the created reference
        """
        pass
    
    @abstractmethod
    def get_reference(self, reference_id: UUID) -> Optional[Reference]:
        """
        Retrieve a reference by ID.
        
        Args:
            reference_id: The ID of the reference to retrieve
            
        Returns:
            Optional[Reference]: The reference if found, None otherwise
        """
        pass
    
    @abstractmethod
    def update_reference(self, reference: Reference) -> bool:
        """
        Update an existing reference.
        
        Args:
            reference: The reference with updated fields
            
        Returns:
            bool: True if update successful, False otherwise
        """
        pass
    
    @abstractmethod
    def delete_reference(self, reference_id: UUID) -> bool:
        """
        Delete a reference by ID.
        
        Args:
            reference_id: The ID of the reference to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        pass
    
    @abstractmethod
    def list_references(
        self, author_name: Optional[str] = None, year: Optional[int] = None, 
        keywords: Optional[Set[str]] = None
    ) -> List[Reference]:
        """
        List references with optional filtering.
        
        Args:
            author_name: Filter by author name (partial match)
            year: Filter by publication year
            keywords: Filter by keywords (references must have all specified keywords)
            
        Returns:
            List[Reference]: List of references matching the criteria
        """
        pass
    
    @abstractmethod
    def create_task_reference_link(self, link: TaskReferenceLink) -> UUID:
        """
        Create a link between a task and a reference.
        
        Args:
            link: The link to create
            
        Returns:
            UUID: The ID of the created link
        """
        pass
    
    @abstractmethod
    def get_task_reference_link(self, link_id: UUID) -> Optional[TaskReferenceLink]:
        """
        Retrieve a task-reference link by ID.
        
        Args:
            link_id: The ID of the link to retrieve
            
        Returns:
            Optional[TaskReferenceLink]: The link if found, None otherwise
        """
        pass
    
    @abstractmethod
    def update_task_reference_link(self, link: TaskReferenceLink) -> bool:
        """
        Update an existing task-reference link.
        
        Args:
            link: The link with updated fields
            
        Returns:
            bool: True if update successful, False otherwise
        """
        pass
    
    @abstractmethod
    def delete_task_reference_link(self, link_id: UUID) -> bool:
        """
        Delete a task-reference link by ID.
        
        Args:
            link_id: The ID of the link to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_references_for_task(self, task_id: UUID) -> List[Reference]:
        """
        Get all references associated with a task.
        
        Args:
            task_id: The ID of the task
            
        Returns:
            List[Reference]: List of associated references
        """
        pass
    
    @abstractmethod
    def get_tasks_for_reference(self, reference_id: UUID) -> List[UUID]:
        """
        Get all task IDs associated with a reference.
        
        Args:
            reference_id: The ID of the reference
            
        Returns:
            List[UUID]: List of associated task IDs
        """
        pass
    
    @abstractmethod
    def get_links_by_task(self, task_id: UUID) -> List[TaskReferenceLink]:
        """
        Get all reference links for a specific task.
        
        Args:
            task_id: The ID of the task
            
        Returns:
            List[TaskReferenceLink]: List of task-reference links for this task
        """
        pass
    
    @abstractmethod
    def get_tasks_by_reference(self, reference_id: UUID) -> List[UUID]:
        """
        Alias for get_tasks_for_reference, to maintain API compatibility.
        
        Args:
            reference_id: The ID of the reference
            
        Returns:
            List[UUID]: List of associated task IDs
        """
        pass
        
    @abstractmethod
    def get_references_by_task(self, task_id: UUID) -> List[Reference]:
        """
        Alias for get_references_for_task, to maintain API compatibility.
        
        Args:
            task_id: The ID of the task
            
        Returns:
            List[Reference]: List of associated references
        """
        pass


class InMemoryBibliographyStorage(BibliographyStorageInterface):
    """In-memory implementation of bibliography storage."""
    
    def __init__(self):
        self._references: Dict[UUID, Reference] = {}
        self._task_reference_links: Dict[UUID, TaskReferenceLink] = {}
    
    def create_reference(self, reference: Reference) -> UUID:
        self._references[reference.id] = reference
        return reference.id
    
    def get_reference(self, reference_id: UUID) -> Optional[Reference]:
        return self._references.get(reference_id)
    
    def update_reference(self, reference: Reference) -> bool:
        if reference.id not in self._references:
            return False
        self._references[reference.id] = reference
        return True
    
    def delete_reference(self, reference_id: UUID) -> bool:
        if reference_id not in self._references:
            return False
        del self._references[reference_id]
        
        # Delete any links associated with this reference
        links_to_delete = [
            link_id for link_id, link in self._task_reference_links.items()
            if link.reference_id == reference_id
        ]
        for link_id in links_to_delete:
            del self._task_reference_links[link_id]
        
        return True
    
    def list_references(
        self, author_name: Optional[str] = None, year: Optional[int] = None, 
        keywords: Optional[Set[str]] = None
    ) -> List[Reference]:
        references = list(self._references.values())
        
        if author_name:
            author_name_lower = author_name.lower()
            references = [
                ref for ref in references if any(
                    author_name_lower in author.full_name().lower() 
                    for author in ref.authors
                )
            ]
        
        if year:
            references = [ref for ref in references if ref.year == year]
        
        if keywords:
            references = [
                ref for ref in references
                if all(keyword in ref.keywords for keyword in keywords)
            ]
        
        return references
    
    def create_task_reference_link(self, link: TaskReferenceLink) -> UUID:
        self._task_reference_links[link.id] = link
        return link.id
    
    def get_task_reference_link(self, link_id: UUID) -> Optional[TaskReferenceLink]:
        return self._task_reference_links.get(link_id)
    
    def update_task_reference_link(self, link: TaskReferenceLink) -> bool:
        if link.id not in self._task_reference_links:
            return False
        self._task_reference_links[link.id] = link
        return True
    
    def delete_task_reference_link(self, link_id: UUID) -> bool:
        if link_id not in self._task_reference_links:
            return False
        del self._task_reference_links[link_id]
        return True
    
    def get_references_for_task(self, task_id: UUID) -> List[Reference]:
        links = [
            link for link in self._task_reference_links.values()
            if link.task_id == task_id
        ]
        
        references = []
        for link in links:
            reference = self.get_reference(link.reference_id)
            if reference:
                references.append(reference)
                
        return references
    
    def get_tasks_for_reference(self, reference_id: UUID) -> List[UUID]:
        links = [
            link for link in self._task_reference_links.values()
            if link.reference_id == reference_id
        ]
        
        return [link.task_id for link in links]
    
    def get_links_by_task(self, task_id: UUID) -> List[TaskReferenceLink]:
        """
        Get all reference links for a specific task.
        
        Args:
            task_id: The ID of the task
            
        Returns:
            List[TaskReferenceLink]: List of task-reference links for this task
        """
        return [
            link for link in self._task_reference_links.values()
            if link.task_id == task_id
        ]
    
    def get_tasks_by_reference(self, reference_id: UUID) -> List[UUID]:
        """
        Alias for get_tasks_for_reference, to maintain API compatibility.
        
        Args:
            reference_id: The ID of the reference
            
        Returns:
            List[UUID]: List of associated task IDs
        """
        return self.get_tasks_for_reference(reference_id)
        
    def get_references_by_task(self, task_id: UUID) -> List[Reference]:
        """
        Alias for get_references_for_task, to maintain API compatibility.
        
        Args:
            task_id: The ID of the task
            
        Returns:
            List[Reference]: List of associated references
        """
        return self.get_references_for_task(task_id)