"""
Asset compression module for GameVault.

This module provides specialized compression algorithms for game assets.
"""

import io
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, BinaryIO

import bsdiff4
import numpy as np
from pyzstd import compress, decompress

from gamevault.utils import compress_data, decompress_data


class AssetCompressor:
    """
    Base class for asset compression.
    
    This class serves as a base for specialized asset compressors
    that optimize storage of game assets.
    """
    
    def compress(self, data: bytes) -> bytes:
        """
        Compress binary asset data.
        
        Args:
            data: Binary data to compress
            
        Returns:
            bytes: Compressed data
        """
        return compress_data(data)
    
    def decompress(self, compressed_data: bytes) -> bytes:
        """
        Decompress binary asset data.
        
        Args:
            compressed_data: Compressed binary data
            
        Returns:
            bytes: Decompressed data
        """
        return decompress_data(compressed_data)


class TextureCompressor(AssetCompressor):
    """
    Specialized compressor for texture assets.
    
    This class optimizes storage of texture assets like images and textures.
    """
    
    def __init__(self, compression_level: int = 3):
        """
        Initialize the texture compressor.
        
        Args:
            compression_level: Compression level (0-22 for zstd)
        """
        self.compression_level = compression_level
    
    def compress(self, data: bytes) -> bytes:
        """
        Compress texture data.
        
        Args:
            data: Binary texture data
            
        Returns:
            bytes: Compressed data
        """
        # For texture assets, we use a higher compression level
        # than the default to achieve better compression ratios
        return compress_data(data, self.compression_level)


class AudioCompressor(AssetCompressor):
    """
    Specialized compressor for audio assets.
    
    This class optimizes storage of audio assets like sound effects and music.
    """
    
    def __init__(self, compression_level: int = 2):
        """
        Initialize the audio compressor.
        
        Args:
            compression_level: Compression level (0-22 for zstd)
        """
        self.compression_level = compression_level
    
    def compress(self, data: bytes) -> bytes:
        """
        Compress audio data.
        
        Args:
            data: Binary audio data
            
        Returns:
            bytes: Compressed data
        """
        # Audio files are often already compressed, so we use a lower
        # compression level to avoid diminishing returns
        return compress_data(data, self.compression_level)


class ModelCompressor(AssetCompressor):
    """
    Specialized compressor for 3D model assets.
    
    This class optimizes storage of 3D model assets.
    """
    
    def __init__(self, compression_level: int = 5):
        """
        Initialize the model compressor.
        
        Args:
            compression_level: Compression level (0-22 for zstd)
        """
        self.compression_level = compression_level
    
    def compress(self, data: bytes) -> bytes:
        """
        Compress 3D model data.
        
        Args:
            data: Binary model data
            
        Returns:
            bytes: Compressed data
        """
        # 3D models often have good compression potential,
        # so we use a higher compression level
        return compress_data(data, self.compression_level)


class DeltaCompressor:
    """
    Delta compressor for storing differences between asset versions.
    
    This class uses binary diffing to store only the changes between
    versions of an asset, rather than entire copies.
    """
    
    def create_delta(self, source_data: bytes, target_data: bytes) -> bytes:
        """
        Create a binary delta between source and target data.
        
        Args:
            source_data: Original binary data
            target_data: New binary data
            
        Returns:
            bytes: Delta patch
        """
        return bsdiff4.diff(source_data, target_data)
    
    def apply_delta(self, source_data: bytes, delta_data: bytes) -> bytes:
        """
        Apply a delta patch to source data to produce target data.
        
        Args:
            source_data: Original binary data
            delta_data: Delta patch
            
        Returns:
            bytes: Reconstructed target data
        """
        return bsdiff4.patch(source_data, delta_data)
    
    def compress_delta(self, delta_data: bytes, compression_level: int = 9) -> bytes:
        """
        Compress a delta patch.
        
        Args:
            delta_data: Delta patch data
            compression_level: Compression level (0-22 for zstd)
            
        Returns:
            bytes: Compressed delta patch
        """
        # Delta patches compress very well, so we use a high compression level
        return compress_data(delta_data, compression_level)
    
    def decompress_delta(self, compressed_delta: bytes) -> bytes:
        """
        Decompress a compressed delta patch.
        
        Args:
            compressed_delta: Compressed delta patch
            
        Returns:
            bytes: Decompressed delta patch
        """
        return decompress_data(compressed_delta)


class AssetCompressorFactory:
    """
    Factory for creating asset compressors based on file type.
    
    This class provides appropriate compressors for different asset types.
    """
    
    @staticmethod
    def get_compressor(file_extension: str) -> AssetCompressor:
        """
        Get an appropriate compressor for a file type.
        
        Args:
            file_extension: Extension of the file
            
        Returns:
            AssetCompressor: An appropriate compressor instance
        """
        file_extension = file_extension.lower()
        
        # Images and textures
        if file_extension in {".png", ".jpg", ".jpeg", ".bmp", ".tga", ".gif", ".psd", ".tif", ".tiff"}:
            return TextureCompressor()
        
        # Audio files
        elif file_extension in {".wav", ".mp3", ".ogg", ".flac", ".aif", ".aiff"}:
            return AudioCompressor()
        
        # 3D models
        elif file_extension in {".fbx", ".obj", ".blend", ".dae", ".3ds", ".max"}:
            return ModelCompressor()
        
        # Default compressor for other assets
        else:
            return AssetCompressor()