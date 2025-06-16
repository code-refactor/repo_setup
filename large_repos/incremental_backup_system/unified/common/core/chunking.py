"""
File chunking strategies for the unified backup system.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Union, Iterator, Tuple

from .exceptions import ChunkingError
from .hashing import RollingHasher, calculate_data_hash
from .models import ChunkInfo, ChunkingConfig


class ChunkingStrategy(ABC):
    """Abstract base class for file chunking strategies."""
    
    @abstractmethod
    def chunk_file(self, file_path: Union[str, Path]) -> List[ChunkInfo]:
        """
        Split file into chunks.
        
        Args:
            file_path: Path to file to chunk
            
        Returns:
            List of ChunkInfo objects
        """
        pass
        
    @abstractmethod
    def chunk_data(self, data: bytes) -> List[ChunkInfo]:
        """
        Split data into chunks.
        
        Args:
            data: Data to chunk
            
        Returns:
            List of ChunkInfo objects
        """
        pass


class FixedSizeChunker(ChunkingStrategy):
    """Fixed-size chunking strategy."""
    
    def __init__(self, chunk_size: int = 64 * 1024):
        """
        Initialize fixed-size chunker.
        
        Args:
            chunk_size: Size of each chunk in bytes
        """
        self.chunk_size = chunk_size
        
    def chunk_file(self, file_path: Union[str, Path]) -> List[ChunkInfo]:
        """Split file into fixed-size chunks."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise ChunkingError(f"File not found: {file_path}")
            
        chunks = []
        offset = 0
        
        try:
            with open(file_path, 'rb') as f:
                while True:
                    chunk_data = f.read(self.chunk_size)
                    if not chunk_data:
                        break
                        
                    chunk_hash = calculate_data_hash(chunk_data)
                    chunks.append(ChunkInfo(
                        hash=chunk_hash,
                        size=len(chunk_data),
                        offset=offset
                    ))
                    
                    offset += len(chunk_data)
                    
        except Exception as e:
            raise ChunkingError(f"Failed to chunk file {file_path}: {e}")
            
        return chunks
        
    def chunk_data(self, data: bytes) -> List[ChunkInfo]:
        """Split data into fixed-size chunks."""
        if len(data) == 0:
            return []
            
        chunks = []
        offset = 0
        
        while offset < len(data):
            chunk_end = min(offset + self.chunk_size, len(data))
            chunk_data = data[offset:chunk_end]
            
            chunk_hash = calculate_data_hash(chunk_data)
            chunks.append(ChunkInfo(
                hash=chunk_hash,
                size=len(chunk_data),
                offset=offset
            ))
            
            offset = chunk_end
            
        return chunks


class RollingHashChunker(ChunkingStrategy):
    """Content-defined chunking using rolling hash."""
    
    def __init__(self, config: ChunkingConfig):
        """
        Initialize rolling hash chunker.
        
        Args:
            config: Chunking configuration
        """
        self.config = config
        self.window_size = config.window_size
        self.chunk_size_min = config.chunk_size_min
        self.chunk_size_max = config.chunk_size_max
        self.boundary_mask = config.boundary_mask
        self.polynomial = config.polynomial
        
    def chunk_file(self, file_path: Union[str, Path]) -> List[ChunkInfo]:
        """Split file using content-defined chunking."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise ChunkingError(f"File not found: {file_path}")
            
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            return self.chunk_data(data)
            
        except Exception as e:
            raise ChunkingError(f"Failed to chunk file {file_path}: {e}")
            
    def chunk_data(self, data: bytes) -> List[ChunkInfo]:
        """Split data using content-defined chunking."""
        if len(data) == 0:
            return []
            
        if len(data) <= self.chunk_size_min:
            # File too small for chunking
            chunk_hash = calculate_data_hash(data)
            return [ChunkInfo(hash=chunk_hash, size=len(data), offset=0)]
            
        chunks = []
        chunk_start = 0
        
        for boundary in self._find_boundaries(data):
            chunk_data = data[chunk_start:boundary]
            chunk_hash = calculate_data_hash(chunk_data)
            
            chunks.append(ChunkInfo(
                hash=chunk_hash,
                size=len(chunk_data),
                offset=chunk_start
            ))
            
            chunk_start = boundary
            
        # Handle remaining data
        if chunk_start < len(data):
            remaining_data = data[chunk_start:]
            
            # If remaining data is too small and we have previous chunks,
            # merge it with the last chunk to maintain minimum size
            if len(remaining_data) < self.chunk_size_min and chunks:
                # Merge with last chunk
                last_chunk = chunks.pop()
                merged_data = data[last_chunk.offset:chunk_start] + remaining_data
                merged_hash = calculate_data_hash(merged_data)
                
                chunks.append(ChunkInfo(
                    hash=merged_hash,
                    size=len(merged_data),
                    offset=last_chunk.offset
                ))
            else:
                # Add as separate chunk
                chunk_hash = calculate_data_hash(remaining_data)
                chunks.append(ChunkInfo(
                    hash=chunk_hash,
                    size=len(remaining_data),
                    offset=chunk_start
                ))
            
        return chunks
        
    def _find_boundaries(self, data: bytes) -> Iterator[int]:
        """Find chunk boundaries using rolling hash."""
        if len(data) <= self.chunk_size_min:
            return
            
        hasher = RollingHasher(self.window_size, self.polynomial)
        
        # Initialize window
        for i in range(min(self.window_size, len(data))):
            hasher.update(data[i])
            
        last_boundary = 0
        
        for i in range(self.window_size, len(data)):
            hash_value = hasher.update(data[i])
            chunk_size = i - last_boundary
            
            # Check for boundary conditions - ensure we meet minimum chunk size first
            if chunk_size >= self.chunk_size_min:
                if (hash_value & self.boundary_mask) == 0:
                    yield i + 1  # Include the boundary byte in the chunk
                    last_boundary = i + 1
                elif chunk_size >= self.chunk_size_max:
                    yield i + 1
                    last_boundary = i + 1


class GameAssetChunker(ChunkingStrategy):
    """Specialized chunker for game assets with format-aware boundaries."""
    
    def __init__(self, config: ChunkingConfig):
        """
        Initialize game asset chunker.
        
        Args:
            config: Chunking configuration
        """
        self.config = config
        self.rolling_chunker = RollingHashChunker(config)
        self.fixed_chunker = FixedSizeChunker(config.chunk_size_max)
        
    def chunk_file(self, file_path: Union[str, Path]) -> List[ChunkInfo]:
        """Split file using asset-aware chunking."""
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        # Use specialized chunking for known formats
        if extension in {'.png', '.jpg', '.jpeg'}:
            return self._chunk_image_file(file_path)
        elif extension in {'.wav', '.ogg'}:
            return self._chunk_audio_file(file_path)
        elif extension in {'.fbx', '.obj'}:
            return self._chunk_model_file(file_path)
        else:
            # Use rolling hash for other files
            return self.rolling_chunker.chunk_file(file_path)
            
    def chunk_data(self, data: bytes) -> List[ChunkInfo]:
        """Split data using rolling hash chunking."""
        if len(data) == 0:
            return []
        return self.rolling_chunker.chunk_data(data)
        
    def _chunk_image_file(self, file_path: Path) -> List[ChunkInfo]:
        """Chunk image files with format awareness."""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
                
            # For PNG files, try to chunk at IDAT boundaries
            if file_path.suffix.lower() == '.png':
                return self._chunk_png_data(data)
            else:
                # Use rolling hash for other image formats
                return self.rolling_chunker.chunk_data(data)
                
        except Exception as e:
            raise ChunkingError(f"Failed to chunk image file {file_path}: {e}")
            
    def _chunk_png_data(self, data: bytes) -> List[ChunkInfo]:
        """Chunk PNG data at IDAT chunk boundaries."""
        chunks = []
        offset = 0
        
        # PNG signature is 8 bytes
        if len(data) < 8 or data[:8] != b'\x89PNG\r\n\x1a\n':
            # Not a valid PNG, use regular chunking
            return self.rolling_chunker.chunk_data(data)
            
        chunk_start = 0
        i = 8  # Skip PNG signature
        
        while i < len(data) - 8:
            # Read chunk length (4 bytes, big-endian)
            if i + 4 > len(data):
                break
                
            chunk_length = int.from_bytes(data[i:i+4], 'big')
            chunk_type = data[i+4:i+8]
            
            # Check if this is an IDAT chunk (image data)
            if chunk_type == b'IDAT' and i - chunk_start >= self.config.chunk_size_min:
                # Create chunk up to this point
                chunk_data = data[chunk_start:i]
                chunk_hash = calculate_data_hash(chunk_data)
                
                chunks.append(ChunkInfo(
                    hash=chunk_hash,
                    size=len(chunk_data),
                    offset=chunk_start
                ))
                
                chunk_start = i
                
            # Move to next chunk (length + type + data + CRC)
            i += 4 + 4 + chunk_length + 4
            
        # Handle remaining data
        if chunk_start < len(data):
            chunk_data = data[chunk_start:]
            chunk_hash = calculate_data_hash(chunk_data)
            
            chunks.append(ChunkInfo(
                hash=chunk_hash,
                size=len(chunk_data),
                offset=chunk_start
            ))
            
        return chunks if chunks else self.rolling_chunker.chunk_data(data)
        
    def _chunk_audio_file(self, file_path: Path) -> List[ChunkInfo]:
        """Chunk audio files with format awareness."""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
                
            # For WAV files, try to chunk at data boundaries
            if file_path.suffix.lower() == '.wav':
                return self._chunk_wav_data(data)
            else:
                # Use rolling hash for other audio formats
                return self.rolling_chunker.chunk_data(data)
                
        except Exception as e:
            raise ChunkingError(f"Failed to chunk audio file {file_path}: {e}")
            
    def _chunk_wav_data(self, data: bytes) -> List[ChunkInfo]:
        """Chunk WAV data at chunk boundaries."""
        # Simple WAV chunking - look for 'data' chunk
        if len(data) < 12 or data[:4] != b'RIFF' or data[8:12] != b'WAVE':
            return self.rolling_chunker.chunk_data(data)
            
        # Find data chunk
        i = 12
        while i < len(data) - 8:
            chunk_id = data[i:i+4]
            chunk_size = int.from_bytes(data[i+4:i+8], 'little')
            
            if chunk_id == b'data':
                # Split at data chunk boundary if significant
                if i >= self.config.chunk_size_min:
                    chunks = []
                    
                    # Header chunk
                    header_data = data[:i]
                    header_hash = calculate_data_hash(header_data)
                    chunks.append(ChunkInfo(
                        hash=header_hash,
                        size=len(header_data),
                        offset=0
                    ))
                    
                    # Data chunk
                    data_chunk = data[i:]
                    data_hash = calculate_data_hash(data_chunk)
                    chunks.append(ChunkInfo(
                        hash=data_hash,
                        size=len(data_chunk),
                        offset=i
                    ))
                    
                    return chunks
                break
                
            i += 8 + chunk_size
            
        return self.rolling_chunker.chunk_data(data)
        
    def _chunk_model_file(self, file_path: Path) -> List[ChunkInfo]:
        """Chunk 3D model files."""
        # For now, use rolling hash chunking for model files
        # Could be enhanced with format-specific boundaries
        return self.rolling_chunker.chunk_file(file_path)


def create_chunker(strategy: str, config: ChunkingConfig) -> ChunkingStrategy:
    """
    Factory function to create chunking strategy.
    
    Args:
        strategy: Chunking strategy name
        config: Chunking configuration
        
    Returns:
        ChunkingStrategy instance
        
    Raises:
        ChunkingError: If unknown strategy requested
    """
    if strategy == "fixed":
        return FixedSizeChunker(config.chunk_size_max)
    elif strategy == "rolling_hash":
        return RollingHashChunker(config)
    elif strategy == "game_asset":
        return GameAssetChunker(config)
    else:
        raise ChunkingError(f"Unknown chunking strategy: {strategy}")