"""
Hash calculation utilities for the unified backup system.
"""

import hashlib
from pathlib import Path
from typing import Union, BinaryIO

try:
    import xxhash
    HAS_XXHASH = True
except ImportError:
    HAS_XXHASH = False

from .exceptions import HashError


def calculate_file_hash(file_path: Union[str, Path], algorithm: str = "sha256", chunk_size: int = 8192) -> str:
    """
    Calculate hash of a file using specified algorithm.
    
    Args:
        file_path: Path to the file
        algorithm: Hash algorithm to use ('sha256', 'sha1', 'md5', 'xxhash64')
        chunk_size: Size of chunks to read at a time
        
    Returns:
        Hexadecimal hash string
        
    Raises:
        HashError: If hashing fails
    """
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            raise HashError(f"File not found: {file_path}")
            
        if algorithm == "xxhash64":
            if not HAS_XXHASH:
                raise HashError("xxhash library not available, falling back to sha256")
            hasher = xxhash.xxh64()
        else:
            hasher = hashlib.new(algorithm)
            
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
                
        return hasher.hexdigest()
        
    except Exception as e:
        raise HashError(f"Failed to calculate hash for {file_path}: {e}")


def calculate_data_hash(data: bytes, algorithm: str = "sha256") -> str:
    """
    Calculate hash of data bytes using specified algorithm.
    
    Args:
        data: Data to hash
        algorithm: Hash algorithm to use
        
    Returns:
        Hexadecimal hash string
        
    Raises:
        HashError: If hashing fails
    """
    try:
        if algorithm == "xxhash64":
            if not HAS_XXHASH:
                raise HashError("xxhash library not available, falling back to sha256")
            hasher = xxhash.xxh64()
        else:
            hasher = hashlib.new(algorithm)
            
        hasher.update(data)
        return hasher.hexdigest()
        
    except Exception as e:
        raise HashError(f"Failed to calculate hash for data: {e}")


def calculate_stream_hash(stream: BinaryIO, algorithm: str = "sha256", chunk_size: int = 8192) -> str:
    """
    Calculate hash of a binary stream.
    
    Args:
        stream: Binary stream to hash
        algorithm: Hash algorithm to use
        chunk_size: Size of chunks to read at a time
        
    Returns:
        Hexadecimal hash string
        
    Raises:
        HashError: If hashing fails
    """
    try:
        if algorithm == "xxhash64":
            if not HAS_XXHASH:
                raise HashError("xxhash library not available, falling back to sha256")
            hasher = xxhash.xxh64()
        else:
            hasher = hashlib.new(algorithm)
            
        while chunk := stream.read(chunk_size):
            hasher.update(chunk)
            
        return hasher.hexdigest()
        
    except Exception as e:
        raise HashError(f"Failed to calculate hash for stream: {e}")


def verify_file_hash(file_path: Union[str, Path], expected_hash: str, algorithm: str = "sha256") -> bool:
    """
    Verify that a file matches the expected hash.
    
    Args:
        file_path: Path to the file
        expected_hash: Expected hash value
        algorithm: Hash algorithm to use
        
    Returns:
        True if hash matches, False otherwise
    """
    try:
        actual_hash = calculate_file_hash(file_path, algorithm)
        return actual_hash.lower() == expected_hash.lower()
    except Exception:
        return False


def get_rolling_hash(data: bytes, window_size: int = 64, polynomial: int = 0x3DA3358B4DC173) -> int:
    """
    Calculate rolling hash for content-defined chunking.
    
    Args:
        data: Data to hash
        window_size: Size of rolling window
        polynomial: Polynomial for hash calculation
        
    Returns:
        Rolling hash value
    """
    if len(data) < window_size:
        return 0
        
    hash_value = 0
    for i in range(window_size):
        hash_value = ((hash_value << 1) + data[i]) & 0xFFFFFFFFFFFFFFFF
        
    return hash_value


class RollingHasher:
    """Rolling hash calculator for efficient content-defined chunking."""
    
    def __init__(self, window_size: int = 64, polynomial: int = 0x3DA3358B4DC173):
        self.window_size = window_size
        self.polynomial = polynomial
        self.window = bytearray(window_size)
        self.window_pos = 0
        self.hash_value = 0
        self.initialized = False
        
    def update(self, byte: int) -> int:
        """
        Update rolling hash with new byte.
        
        Args:
            byte: New byte to add
            
        Returns:
            Current hash value
        """
        if not self.initialized:
            self.window[self.window_pos] = byte
            self.hash_value = ((self.hash_value << 1) + byte) & 0xFFFFFFFFFFFFFFFF
            self.window_pos = (self.window_pos + 1) % self.window_size
            
            if self.window_pos == 0:
                self.initialized = True
        else:
            # Remove old byte and add new byte
            old_byte = self.window[self.window_pos]
            self.window[self.window_pos] = byte
            
            # Update hash: remove old byte contribution and add new byte
            self.hash_value = ((self.hash_value << 1) - (old_byte << self.window_size) + byte) & 0xFFFFFFFFFFFFFFFF
            self.window_pos = (self.window_pos + 1) % self.window_size
            
        return self.hash_value
        
    def reset(self):
        """Reset the rolling hasher to initial state."""
        self.window = bytearray(self.window_size)
        self.window_pos = 0
        self.hash_value = 0
        self.initialized = False