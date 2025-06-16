"""File system utility functions for the Database Storage Optimization Analyzer."""

import logging
from typing import Dict, List, Optional, Set, Tuple, Iterator, Union
from pathlib import Path
from datetime import datetime
from functools import lru_cache

# Import common library functions
from common.core.filesystem import FileSystemScanner, get_file_metadata, estimate_file_growth_rate as common_estimate_file_growth_rate

logger = logging.getLogger(__name__)

# Create a shared scanner instance
_scanner = FileSystemScanner()

# Re-export common functions with compatible interfaces
def get_file_stats(file_path: Union[str, Path]) -> Dict[str, Union[int, datetime, bool]]:
    """
    Get detailed file statistics using common library.

    Args:
        file_path: Path to the file

    Returns:
        Dict containing file statistics including size, modification times, etc.
    """
    metadata = get_file_metadata(file_path)
    
    # Handle error case (file doesn't exist)
    if "error" in metadata:
        return {
            "path": metadata["path"],
            "exists": metadata["exists"],
            "error": metadata["error"]
        }
    
    # Convert to expected format for backward compatibility
    result = {
        "path": metadata["path"],
        "size_bytes": metadata["file_size"],
        "last_modified": metadata["last_modified"],
        "creation_time": metadata.get("creation_time"),
        "last_accessed": metadata.get("last_accessed"),
        "exists": metadata["exists"],
        "is_file": metadata["is_file"],
        "is_dir": metadata["is_dir"],
        "is_symlink": metadata["is_symlink"],
    }
    
    # Add platform-specific fields if available
    if "is_executable" in metadata:
        result["is_executable"] = metadata["is_executable"]
    if "permissions" in metadata:
        result["permissions"] = metadata["permissions"]
    if "is_hidden" in metadata:
        result["is_hidden"] = metadata["is_hidden"]
        
    return result


def find_files(
    root_path: Union[str, Path],
    extensions: Optional[Set[str]] = None,
    min_size: Optional[int] = None,
    max_size: Optional[int] = None,
    modified_after: Optional[datetime] = None,
    modified_before: Optional[datetime] = None,
    max_depth: Optional[int] = None,
    follow_symlinks: bool = False,
    skip_hidden: bool = True,
    recursive: bool = True,
    max_files: Optional[int] = None,
) -> Iterator[Path]:
    """
    Find files matching specified criteria using common library.

    Args:
        root_path: Starting directory for search
        extensions: File extensions to include (e.g., {'.ibd', '.myd'})
        min_size: Minimum file size in bytes
        max_size: Maximum file size in bytes
        modified_after: Only include files modified after this datetime
        modified_before: Only include files modified before this datetime
        max_depth: Maximum directory depth to search
        follow_symlinks: Whether to follow symbolic links
        skip_hidden: Whether to skip hidden files and directories
        recursive: Whether to search recursively
        max_files: Maximum number of files to return

    Returns:
        Iterator of Path objects for matching files
    """
    return _scanner.find_files(
        root_path=root_path,
        recursive=recursive,
        max_depth=max_depth,
        follow_symlinks=follow_symlinks,
        extensions=extensions,
        min_size=min_size,
        max_size=max_size,
        modified_after=modified_after,
        modified_before=modified_before,
        skip_hidden=skip_hidden,
        max_files=max_files
    )


def calculate_dir_size(
    dir_path: Union[str, Path], 
    follow_symlinks: bool = False,
    max_workers: int = 10
) -> int:
    """
    Calculate the total size of a directory using common library.

    Args:
        dir_path: Path to the directory
        follow_symlinks: Whether to follow symbolic links
        max_workers: Maximum number of worker threads

    Returns:
        Total size in bytes
    """
    return _scanner.calculate_directory_size(dir_path, follow_symlinks)


@lru_cache(maxsize=128)
def get_disk_usage(path: Union[str, Path]) -> Dict[str, Union[int, float]]:
    """
    Get disk usage statistics for the partition containing the path.

    Args:
        path: Path to check

    Returns:
        Dictionary with disk usage information
    """
    try:
        import psutil
        usage = psutil.disk_usage(str(path))
        return {
            "total_bytes": usage.total,
            "used_bytes": usage.used,
            "free_bytes": usage.free,
            "percent_used": usage.percent,
        }
    except Exception as e:
        logger.error(f"Error getting disk usage for {path}: {e}")
        return {
            "error": str(e)
        }


def estimate_file_growth_rate(
    file_path: Union[str, Path],
    historical_sizes: List[Tuple[datetime, int]]
) -> float:
    """
    Estimate the growth rate of a file based on historical size measurements.

    Args:
        file_path: Path to the file
        historical_sizes: List of (datetime, size_bytes) tuples representing historical measurements

    Returns:
        Estimated growth rate in bytes per day
    """
    return common_estimate_file_growth_rate(file_path, historical_sizes)