"""
Compression utilities for the unified backup system.
"""

import zlib
from typing import Tuple, Optional

try:
    import zstandard as zstd
    HAS_ZSTD = True
except ImportError:
    HAS_ZSTD = False

try:
    import bsdiff4
    HAS_BSDIFF = True
except ImportError:
    HAS_BSDIFF = False

from .exceptions import CompressionError


def compress_data(data: bytes, algorithm: str = "zstd", level: int = 3) -> bytes:
    """
    Compress data using specified algorithm.
    
    Args:
        data: Data to compress
        algorithm: Compression algorithm ('zstd', 'zlib', 'none')
        level: Compression level (0-22 for zstd, 0-9 for zlib)
        
    Returns:
        Compressed data
        
    Raises:
        CompressionError: If compression fails
    """
    try:
        if algorithm == "none":
            return data
        elif algorithm == "zstd":
            if not HAS_ZSTD:
                # Fallback to zlib if zstd not available
                return zlib.compress(data, level=min(level, 9))
            
            compressor = zstd.ZstdCompressor(level=level)
            return compressor.compress(data)
        elif algorithm == "zlib":
            return zlib.compress(data, level=min(level, 9))
        else:
            raise CompressionError(f"Unsupported compression algorithm: {algorithm}")
            
    except Exception as e:
        raise CompressionError(f"Compression failed: {e}")


def decompress_data(data: bytes, algorithm: str = "zstd") -> bytes:
    """
    Decompress data using specified algorithm.
    
    Args:
        data: Compressed data
        algorithm: Compression algorithm used
        
    Returns:
        Decompressed data
        
    Raises:
        CompressionError: If decompression fails
    """
    try:
        if algorithm == "none":
            return data
        elif algorithm == "zstd":
            if not HAS_ZSTD:
                # Try zlib fallback
                return zlib.decompress(data)
            
            decompressor = zstd.ZstdDecompressor()
            return decompressor.decompress(data)
        elif algorithm == "zlib":
            return zlib.decompress(data)
        else:
            raise CompressionError(f"Unsupported compression algorithm: {algorithm}")
            
    except Exception as e:
        raise CompressionError(f"Decompression failed: {e}")


def get_compression_ratio(original_size: int, compressed_size: int) -> float:
    """
    Calculate compression ratio.
    
    Args:
        original_size: Size of original data
        compressed_size: Size of compressed data
        
    Returns:
        Compression ratio (compressed_size / original_size)
    """
    if original_size == 0:
        return 1.0
    return compressed_size / original_size


def should_compress(data: bytes, algorithm: str = "zstd", level: int = 3, threshold: float = 0.9) -> bool:
    """
    Determine if data should be compressed based on potential savings.
    
    Args:
        data: Data to test
        algorithm: Compression algorithm to test
        level: Compression level to test
        threshold: Minimum compression ratio to justify compression
        
    Returns:
        True if compression is beneficial
    """
    if len(data) < 1024:  # Don't compress very small data
        return False
        
    try:
        # Test compression on first 4KB to estimate ratio
        test_data = data[:4096]
        compressed = compress_data(test_data, algorithm, level)
        ratio = get_compression_ratio(len(test_data), len(compressed))
        return ratio < threshold
    except Exception:
        return False


class DeltaCompressor:
    """Binary delta compression using bsdiff algorithm."""
    
    def __init__(self, threshold: float = 0.3):
        """
        Initialize delta compressor.
        
        Args:
            threshold: Minimum size reduction ratio to use delta compression
        """
        self.threshold = threshold
        
    def create_delta(self, old_data: bytes, new_data: bytes) -> Optional[bytes]:
        """
        Create binary delta between old and new data.
        
        Args:
            old_data: Original data
            new_data: Modified data
            
        Returns:
            Delta data if beneficial, None otherwise
        """
        if not HAS_BSDIFF:
            return None
            
        try:
            delta = bsdiff4.diff(old_data, new_data)
            
            # Only use delta if it provides significant savings
            if len(delta) < len(new_data) * self.threshold:
                return delta
            else:
                return None
                
        except Exception:
            return None
            
    def apply_delta(self, old_data: bytes, delta: bytes) -> bytes:
        """
        Apply binary delta to reconstruct new data.
        
        Args:
            old_data: Original data
            delta: Delta data
            
        Returns:
            Reconstructed data
            
        Raises:
            CompressionError: If delta application fails
        """
        if not HAS_BSDIFF:
            raise CompressionError("bsdiff4 library not available")
            
        try:
            return bsdiff4.patch(old_data, delta)
        except Exception as e:
            raise CompressionError(f"Failed to apply delta: {e}")
            

def compress_with_fallback(data: bytes, preferred_algorithm: str = "zstd", fallback_algorithm: str = "zlib", level: int = 3) -> Tuple[bytes, str]:
    """
    Compress data with fallback to alternative algorithm.
    
    Args:
        data: Data to compress
        preferred_algorithm: Preferred compression algorithm
        fallback_algorithm: Fallback compression algorithm
        level: Compression level
        
    Returns:
        Tuple of (compressed_data, algorithm_used)
        
    Raises:
        CompressionError: If all compression attempts fail
    """
    try:
        compressed = compress_data(data, preferred_algorithm, level)
        return compressed, preferred_algorithm
    except CompressionError:
        try:
            compressed = compress_data(data, fallback_algorithm, level)
            return compressed, fallback_algorithm
        except CompressionError:
            # Last resort: return uncompressed
            return data, "none"


def estimate_compression_savings(data: bytes, algorithm: str = "zstd", level: int = 3) -> Tuple[float, int]:
    """
    Estimate compression savings without full compression.
    
    Args:
        data: Data to estimate
        algorithm: Compression algorithm
        level: Compression level
        
    Returns:
        Tuple of (compression_ratio, estimated_compressed_size)
    """
    if len(data) == 0:
        return 1.0, 0
        
    # Sample compression on representative portion
    sample_size = min(len(data), 8192)
    sample_data = data[:sample_size]
    
    try:
        compressed_sample = compress_data(sample_data, algorithm, level)
        sample_ratio = get_compression_ratio(len(sample_data), len(compressed_sample))
        estimated_size = int(len(data) * sample_ratio)
        return sample_ratio, estimated_size
    except Exception:
        return 1.0, len(data)