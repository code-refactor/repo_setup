"""
Chunking module for GameVault backup engine.

This module provides game-specific chunking strategies extending common strategies.
"""

import abc
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union

# Import common chunking strategies
from common.core.chunking import (
    ChunkingStrategy as CommonChunkingStrategy,
    FixedSizeChunker as CommonFixedSizeChunker,
    RollingHashChunker as CommonRollingHashChunker,
    GameAssetChunker as CommonGameAssetChunker,
    create_chunker
)
from common.core.models import ChunkInfo, ChunkingConfig


# Backward compatibility aliases - extend common strategies
ChunkingStrategy = CommonChunkingStrategy


class FixedSizeChunker(CommonFixedSizeChunker):
    """
    Game-specific fixed-size chunking strategy extending common implementation.
    
    Provides backward compatibility while using the common chunking infrastructure.
    """
    
    def __init__(self, chunk_size: int = 1024 * 1024):
        """
        Initialize the fixed-size chunker.
        
        Args:
            chunk_size: Size of each chunk in bytes
        """
        super().__init__(chunk_size)
    
    def chunk_data(self, data: bytes) -> List[bytes]:
        """
        Chunk binary data into fixed-size pieces.
        
        Args:
            data: Binary data to chunk
            
        Returns:
            List[bytes]: List of chunked data (backward compatibility)
        """
        chunk_infos = super().chunk_data(data)
        # Convert ChunkInfo objects back to raw bytes for backward compatibility
        chunks = []
        offset = 0
        for chunk_info in chunk_infos:
            chunk_data = data[offset:offset + chunk_info.size]
            chunks.append(chunk_data)
            offset += chunk_info.size
        return chunks


class RollingHashChunker(CommonRollingHashChunker):
    """
    Game-specific rolling hash chunking strategy extending common implementation.
    
    Provides backward compatibility while using the common chunking infrastructure.
    """
    
    def __init__(
        self,
        min_chunk_size: int = 64 * 1024,
        max_chunk_size: int = 4 * 1024 * 1024,
        window_size: int = 48,
        mask_bits: int = 13
    ):
        """
        Initialize the rolling hash chunker.
        
        Args:
            min_chunk_size: Minimum size of each chunk in bytes
            max_chunk_size: Maximum size of each chunk in bytes
            window_size: Size of the rolling hash window
            mask_bits: Number of bits to consider in the rolling hash
        """
        # Create chunking config compatible with common implementation
        config = ChunkingConfig(
            strategy="rolling_hash",
            window_size=window_size,
            chunk_size_min=min_chunk_size,
            chunk_size_max=max_chunk_size,
            boundary_mask=(1 << mask_bits) - 1
        )
        super().__init__(config)
        
        # Store original parameters for backward compatibility
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        self.window_size = window_size
        self.mask = (1 << mask_bits) - 1
    
    def _is_boundary(self, hash_value: int) -> bool:
        """
        Check if a hash value indicates a chunk boundary.
        
        Args:
            hash_value: Rolling hash value
            
        Returns:
            bool: True if the hash value indicates a boundary
        """
        return (hash_value & self.mask) == 0
    
    def chunk_data(self, data: bytes) -> List[bytes]:
        """
        Chunk binary data using content-defined chunking.

        Args:
            data: Binary data to chunk

        Returns:
            List[bytes]: List of chunked data (backward compatibility)
        """
        chunk_infos = super().chunk_data(data)
        # Convert ChunkInfo objects back to raw bytes for backward compatibility
        chunks = []
        offset = 0
        for chunk_info in chunk_infos:
            chunk_data = data[offset:offset + chunk_info.size]
            chunks.append(chunk_data)
            offset += chunk_info.size
        return chunks


class GameAssetChunker(CommonGameAssetChunker):
    """
    Game-specific asset chunking strategy extending common implementation.
    
    Provides backward compatibility while using the common chunking infrastructure.
    """
    
    def __init__(
        self,
        min_chunk_size: int = 64 * 1024,
        max_chunk_size: int = 4 * 1024 * 1024,
        image_chunk_size: int = 1024 * 1024,
        audio_chunk_size: int = 2 * 1024 * 1024
    ):
        """
        Initialize the game asset chunker.
        
        Args:
            min_chunk_size: Minimum size of each chunk in bytes
            max_chunk_size: Maximum size of each chunk in bytes
            image_chunk_size: Chunk size for image files
            audio_chunk_size: Chunk size for audio files
        """
        # Create chunking config compatible with common implementation
        config = ChunkingConfig(
            strategy="game_asset",
            window_size=48,
            chunk_size_min=min_chunk_size,
            chunk_size_max=max_chunk_size,
            boundary_mask=0x1FFF
        )
        super().__init__(config)
        
        # Store original chunkers for backward compatibility
        self.default_chunker = RollingHashChunker(min_chunk_size, max_chunk_size)
        self.image_chunker = FixedSizeChunker(image_chunk_size)
        self.audio_chunker = FixedSizeChunker(audio_chunk_size)
    
    def chunk_data(self, data: bytes, file_extension: Optional[str] = None) -> List[bytes]:
        """
        Chunk binary data based on the file type.
        
        Args:
            data: Binary data to chunk
            file_extension: Extension of the file
            
        Returns:
            List[bytes]: List of chunked data (backward compatibility)
        """
        if not file_extension:
            return self.default_chunker.chunk_data(data)
        
        # Choose chunking strategy based on file extension
        if file_extension.lower() in {".png", ".jpg", ".jpeg", ".bmp", ".tga", ".gif", ".psd"}:
            return self.image_chunker.chunk_data(data)
        elif file_extension.lower() in {".wav", ".mp3", ".ogg", ".flac", ".aif", ".aiff"}:
            return self.audio_chunker.chunk_data(data)
        else:
            return self.default_chunker.chunk_data(data)