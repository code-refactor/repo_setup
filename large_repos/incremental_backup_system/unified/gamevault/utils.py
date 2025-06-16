"""
Utility functions for GameVault.

This module contains game-specific utility functions extending common utilities.
"""

import hashlib
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Generator, List, Optional, Set, Tuple, Union

import xxhash
from pyzstd import compress, decompress

# Import common utilities
from common.core.file_utils import (
    scan_directory as common_scan_directory,
    get_file_info,
    is_binary_file as common_is_binary_file,
    compare_files,
    ensure_directory,
    safe_file_copy,
    get_directory_size,
    normalize_path,
    is_ignored_file,
    get_unique_filename
)
from common.core.hashing import calculate_file_hash
from common.core.compression import compress_data as common_compress_data, decompress_data as common_decompress_data


def get_file_hash(file_path: Union[str, Path], chunk_size: int = 8192) -> str:
    """
    Calculate the SHA-256 hash of a file.
    
    Args:
        file_path: Path to the file
        chunk_size: Size of chunks to read from the file (kept for backward compatibility)
        
    Returns:
        str: Hexadecimal digest of the file hash
    """
    # Use common implementation for consistency
    return calculate_file_hash(file_path, algorithm="sha256")


def get_file_xxhash(file_path: Union[str, Path], chunk_size: int = 8192) -> str:
    """
    Calculate a faster xxHash64 hash of a file.
    
    Args:
        file_path: Path to the file
        chunk_size: Size of chunks to read from the file (kept for backward compatibility)
        
    Returns:
        str: Hexadecimal digest of the file hash
    """
    # Use common implementation with xxhash algorithm
    return calculate_file_hash(file_path, algorithm="xxhash")


def compress_data(data: bytes, level: int = 3) -> bytes:
    """
    Compress binary data using zstd.
    
    Args:
        data: Binary data to compress
        level: Compression level (0-22)
        
    Returns:
        bytes: Compressed data
    """
    # Use common implementation for consistency
    return common_compress_data(data, level)


def decompress_data(compressed_data: bytes) -> bytes:
    """
    Decompress binary data using zstd.
    
    Args:
        compressed_data: Compressed binary data
        
    Returns:
        bytes: Decompressed data
    """
    # Use common implementation for consistency
    return common_decompress_data(compressed_data)


def get_file_modification_time(file_path: Union[str, Path]) -> float:
    """
    Get the modification time of a file as a Unix timestamp.
    
    Args:
        file_path: Path to the file
        
    Returns:
        float: Modification time as a Unix timestamp
    """
    return os.path.getmtime(file_path)


def get_file_size(file_path: Union[str, Path]) -> int:
    """
    Get the size of a file in bytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        int: Size of the file in bytes
    """
    return os.path.getsize(file_path)


def format_timestamp(timestamp: float) -> str:
    """
    Format a Unix timestamp as a human-readable string.
    
    Args:
        timestamp: Unix timestamp
        
    Returns:
        str: Formatted timestamp
    """
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def generate_timestamp() -> float:
    """
    Generate a current timestamp.
    
    Returns:
        float: Current Unix timestamp
    """
    return time.time()


def is_binary_file(file_path: Union[str, Path], binary_extensions: Optional[Set[str]] = None) -> bool:
    """
    Check if a file is binary based on its extension and content.
    
    Args:
        file_path: Path to the file
        binary_extensions: Set of binary file extensions (kept for backward compatibility)
        
    Returns:
        bool: True if the file is binary, False otherwise
    """
    if binary_extensions is not None:
        # Legacy mode - use extension-only check for backward compatibility
        file_path = Path(file_path)
        return file_path.suffix.lower() in binary_extensions
    else:
        # Use common implementation which checks both extension and content
        return common_is_binary_file(file_path)


def scan_directory(
    directory: Union[str, Path], 
    ignore_patterns: Optional[List[str]] = None
) -> Generator[Path, None, None]:
    """
    Scan a directory recursively for files, ignoring specified patterns.
    
    Args:
        directory: Directory to scan
        ignore_patterns: List of glob patterns to ignore
        
    Yields:
        Path: Path to each file found
    """
    if ignore_patterns is None:
        from gamevault.config import get_config
        ignore_patterns = get_config().ignore_patterns
    
    # Use common implementation but maintain backward compatibility
    for file_path in common_scan_directory(
        directory=directory,
        ignore_patterns=ignore_patterns,
        follow_symlinks=False,
        include_hidden=False
    ):
        yield file_path