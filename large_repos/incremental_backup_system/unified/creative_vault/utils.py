"""
Utility functions for the CreativeVault backup system.

This module provides common utility functions used across the various
components of the CreativeVault backup system.

Note: Many functions have been moved to common.core modules for consistency.
This module now primarily provides creative-specific utilities and compatibility.
"""

import json
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union, BinaryIO

import numpy as np
from pydantic import BaseModel

# Import from common core for consistency
from common.core.models import FileInfo as UnifiedFileInfo, FileType
from common.core.config import UnifiedBackupConfig
from common.core.file_utils import (
    calculate_file_hash, get_file_type, scan_directory as unified_scan_directory,
    get_file_info, is_binary_file
)
from common.core.hashing import calculate_file_hash as core_calculate_file_hash


class FileInfo(BaseModel):
    """Information about a file tracked by the backup system.
    
    Note: This class is maintained for backward compatibility.
    New code should use common.core.models.FileInfo.
    """
    
    path: Path
    size: int
    modified_time: float
    hash: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Dict[str, Any] = {}
    
    def model_dump(self) -> Dict[str, Any]:
        """Convert to dictionary.
        
        Returns:
            Dictionary representation of this object
        """
        result = {
            "path": str(self.path),
            "size": self.size,
            "modified_time": self.modified_time,
            "hash": self.hash,
            "content_type": self.content_type,
            "metadata": self.metadata
        }
        return result
    
    def dict(self) -> Dict[str, Any]:
        """Convert to dictionary (for backwards compatibility).
        
        Returns:
            Dictionary representation of this object
        """
        return self.model_dump()
        
    @classmethod
    def from_unified_file_info(cls, unified_info: UnifiedFileInfo) -> 'FileInfo':
        """Create legacy FileInfo from unified FileInfo.
        
        Args:
            unified_info: UnifiedFileInfo instance
            
        Returns:
            Legacy FileInfo instance
        """
        return cls(
            path=unified_info.path,
            size=unified_info.size,
            modified_time=unified_info.modified_time.timestamp(),
            hash=unified_info.hash,
            content_type=unified_info.content_type,
            metadata=unified_info.metadata
        )
        
    def to_unified_file_info(self) -> UnifiedFileInfo:
        """Convert to unified FileInfo.
        
        Returns:
            UnifiedFileInfo instance
        """
        return UnifiedFileInfo(
            path=self.path,
            size=self.size,
            hash=self.hash or "",
            modified_time=datetime.fromtimestamp(self.modified_time),
            file_type=get_file_type(self.path),
            content_type=self.content_type or "",
            metadata=self.metadata
        )


class BackupConfig(BaseModel):
    """Configuration for the backup system.
    
    Note: This class is maintained for backward compatibility.
    New code should use common.core.config.UnifiedBackupConfig.
    """
    
    repository_path: Path
    compression_level: int = 6
    deduplication_enabled: bool = True
    max_delta_chain_length: int = 10
    thumbnail_size: Tuple[int, int] = (256, 256)
    max_versions_per_file: Optional[int] = None
    storage_quota: Optional[int] = None
    
    def model_dump(self) -> Dict[str, Any]:
        """Convert to dictionary.
        
        Returns:
            Dictionary representation of this object
        """
        result = {
            "repository_path": str(self.repository_path),
            "compression_level": self.compression_level,
            "deduplication_enabled": self.deduplication_enabled,
            "max_delta_chain_length": self.max_delta_chain_length,
            "thumbnail_size": self.thumbnail_size,
            "max_versions_per_file": self.max_versions_per_file,
            "storage_quota": self.storage_quota
        }
        return result
    
    def dict(self) -> Dict[str, Any]:
        """Convert to dictionary (for backwards compatibility).
        
        Returns:
            Dictionary representation of this object
        """
        return self.model_dump()
        
    def to_unified_config(self) -> UnifiedBackupConfig:
        """Convert to unified backup config.
        
        Returns:
            UnifiedBackupConfig instance
        """
        return UnifiedBackupConfig(
            backup_dir=self.repository_path,
            compression_level=self.compression_level,
            enable_deduplication=self.deduplication_enabled
        )


# File hashing functionality moved to common.core.hashing
# Keeping a compatibility wrapper
def calculate_file_hash(file_path: Path, algorithm: str = 'sha256', buffer_size: int = 65536) -> str:
    """Calculate a hash for a file using the specified algorithm.
    
    Note: This function is deprecated. Use common.core.hashing.calculate_file_hash instead.
    
    Args:
        file_path: Path to the file
        algorithm: Hash algorithm to use (default: sha256)
        buffer_size: Size of the buffer for reading the file
        
    Returns:
        String containing the hexadecimal hash
        
    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the algorithm is not supported
    """
    return core_calculate_file_hash(file_path, algorithm)


# File type detection moved to common.core.file_utils
# Keeping a compatibility wrapper
def detect_file_type(file_path: Path) -> str:
    """Detect the type of a file based on its extension and content.
    
    Note: This function is deprecated. Use common.core.file_utils.get_file_type instead.
    
    Args:
        file_path: Path to the file
        
    Returns:
        String representing the file type (e.g., "image", "model", "project")
        
    Raises:
        FileNotFoundError: If the file does not exist
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_type = get_file_type(file_path)
    
    # Map unified file types to legacy creative types
    type_mapping = {
        FileType.IMAGE: "image",
        FileType.MODEL_3D: "model",
        FileType.PROJECT: "project",
        FileType.TEXT: "text",
        FileType.BINARY: "binary",
        FileType.AUDIO: "audio",
        FileType.VIDEO: "video",
        FileType.DOCUMENT: "document",
        FileType.ARCHIVE: "archive",
        FileType.UNKNOWN: "binary"
    }
    
    # Check for creative-specific types
    extension = file_path.suffix.lower()
    if extension in ['.psd', '.ai', '.indd', '.aep', '.prproj']:
        return "adobe_project"
    elif extension in ['.max', '.mb', '.ma', '.c4d']:
        return "3d_project"
    
    return type_mapping.get(file_type, "binary")


# Directory scanning moved to common.core.file_utils
# Keeping a compatibility wrapper
def scan_directory(directory_path: Path, include_patterns: Optional[List[str]] = None, 
                 exclude_patterns: Optional[List[str]] = None) -> List[FileInfo]:
    """Scan a directory and return information about all files.
    
    Note: This function is deprecated. Use common.core.file_utils.scan_directory instead.
    
    Args:
        directory_path: Path to the directory to scan
        include_patterns: Optional list of glob patterns to include
        exclude_patterns: Optional list of glob patterns to exclude
        
    Returns:
        List of FileInfo objects for all matching files
        
    Raises:
        FileNotFoundError: If the directory does not exist
    """
    if not directory_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory_path}")
    
    result = []
    
    # Use unified scan_directory and convert ignore patterns
    ignore_patterns = exclude_patterns or []
    
    for file_path in unified_scan_directory(directory_path, ignore_patterns=ignore_patterns):
        try:
            # Skip if include patterns specified and file doesn't match
            if include_patterns:
                matches = False
                relative_path = file_path.relative_to(directory_path)
                for pattern in include_patterns:
                    if relative_path.match(pattern):
                        matches = True
                        break
                if not matches:
                    continue
            
            stat = file_path.stat()
            result.append(
                FileInfo(
                    path=file_path.relative_to(directory_path),
                    size=stat.st_size,
                    modified_time=stat.st_mtime,
                    content_type=detect_file_type(file_path)
                )
            )
        except Exception as e:
            # Log error and continue
            print(f"Error processing file {file_path}: {e}")
    
    return result


def create_timestamp() -> str:
    """Create a formatted timestamp for the current time.
    
    Returns:
        String containing the timestamp in the format YYYY-MM-DD_HH-MM-SS
    """
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


def create_unique_id(prefix: str = "") -> str:
    """Create a unique ID string.
    
    Args:
        prefix: Optional prefix to add to the ID
        
    Returns:
        String containing a unique ID
    """
    timestamp = int(time.time() * 1000)
    random_part = np.random.randint(0, 1000000)
    return f"{prefix}{timestamp}_{random_part:06d}"


def save_json(data: Dict[str, Any], file_path: Path) -> None:
    """Save data as a JSON file.
    
    Args:
        data: Dictionary to save
        file_path: Path where the JSON file will be saved
        
    Raises:
        IOError: If the file cannot be written
    """
    # Ensure the parent directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with file_path.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=_json_serializer)


def load_json(file_path: Path) -> Dict[str, Any]:
    """Load data from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dictionary containing the loaded data
        
    Raises:
        FileNotFoundError: If the file does not exist
        json.JSONDecodeError: If the file is not valid JSON
    """
    with file_path.open('r', encoding='utf-8') as f:
        return json.load(f)


def _json_serializer(obj: Any) -> Any:
    """Custom JSON serializer for types that are not JSON serializable by default.
    
    Args:
        obj: Object to serialize
        
    Returns:
        JSON serializable representation of the object
        
    Raises:
        TypeError: If the object cannot be serialized
    """
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")