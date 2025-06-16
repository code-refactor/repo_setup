"""
File utilities for the unified backup system.
"""

import mimetypes
import os
from datetime import datetime
from pathlib import Path
from typing import Iterator, List, Optional, Set, Union

from .exceptions import BackupSystemError
from .hashing import calculate_file_hash
from .models import FileInfo, FileType, FILE_TYPE_MAPPINGS


def scan_directory(
    directory: Union[str, Path],
    ignore_patterns: Optional[List[str]] = None,
    follow_symlinks: bool = False,
    include_hidden: bool = False
) -> Iterator[Path]:
    """
    Recursively scan directory for files.
    
    Args:
        directory: Directory to scan
        ignore_patterns: List of glob patterns to ignore
        follow_symlinks: Whether to follow symbolic links
        include_hidden: Whether to include hidden files/directories
        
    Yields:
        Path objects for each file found
    """
    directory = Path(directory)
    if not directory.exists() or not directory.is_dir():
        return
        
    ignore_patterns = ignore_patterns or []
    
    try:
        for root, dirs, files in os.walk(directory, followlinks=follow_symlinks):
            root_path = Path(root)
            
            # Filter hidden directories if not including them
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
            # Apply ignore patterns to directories
            for pattern in ignore_patterns:
                dirs[:] = [d for d in dirs if not Path(d).match(pattern)]
                
            for file in files:
                # Skip hidden files if not including them
                if not include_hidden and file.startswith('.'):
                    continue
                    
                file_path = root_path / file
                
                # Apply ignore patterns to files
                should_ignore = False
                for pattern in ignore_patterns:
                    if file_path.match(pattern) or file_path.name.match(pattern):
                        should_ignore = True
                        break
                        
                if not should_ignore:
                    yield file_path
                    
    except (OSError, PermissionError) as e:
        # Log error but continue scanning
        pass


def get_file_type(file_path: Union[str, Path]) -> FileType:
    """
    Determine file type based on extension and content.
    
    Args:
        file_path: Path to the file
        
    Returns:
        FileType enum value
    """
    file_path = Path(file_path)
    extension = file_path.suffix.lower()
    
    # Check extension mapping first
    if extension in FILE_TYPE_MAPPINGS:
        return FILE_TYPE_MAPPINGS[extension]
        
    # Use MIME type as fallback
    mime_type, _ = mimetypes.guess_type(str(file_path))
    if mime_type:
        if mime_type.startswith('image/'):
            return FileType.IMAGE
        elif mime_type.startswith('audio/'):
            return FileType.AUDIO
        elif mime_type.startswith('video/'):
            return FileType.VIDEO
        elif mime_type.startswith('text/'):
            return FileType.TEXT
        elif mime_type in ['application/pdf', 'application/msword']:
            return FileType.DOCUMENT
        elif mime_type in ['application/zip', 'application/x-rar']:
            return FileType.ARCHIVE
            
    return FileType.UNKNOWN


def is_binary_file(file_path: Union[str, Path], sample_size: int = 8192) -> bool:
    """
    Determine if a file is binary by sampling its content.
    
    Args:
        file_path: Path to the file
        sample_size: Number of bytes to sample
        
    Returns:
        True if file appears to be binary
    """
    file_path = Path(file_path)
    
    # Check extension first
    extension = file_path.suffix.lower()
    if extension in {'.exe', '.dll', '.so', '.dylib', '.bin', '.dat', '.pak', '.wad', '.zip', '.rar', '.7z'}:
        return True
        
    if extension in {'.txt', '.py', '.js', '.css', '.html', '.xml', '.json', '.yaml', '.yml', '.md', '.rst'}:
        return False
        
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(sample_size)
            
        # Check for null bytes (common in binary files)
        if b'\x00' in chunk:
            return True
            
        # Check for high ratio of non-printable characters
        printable_chars = sum(1 for b in chunk if 32 <= b <= 126 or b in (9, 10, 13))
        if len(chunk) > 0 and printable_chars / len(chunk) < 0.7:
            return True
            
        return False
        
    except (OSError, PermissionError):
        return True  # Assume binary if can't read


def get_file_info(file_path: Union[str, Path], hash_algorithm: str = "sha256") -> FileInfo:
    """
    Get comprehensive file information.
    
    Args:
        file_path: Path to the file
        hash_algorithm: Hash algorithm to use
        
    Returns:
        FileInfo object with complete metadata
        
    Raises:
        BackupSystemError: If file cannot be accessed
    """
    file_path = Path(file_path)
    
    try:
        stat = file_path.stat()
        file_hash = calculate_file_hash(file_path, hash_algorithm)
        file_type = get_file_type(file_path)
        
        # Get MIME type
        content_type, _ = mimetypes.guess_type(str(file_path))
        if not content_type:
            content_type = "application/octet-stream"
            
        return FileInfo(
            path=file_path,
            size=stat.st_size,
            hash=file_hash,
            modified_time=datetime.fromtimestamp(stat.st_mtime),
            file_type=file_type,
            content_type=content_type
        )
        
    except Exception as e:
        raise BackupSystemError(f"Failed to get file info for {file_path}: {e}")


def compare_files(file1: Union[str, Path], file2: Union[str, Path]) -> bool:
    """
    Compare two files for equality using size and hash.
    
    Args:
        file1: First file path
        file2: Second file path
        
    Returns:
        True if files are identical
    """
    file1 = Path(file1)
    file2 = Path(file2)
    
    if not (file1.exists() and file2.exists()):
        return False
        
    # Quick size check first
    if file1.stat().st_size != file2.stat().st_size:
        return False
        
    # Hash comparison
    try:
        hash1 = calculate_file_hash(file1)
        hash2 = calculate_file_hash(file2)
        return hash1 == hash2
    except Exception:
        return False


def ensure_directory(directory: Union[str, Path]) -> Path:
    """
    Ensure directory exists, creating it if necessary.
    
    Args:
        directory: Directory path
        
    Returns:
        Path object for the directory
        
    Raises:
        BackupSystemError: If directory cannot be created
    """
    directory = Path(directory)
    
    try:
        directory.mkdir(parents=True, exist_ok=True)
        return directory
    except Exception as e:
        raise BackupSystemError(f"Failed to create directory {directory}: {e}")


def safe_file_copy(src: Union[str, Path], dst: Union[str, Path], preserve_metadata: bool = True) -> None:
    """
    Safely copy a file with atomic operation.
    
    Args:
        src: Source file path
        dst: Destination file path
        preserve_metadata: Whether to preserve file metadata
        
    Raises:
        BackupSystemError: If copy fails
    """
    src = Path(src)
    dst = Path(dst)
    
    if not src.exists():
        raise BackupSystemError(f"Source file does not exist: {src}")
        
    # Ensure destination directory exists
    ensure_directory(dst.parent)
    
    # Use temporary file for atomic operation
    temp_dst = dst.with_suffix(dst.suffix + '.tmp')
    
    try:
        # Copy file content
        with open(src, 'rb') as src_file, open(temp_dst, 'wb') as dst_file:
            while chunk := src_file.read(8192):
                dst_file.write(chunk)
                
        # Preserve metadata if requested
        if preserve_metadata:
            src_stat = src.stat()
            os.utime(temp_dst, (src_stat.st_atime, src_stat.st_mtime))
            
        # Atomic move to final destination
        temp_dst.replace(dst)
        
    except Exception as e:
        # Clean up temporary file on error
        if temp_dst.exists():
            temp_dst.unlink()
        raise BackupSystemError(f"Failed to copy {src} to {dst}: {e}")


def get_directory_size(directory: Union[str, Path]) -> int:
    """
    Calculate total size of all files in directory.
    
    Args:
        directory: Directory path
        
    Returns:
        Total size in bytes
    """
    total_size = 0
    
    for file_path in scan_directory(directory):
        try:
            total_size += file_path.stat().st_size
        except (OSError, PermissionError):
            continue
            
    return total_size


def normalize_path(path: Union[str, Path], base_path: Optional[Union[str, Path]] = None) -> Path:
    """
    Normalize path for consistent storage and comparison.
    
    Args:
        path: Path to normalize
        base_path: Base path to make relative to
        
    Returns:
        Normalized Path object
    """
    path = Path(path).resolve()
    
    if base_path:
        base_path = Path(base_path).resolve()
        try:
            return path.relative_to(base_path)
        except ValueError:
            # Path is not relative to base_path
            pass
            
    return path


def is_ignored_file(file_path: Union[str, Path], ignore_patterns: List[str]) -> bool:
    """
    Check if file should be ignored based on patterns.
    
    Args:
        file_path: File path to check
        ignore_patterns: List of glob patterns
        
    Returns:
        True if file should be ignored
    """
    file_path = Path(file_path)
    
    for pattern in ignore_patterns:
        if file_path.match(pattern) or file_path.name.match(pattern):
            return True
            
    return False


def get_unique_filename(file_path: Union[str, Path]) -> Path:
    """
    Generate unique filename if original already exists.
    
    Args:
        file_path: Desired file path
        
    Returns:
        Unique file path
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        return file_path
        
    counter = 1
    stem = file_path.stem
    suffix = file_path.suffix
    parent = file_path.parent
    
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name
        
        if not new_path.exists():
            return new_path
            
        counter += 1