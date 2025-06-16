"""
File system scanner utilities.

This module provides unified file system traversal and discovery functionality
used by both the Security Auditor and Database Administrator implementations.
"""

import os
import stat
import hashlib
import mimetypes
import subprocess
import platform
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional, Union, Iterator, Tuple, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logger = logging.getLogger(__name__)


class FileSystemScanner:
    """Unified file system traversal and discovery."""
    
    def __init__(self, max_workers: int = 10):
        """Initialize scanner with configuration."""
        self.max_workers = max_workers
    
    def find_files(self, 
                   root_path: Union[str, Path],
                   recursive: bool = True,
                   max_depth: Optional[int] = None,
                   follow_symlinks: bool = False,
                   include_patterns: Optional[List[str]] = None,
                   exclude_patterns: Optional[List[str]] = None,
                   extensions: Optional[Set[str]] = None,
                   min_size: Optional[int] = None,
                   max_size: Optional[int] = None,
                   modified_after: Optional[datetime] = None,
                   modified_before: Optional[datetime] = None,
                   skip_hidden: bool = True,
                   max_files: Optional[int] = None) -> Iterator[Path]:
        """
        Enhanced file discovery with filtering.
        
        Args:
            root_path: Starting directory for search
            recursive: Whether to search recursively
            max_depth: Maximum directory depth to search
            follow_symlinks: Whether to follow symbolic links
            include_patterns: List of glob patterns to include
            exclude_patterns: List of glob patterns to exclude
            extensions: File extensions to include (e.g., {'.ibd', '.myd'})
            min_size: Minimum file size in bytes
            max_size: Maximum file size in bytes
            modified_after: Only include files modified after this datetime
            modified_before: Only include files modified before this datetime
            skip_hidden: Whether to skip hidden files and directories
            max_files: Maximum number of files to return
            
        Returns:
            Iterator of Path objects for matching files
        """
        root = Path(root_path)
        if not root.exists() or not root.is_dir():
            logger.warning(f"Root path {root_path} does not exist or is not a directory")
            return
        
        count = 0
        
        for current_depth, (dirpath, dirnames, filenames) in enumerate(os.walk(root, followlinks=follow_symlinks)):
            # Skip hidden directories if requested
            if skip_hidden:
                dirnames[:] = [d for d in dirnames if not d.startswith('.')]
            
            # Respect max depth if specified
            if max_depth is not None and current_depth >= max_depth:
                dirnames.clear()  # Clear dirnames to prevent further recursion
            
            # Skip further processing if not recursive and not at root
            if not recursive and Path(dirpath) != root:
                continue
            
            # Process files in current directory
            for filename in filenames:
                # Skip hidden files if requested
                if skip_hidden and filename.startswith('.'):
                    continue
                
                file_path = Path(dirpath) / filename
                
                # Check extension filter
                if extensions and file_path.suffix.lower() not in extensions:
                    continue
                
                # Check exclude patterns
                if exclude_patterns:
                    skip_file = False
                    for pattern in exclude_patterns:
                        if file_path.match(pattern):
                            skip_file = True
                            break
                    if skip_file:
                        continue
                
                # Check include patterns
                if include_patterns:
                    include_file = False
                    for pattern in include_patterns:
                        if file_path.match(pattern):
                            include_file = True
                            break
                    if not include_file:
                        continue
                
                try:
                    # Get file stats for further filtering
                    stats = file_path.stat()
                    
                    # Size filters
                    if min_size is not None and stats.st_size < min_size:
                        continue
                    if max_size is not None and stats.st_size > max_size:
                        continue
                    
                    # Date filters
                    mod_time = datetime.fromtimestamp(stats.st_mtime)
                    if modified_after is not None and mod_time < modified_after:
                        continue
                    if modified_before is not None and mod_time > modified_before:
                        continue
                    
                    # Yield the matching file
                    yield file_path
                    
                    # Check if we've reached the max files limit
                    count += 1
                    if max_files is not None and count >= max_files:
                        return
                
                except (PermissionError, OSError) as e:
                    logger.warning(f"Error accessing {file_path}: {e}")
                    continue
    
    def scan_directory(self, path: Union[str, Path]) -> Dict[str, Any]:
        """
        Complete directory analysis with metadata.
        
        Args:
            path: Directory path to scan
            
        Returns:
            Dictionary with directory scan results
        """
        start_time = datetime.now()
        path_obj = Path(path)
        
        if not path_obj.exists() or not path_obj.is_dir():
            return {
                "path": str(path),
                "exists": False,
                "error": "Path does not exist or is not a directory"
            }
        
        try:
            files = list(self.find_files(path))
            total_size = sum(f.stat().st_size for f in files if f.is_file())
            
            result = {
                "path": str(path_obj.absolute()),
                "exists": True,
                "is_directory": True,
                "scan_time": start_time,
                "duration": (datetime.now() - start_time).total_seconds(),
                "file_count": len(files),
                "total_size_bytes": total_size,
                "files": [str(f) for f in files]
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error scanning directory {path}: {e}")
            return {
                "path": str(path),
                "exists": True,
                "error": str(e)
            }
    
    def calculate_directory_size(self, 
                                dir_path: Union[str, Path], 
                                follow_symlinks: bool = False) -> int:
        """
        Calculate the total size of a directory.
        
        Args:
            dir_path: Path to the directory
            follow_symlinks: Whether to follow symbolic links
            
        Returns:
            Total size in bytes
        """
        path = Path(dir_path)
        if not path.exists() or not path.is_dir():
            return 0
        
        try:
            # For small directories, use a simple approach
            files = list(path.glob('**/*'))
            if len(files) < 1000:
                return sum(f.stat().st_size for f in files if f.is_file())
            
            # For larger directories, use parallel processing
            file_paths = [f for f in files if f.is_file()]
            
            def get_file_size(file_path):
                try:
                    return file_path.stat().st_size
                except (PermissionError, OSError):
                    return 0
            
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [executor.submit(get_file_size, file_path) for file_path in file_paths]
                sizes = [future.result() for future in as_completed(futures)]
            
            return sum(sizes)
        
        except (PermissionError, OSError) as e:
            logger.error(f"Error calculating size of {dir_path}: {e}")
            return 0


def get_file_metadata(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Get comprehensive file metadata.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dictionary containing file metadata
    """
    try:
        path = Path(file_path)
        stats = path.stat()
        
        # Get file type using system 'file' command or mimetypes
        try:
            mime_type = subprocess.check_output(
                ["file", "--mime-type", "-b", str(path)], 
                universal_newlines=True
            ).strip()
            file_type = subprocess.check_output(
                ["file", "-b", str(path)], 
                universal_newlines=True
            ).strip()
        except Exception:
            mime_type, _ = mimetypes.guess_type(str(path))
            file_type = mime_type or "unknown"
            mime_type = mime_type or "application/octet-stream"
        
        # Calculate file hash
        hash_sha256 = None
        if path.is_file() and stats.st_size <= 100 * 1024 * 1024:  # Only hash files <= 100MB
            try:
                sha256 = hashlib.sha256()
                with open(path, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b''):
                        sha256.update(chunk)
                hash_sha256 = sha256.hexdigest()
            except Exception as e:
                logger.warning(f"Could not calculate hash for {path}: {e}")
        
        result = {
            "path": str(path.absolute()),
            "file_name": path.name,
            "file_size": stats.st_size,
            "file_type": file_type,
            "mime_type": mime_type,
            "last_modified": datetime.fromtimestamp(stats.st_mtime),
            "creation_time": datetime.fromtimestamp(stats.st_ctime),
            "last_accessed": datetime.fromtimestamp(stats.st_atime),
            "exists": path.exists(),
            "is_file": path.is_file(),
            "is_dir": path.is_dir(),
            "is_symlink": path.is_symlink(),
            "hash_sha256": hash_sha256,
        }
        
        # Add platform-specific information
        if platform.system() == "Windows":
            # Add Windows-specific attributes
            result["is_hidden"] = bool(stats.st_file_attributes & 0x2)  # type: ignore
        elif platform.system() in ["Linux", "Darwin"]:
            # Add Unix-specific attributes
            result["is_executable"] = bool(stats.st_mode & stat.S_IXUSR)
            result["permissions"] = oct(stats.st_mode & 0o777)
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting metadata for {file_path}: {e}")
        return {
            "path": str(file_path),
            "exists": False,
            "error": str(e)
        }


def estimate_file_growth_rate(file_path: Union[str, Path],
                             historical_sizes: List[Tuple[datetime, int]]) -> float:
    """
    Estimate the growth rate of a file based on historical size measurements.
    
    Args:
        file_path: Path to the file
        historical_sizes: List of (datetime, size_bytes) tuples representing historical measurements
        
    Returns:
        Estimated growth rate in bytes per day
    """
    if not historical_sizes or len(historical_sizes) < 2:
        return 0.0
    
    # Sort by datetime
    sorted_sizes = sorted(historical_sizes, key=lambda x: x[0])
    
    # Calculate deltas
    deltas = []
    for i in range(1, len(sorted_sizes)):
        time_diff = (sorted_sizes[i][0] - sorted_sizes[i-1][0]).total_seconds() / 86400  # Convert to days
        if time_diff <= 0:
            continue
        
        size_diff = sorted_sizes[i][1] - sorted_sizes[i-1][1]
        growth_rate = size_diff / time_diff
        deltas.append(growth_rate)
    
    # Return average growth rate if we have data, otherwise 0
    return sum(deltas) / len(deltas) if deltas else 0.0