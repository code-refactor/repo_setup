from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Union, Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DatasetFormat(str, Enum):
    """Supported dataset formats."""
    
    CSV = "csv"
    JSON = "json"
    PARQUET = "parquet"
    HDF5 = "hdf5"
    EXCEL = "excel"
    SQL = "sql"
    PICKLE = "pickle"
    NUMPY = "numpy"
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    OTHER = "other"


class DatasetStorageType(str, Enum):
    """Types of dataset storage."""
    
    LOCAL = "local"
    S3 = "s3"
    GCS = "gs"
    AZURE = "azure"
    HTTP = "http"
    DATABASE = "database"
    GIT_LFS = "git_lfs"
    DVC = "dvc"
    OTHER = "other"


class DataTransformationType(str, Enum):
    """Types of data transformations."""
    
    CLEANING = "cleaning"
    NORMALIZATION = "normalization"
    AGGREGATION = "aggregation"
    FILTERING = "filtering"
    FEATURE_ENGINEERING = "feature_engineering"
    IMPUTATION = "imputation"
    ENCODING = "encoding"
    DIMENSIONALITY_REDUCTION = "dimensionality_reduction"
    RESAMPLING = "resampling"
    SPLITTING = "splitting"
    AUGMENTATION = "augmentation"
    OTHER = "other"


class Dataset(BaseModel):
    """Model representing a dataset."""
    
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: Optional[str] = None
    format: DatasetFormat
    storage_type: DatasetStorageType
    location: str  # Path or URL to the dataset
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Metadata
    size_bytes: Optional[int] = None
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    schema: Optional[Dict[str, str]] = None  # Column name -> data type
    tags: Set[str] = Field(default_factory=set)
    custom_metadata: Dict[str, Union[str, int, float, bool, list, dict]] = Field(
        default_factory=dict
    )
    
    # Version control
    hash: Optional[str] = None  # Content hash for verification
    version: Optional[str] = None  # Version identifier
    parent_dataset_id: Optional[UUID] = None  # Previous version in lineage
    
    # Additional properties for integration tests
    # This isn't persisted, but used for convenience in tests
    versions: List[Any] = Field(default_factory=list, exclude=True)
    
    def update(self, **kwargs) -> None:
        """Update dataset fields."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the dataset."""
        self.tags.add(tag)
        self.updated_at = datetime.now()
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the dataset."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()
    
    def update_custom_metadata(self, key: str, value: Union[str, int, float, bool, list, dict]) -> None:
        """Update a custom metadata field."""
        self.custom_metadata[key] = value
        self.updated_at = datetime.now()
    
    def remove_custom_metadata(self, key: str) -> bool:
        """
        Remove a custom metadata field.
        
        Args:
            key: The key of the custom field to remove
            
        Returns:
            bool: True if field was removed, False if not found
        """
        if key in self.custom_metadata:
            del self.custom_metadata[key]
            self.updated_at = datetime.now()
            return True
        return False


class DatasetVersion(BaseModel):
    """Model representing a specific version of a dataset."""
    
    id: UUID = Field(default_factory=uuid4)
    dataset_id: UUID  # Reference to the dataset
    version_number: str  # Semantic version or other identifier
    created_at: datetime = Field(default_factory=datetime.now)
    creator: Optional[str] = None  # Who created this version
    description: Optional[str] = None  # What changed in this version
    
    # Version details
    location: str  # Path or URL to this specific version
    hash: Optional[str] = None  # Content hash for verification
    size_bytes: Optional[int] = None
    parent_version_id: Optional[UUID] = None  # Previous version
    
    # Metadata specific to this version
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    schema: Optional[Dict[str, str]] = None  # Column name -> data type
    custom_metadata: Dict[str, Union[str, int, float, bool, list, dict]] = Field(
        default_factory=dict
    )
    
    def update(self, **kwargs) -> None:
        """Update version fields."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def update_custom_metadata(self, key: str, value: Union[str, int, float, bool, list, dict]) -> None:
        """Update a custom metadata field."""
        self.custom_metadata[key] = value
    
    def remove_custom_metadata(self, key: str) -> bool:
        """
        Remove a custom metadata field.
        
        Args:
            key: The key of the custom field to remove
            
        Returns:
            bool: True if field was removed, False if not found
        """
        if key in self.custom_metadata:
            del self.custom_metadata[key]
            return True
        return False


class DataTransformation(BaseModel):
    """Model representing a transformation applied to a dataset."""
    
    id: UUID = Field(default_factory=uuid4)
    type: DataTransformationType
    name: str  # Name of the transformation
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    
    # Input and output datasets
    input_dataset_version_id: UUID  # Version ID of the input dataset
    output_dataset_version_id: UUID  # Version ID of the output dataset
    
    # Transformation details
    parameters: Dict[str, Union[str, int, float, bool, list, dict]] = Field(
        default_factory=dict
    )  # Parameters used in the transformation
    code_reference: Optional[str] = None  # Reference to the code that performed the transformation
    execution_time_seconds: Optional[float] = None  # How long the transformation took
    
    # Metadata
    tags: Set[str] = Field(default_factory=set)
    notes: List[str] = Field(default_factory=list)
    
    def update(self, **kwargs) -> None:
        """Update transformation fields."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the transformation."""
        self.tags.add(tag)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the transformation."""
        if tag in self.tags:
            self.tags.remove(tag)
    
    def add_note(self, note: str) -> None:
        """Add a note to the transformation."""
        self.notes.append(note)
    
    def update_parameter(self, key: str, value: Union[str, int, float, bool, list, dict]) -> None:
        """Update a transformation parameter."""
        self.parameters[key] = value
    
    def remove_parameter(self, key: str) -> bool:
        """
        Remove a transformation parameter.
        
        Args:
            key: The key of the parameter to remove
            
        Returns:
            bool: True if parameter was removed, False if not found
        """
        if key in self.parameters:
            del self.parameters[key]
            return True
        return False


class TaskDatasetLink(BaseModel):
    """Model representing a link between a research task and a dataset version."""
    
    id: UUID = Field(default_factory=uuid4)
    task_id: UUID
    dataset_version_id: UUID
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # Link metadata
    usage_type: Optional[str] = None  # How the dataset is used (input, output, reference, etc.)
    description: Optional[str] = None  # Description of how this dataset relates to the task
    notes: List[str] = Field(default_factory=list)
    
    def update(self, **kwargs) -> None:
        """Update link fields."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
    
    def add_note(self, note: str) -> None:
        """Add a note to the link."""
        self.notes.append(note)
        self.updated_at = datetime.now()