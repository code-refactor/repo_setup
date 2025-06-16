from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Set, Union
from uuid import UUID

from .models import Dataset, DatasetVersion, DataTransformation, TaskDatasetLink


class DatasetStorageInterface(ABC):
    """Abstract interface for dataset versioning storage implementations."""
    
    @abstractmethod
    def create_dataset(self, dataset: Dataset) -> UUID:
        """
        Create a new dataset.
        
        Args:
            dataset: The dataset to create
            
        Returns:
            UUID: The ID of the created dataset
        """
        pass
    
    @abstractmethod
    def get_dataset(self, dataset_id: UUID) -> Optional[Dataset]:
        """
        Retrieve a dataset by ID.
        
        Args:
            dataset_id: The ID of the dataset to retrieve
            
        Returns:
            Optional[Dataset]: The dataset if found, None otherwise
        """
        pass
    
    @abstractmethod
    def update_dataset(self, dataset: Dataset) -> bool:
        """
        Update an existing dataset.
        
        Args:
            dataset: The dataset with updated fields
            
        Returns:
            bool: True if update successful, False otherwise
        """
        pass
    
    @abstractmethod
    def delete_dataset(self, dataset_id: UUID) -> bool:
        """
        Delete a dataset by ID.
        
        Args:
            dataset_id: The ID of the dataset to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        pass
    
    @abstractmethod
    def list_datasets(
        self, format: Optional[str] = None, storage_type: Optional[str] = None, tags: Optional[Set[str]] = None
    ) -> List[Dataset]:
        """
        List datasets with optional filtering.
        
        Args:
            format: Filter by dataset format
            storage_type: Filter by storage type
            tags: Filter by tags (datasets must have all specified tags)
            
        Returns:
            List[Dataset]: List of datasets matching the criteria
        """
        pass
    
    @abstractmethod
    def create_dataset_version(self, version: DatasetVersion) -> UUID:
        """
        Create a new dataset version.
        
        Args:
            version: The dataset version to create
            
        Returns:
            UUID: The ID of the created version
        """
        pass
    
    @abstractmethod
    def get_dataset_version(self, version_id: UUID) -> Optional[DatasetVersion]:
        """
        Retrieve a dataset version by ID.
        
        Args:
            version_id: The ID of the version to retrieve
            
        Returns:
            Optional[DatasetVersion]: The version if found, None otherwise
        """
        pass
    
    @abstractmethod
    def update_dataset_version(self, version: DatasetVersion) -> bool:
        """
        Update an existing dataset version.
        
        Args:
            version: The version with updated fields
            
        Returns:
            bool: True if update successful, False otherwise
        """
        pass
    
    @abstractmethod
    def delete_dataset_version(self, version_id: UUID) -> bool:
        """
        Delete a dataset version by ID.
        
        Args:
            version_id: The ID of the version to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        pass
    
    @abstractmethod
    def list_dataset_versions(
        self, dataset_id: UUID, include_lineage: bool = False
    ) -> List[DatasetVersion]:
        """
        List versions of a dataset.
        
        Args:
            dataset_id: The ID of the dataset
            include_lineage: Whether to include full version lineage
            
        Returns:
            List[DatasetVersion]: List of dataset versions
        """
        pass
    
    @abstractmethod
    def create_data_transformation(self, transformation: DataTransformation) -> UUID:
        """
        Create a new data transformation.
        
        Args:
            transformation: The data transformation to create
            
        Returns:
            UUID: The ID of the created transformation
        """
        pass
    
    @abstractmethod
    def get_data_transformation(
        self, transformation_id: UUID
    ) -> Optional[DataTransformation]:
        """
        Retrieve a data transformation by ID.
        
        Args:
            transformation_id: The ID of the transformation to retrieve
            
        Returns:
            Optional[DataTransformation]: The transformation if found, None otherwise
        """
        pass
    
    @abstractmethod
    def update_data_transformation(self, transformation: DataTransformation) -> bool:
        """
        Update an existing data transformation.
        
        Args:
            transformation: The transformation with updated fields
            
        Returns:
            bool: True if update successful, False otherwise
        """
        pass
    
    @abstractmethod
    def delete_data_transformation(self, transformation_id: UUID) -> bool:
        """
        Delete a data transformation by ID.
        
        Args:
            transformation_id: The ID of the transformation to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        pass
    
    @abstractmethod
    def list_transformations_for_dataset(self, dataset_id: UUID) -> List[DataTransformation]:
        """
        List all transformations related to a dataset.
        
        Args:
            dataset_id: The ID of the dataset
            
        Returns:
            List[DataTransformation]: List of data transformations
        """
        pass
        
    @abstractmethod
    def list_data_transformations(
        self,
        input_dataset_version_id: Optional[UUID] = None,
        output_dataset_version_id: Optional[UUID] = None,
        transformation_type: Optional[str] = None
    ) -> List[DataTransformation]:
        """
        List data transformations with optional filtering.
        
        Args:
            input_dataset_version_id: Filter by input dataset version ID
            output_dataset_version_id: Filter by output dataset version ID
            transformation_type: Filter by transformation type
            
        Returns:
            List[DataTransformation]: List of transformations matching the criteria
        """
        pass
    
    @abstractmethod
    def get_transformation_lineage(
        self, version_id: UUID
    ) -> List[DataTransformation]:
        """
        Get the complete transformation lineage for a dataset version.
        
        Args:
            version_id: The ID of the dataset version
            
        Returns:
            List[DataTransformation]: List of transformations in lineage order
        """
        pass
    
    @abstractmethod
    def find_transformations_by_input_version(self, version_id: UUID) -> List[DataTransformation]:
        """
        Find all transformations where the specified version is the input.
        
        Args:
            version_id: The ID of the dataset version
            
        Returns:
            List[DataTransformation]: List of transformations with this version as input
        """
        pass
    
    @abstractmethod
    def find_transformations_by_output_version(self, version_id: UUID) -> List[DataTransformation]:
        """
        Find all transformations where the specified version is the output.
        
        Args:
            version_id: The ID of the dataset version
            
        Returns:
            List[DataTransformation]: List of transformations with this version as output
        """
        pass
    
    @abstractmethod
    def create_task_dataset_link(self, link: TaskDatasetLink) -> UUID:
        """
        Create a link between a task and a dataset version.
        
        Args:
            link: The link to create
            
        Returns:
            UUID: The ID of the created link
        """
        pass
    
    @abstractmethod
    def get_task_dataset_link(self, link_id: UUID) -> Optional[TaskDatasetLink]:
        """
        Retrieve a task-dataset link by ID.
        
        Args:
            link_id: The ID of the link to retrieve
            
        Returns:
            Optional[TaskDatasetLink]: The link if found, None otherwise
        """
        pass
    
    @abstractmethod
    def update_task_dataset_link(self, link: TaskDatasetLink) -> bool:
        """
        Update an existing task-dataset link.
        
        Args:
            link: The link with updated fields
            
        Returns:
            bool: True if update successful, False otherwise
        """
        pass
    
    @abstractmethod
    def delete_task_dataset_link(self, link_id: UUID) -> bool:
        """
        Delete a task-dataset link by ID.
        
        Args:
            link_id: The ID of the link to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_dataset_versions_by_task(self, task_id: UUID) -> List[DatasetVersion]:
        """
        Get all dataset versions associated with a task.
        
        Args:
            task_id: The ID of the task
            
        Returns:
            List[DatasetVersion]: List of associated dataset versions
        """
        pass
    
    @abstractmethod
    def get_tasks_by_dataset_version(self, version_id: UUID) -> List[UUID]:
        """
        Get all task IDs associated with a dataset version.
        
        Args:
            version_id: The ID of the dataset version
            
        Returns:
            List[UUID]: List of associated task IDs
        """
        pass
    
    @abstractmethod
    def get_links_by_task(self, task_id: UUID) -> List[TaskDatasetLink]:
        """
        Get all dataset links for a specific task.
        
        Args:
            task_id: The ID of the task
            
        Returns:
            List[TaskDatasetLink]: List of task-dataset links for this task
        """
        pass


class InMemoryDatasetStorage(DatasetStorageInterface):
    """In-memory implementation of dataset versioning storage."""
    
    def __init__(self):
        self._datasets: Dict[UUID, Dataset] = {}
        self._versions: Dict[UUID, DatasetVersion] = {}
        self._transformations: Dict[UUID, DataTransformation] = {}
        self._task_dataset_links: Dict[UUID, TaskDatasetLink] = {}
    
    def create_dataset(self, dataset: Dataset) -> UUID:
        self._datasets[dataset.id] = dataset
        return dataset.id
    
    def get_dataset(self, dataset_id: UUID) -> Optional[Dataset]:
        return self._datasets.get(dataset_id)
    
    def update_dataset(self, dataset: Dataset) -> bool:
        if dataset.id not in self._datasets:
            return False
        self._datasets[dataset.id] = dataset
        return True
    
    def delete_dataset(self, dataset_id: UUID) -> bool:
        if dataset_id not in self._datasets:
            return False
        
        # Delete the dataset
        del self._datasets[dataset_id]
        
        # Delete all versions of this dataset
        versions_to_delete = [
            ver_id for ver_id, ver in self._versions.items() 
            if ver.dataset_id == dataset_id
        ]
        for ver_id in versions_to_delete:
            self.delete_dataset_version(ver_id)
        
        return True
    
    def list_datasets(
        self, format: Optional[str] = None, storage_type: Optional[str] = None, tags: Optional[Set[str]] = None
    ) -> List[Dataset]:
        datasets = list(self._datasets.values())
        
        if format:
            datasets = [ds for ds in datasets if ds.format == format]
            
        if storage_type:
            datasets = [ds for ds in datasets if ds.storage_type == storage_type]
        
        if tags:
            datasets = [
                ds for ds in datasets if all(tag in ds.tags for tag in tags)
            ]
        
        return datasets
    
    def create_dataset_version(self, version: DatasetVersion) -> UUID:
        self._versions[version.id] = version
        return version.id
    
    def get_dataset_version(self, version_id: UUID) -> Optional[DatasetVersion]:
        return self._versions.get(version_id)
    
    def update_dataset_version(self, version: DatasetVersion) -> bool:
        if version.id not in self._versions:
            return False
        self._versions[version.id] = version
        return True
    
    def delete_dataset_version(self, version_id: UUID) -> bool:
        if version_id not in self._versions:
            return False
        
        # Get the version before deleting
        version = self._versions[version_id]
        
        # Delete the version
        del self._versions[version_id]
        
        # Delete any transformations that reference this version
        transformations_to_delete = [
            trans_id for trans_id, trans in self._transformations.items()
            if (trans.input_dataset_version_id == version_id or 
                trans.output_dataset_version_id == version_id)
        ]
        for trans_id in transformations_to_delete:
            self.delete_data_transformation(trans_id)
        
        # Delete any task-dataset links that reference this version
        links_to_delete = [
            link_id for link_id, link in self._task_dataset_links.items()
            if link.dataset_version_id == version_id
        ]
        for link_id in links_to_delete:
            self.delete_task_dataset_link(link_id)
            
        # Update parent references in children versions to maintain lineage integrity
        for child_version in self._versions.values():
            if child_version.parent_version_id == version_id:
                # Set parent_version_id to None when deleting a version in the chain
                child_version.parent_version_id = None
        
        return True
    
    def list_dataset_versions(
        self, dataset_id: UUID, include_lineage: bool = False
    ) -> List[DatasetVersion]:
        versions = [
            v for v in self._versions.values() if v.dataset_id == dataset_id
        ]
        
        if include_lineage:
            # Sort versions by their lineage
            # This is a simplified approach - for a real implementation,
            # a more sophisticated algorithm would be needed to handle branches
            
            # First, find the root versions (no parent)
            root_versions = [v for v in versions if v.parent_version_id is None]
            result = []
            
            # For each root, traverse its lineage
            for root in root_versions:
                result.append(root)
                current = root
                
                # Follow children
                while True:
                    children = [
                        v for v in versions if v.parent_version_id == current.id
                    ]
                    if not children:
                        break
                    
                    # Just take first child for simplicity
                    current = children[0]
                    result.append(current)
            
            return result
        
        return versions
    
    def create_data_transformation(self, transformation: DataTransformation) -> UUID:
        self._transformations[transformation.id] = transformation
        return transformation.id
    
    def get_data_transformation(
        self, transformation_id: UUID
    ) -> Optional[DataTransformation]:
        return self._transformations.get(transformation_id)
    
    def update_data_transformation(self, transformation: DataTransformation) -> bool:
        if transformation.id not in self._transformations:
            return False
        self._transformations[transformation.id] = transformation
        return True
    
    def delete_data_transformation(self, transformation_id: UUID) -> bool:
        if transformation_id not in self._transformations:
            return False
        del self._transformations[transformation_id]
        return True
    
    def list_transformations_for_dataset(self, dataset_id: UUID) -> List[DataTransformation]:
        # Get all versions for this dataset
        dataset_versions = self.list_dataset_versions(dataset_id)
        version_ids = {v.id for v in dataset_versions}
        
        # Get all transformations that involve these versions
        return [
            t for t in self._transformations.values()
            if (t.input_dataset_version_id in version_ids or 
                t.output_dataset_version_id in version_ids)
        ]
        
    def list_data_transformations(
        self,
        input_dataset_version_id: Optional[UUID] = None,
        output_dataset_version_id: Optional[UUID] = None,
        transformation_type: Optional[str] = None
    ) -> List[DataTransformation]:
        """
        List data transformations with optional filtering.
        
        Args:
            input_dataset_version_id: Filter by input dataset version ID
            output_dataset_version_id: Filter by output dataset version ID
            transformation_type: Filter by transformation type
            
        Returns:
            List[DataTransformation]: List of transformations matching the criteria
        """
        transformations = list(self._transformations.values())
        
        if input_dataset_version_id:
            transformations = [
                t for t in transformations 
                if t.input_dataset_version_id == input_dataset_version_id
            ]
            
        if output_dataset_version_id:
            transformations = [
                t for t in transformations 
                if t.output_dataset_version_id == output_dataset_version_id
            ]
            
        if transformation_type:
            transformations = [
                t for t in transformations 
                if t.type == transformation_type
            ]
            
        return transformations
    
    def get_latest_dataset_version(self, dataset_id: UUID) -> Optional[DatasetVersion]:
        """
        Get the latest version of a dataset based on creation timestamp.
        
        Args:
            dataset_id: The ID of the dataset
            
        Returns:
            Optional[DatasetVersion]: The latest version, or None if no versions exist
        """
        versions = self.list_dataset_versions(dataset_id)
        if not versions:
            return None
        return max(versions, key=lambda v: v.created_at)
    
    def get_lineage(self, version_id: UUID) -> Dict[str, Dict]:
        """
        Get the full lineage information for a dataset version.
        
        Args:
            version_id: The ID of the dataset version
            
        Returns:
            Dict[str, Dict]: A dictionary with version IDs as keys and lineage info as values
        """
        version = self.get_dataset_version(version_id)
        if not version:
            return {}
        
        # Build a map of all versions in the lineage
        lineage = {}
        versions_to_process = [version_id]
        processed_versions = set()
        
        while versions_to_process:
            current_version_id = versions_to_process.pop(0)
            if current_version_id in processed_versions:
                continue
                
            processed_versions.add(current_version_id)
            current_version = self.get_dataset_version(current_version_id)
            if not current_version:
                continue
                
            # Find transformations with this version as input or output
            input_transformations = self.find_transformations_by_output_version(current_version_id)
            output_transformations = self.find_transformations_by_input_version(current_version_id)
            
            # Add to lineage
            lineage[str(current_version_id)] = {
                "version": current_version,
                "input_transformations": input_transformations,
                "output_transformations": output_transformations
            }
            
            # Add parent version to process queue if it exists
            if current_version.parent_version_id:
                versions_to_process.append(current_version.parent_version_id)
                
            # Add versions linked via transformations
            for trans in input_transformations:
                if trans.input_dataset_version_id:
                    versions_to_process.append(trans.input_dataset_version_id)
                    
            for trans in output_transformations:
                if trans.output_dataset_version_id:
                    versions_to_process.append(trans.output_dataset_version_id)
        
        return lineage
        
    def get_transformation_lineage(
        self, version_id: UUID
    ) -> List[DataTransformation]:
        """
        Get the complete transformation lineage for a dataset version.
        
        This is a simplified implementation that just goes backwards from
        the specified version to find all transformations that led to it.
        """
        version = self.get_dataset_version(version_id)
        if not version:
            return []
        
        result = []
        current_version_id = version_id
        
        while current_version_id:
            # Find the transformation that produced this version
            transformations = [
                t for t in self._transformations.values()
                if t.output_dataset_version_id == current_version_id
            ]
            
            if not transformations:
                # No more transformations in lineage
                break
            
            # Add the transformation to the result (in reverse order)
            transformation = transformations[0]  # Just take first one if multiple
            result.insert(0, transformation)
            
            # Move to the input version
            current_version_id = transformation.input_dataset_version_id
        
        return result
    
    def find_transformations_by_input_version(self, version_id: UUID) -> List[DataTransformation]:
        """
        Find all transformations where the specified version is the input.
        
        Args:
            version_id: The ID of the dataset version
            
        Returns:
            List[DataTransformation]: List of transformations with this version as input
        """
        return [
            t for t in self._transformations.values() 
            if t.input_dataset_version_id == version_id
        ]
    
    def find_transformations_by_output_version(self, version_id: UUID) -> List[DataTransformation]:
        """
        Find all transformations where the specified version is the output.
        
        Args:
            version_id: The ID of the dataset version
            
        Returns:
            List[DataTransformation]: List of transformations with this version as output
        """
        return [
            t for t in self._transformations.values() 
            if t.output_dataset_version_id == version_id
        ]
    
    def create_task_dataset_link(self, link: TaskDatasetLink) -> UUID:
        self._task_dataset_links[link.id] = link
        return link.id
    
    def get_task_dataset_link(self, link_id: UUID) -> Optional[TaskDatasetLink]:
        return self._task_dataset_links.get(link_id)
    
    def update_task_dataset_link(self, link: TaskDatasetLink) -> bool:
        if link.id not in self._task_dataset_links:
            return False
        self._task_dataset_links[link.id] = link
        return True
    
    def delete_task_dataset_link(self, link_id: UUID) -> bool:
        if link_id not in self._task_dataset_links:
            return False
        del self._task_dataset_links[link_id]
        return True
    
    def get_dataset_versions_by_task(self, task_id: UUID) -> List[DatasetVersion]:
        # Get all links for this task
        links = [
            link for link in self._task_dataset_links.values()
            if link.task_id == task_id
        ]
        
        # Get all associated versions
        versions = []
        for link in links:
            version = self.get_dataset_version(link.dataset_version_id)
            if version:
                versions.append(version)
        
        return versions
    
    def get_tasks_by_dataset_version(self, version_id: UUID) -> List[UUID]:
        # Get all links for this dataset version
        links = [
            link for link in self._task_dataset_links.values()
            if link.dataset_version_id == version_id
        ]
        
        # Return task IDs
        return [link.task_id for link in links]
    
    def get_links_by_task(self, task_id: UUID) -> List[TaskDatasetLink]:
        """
        Get all dataset links for a specific task.
        
        Args:
            task_id: The ID of the task
            
        Returns:
            List[TaskDatasetLink]: List of task-dataset links for this task
        """
        return [
            link for link in self._task_dataset_links.values()
            if link.task_id == task_id
        ]