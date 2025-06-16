"""
Configuration module for GameVault.

This module contains game-specific configuration extending common configuration.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Set, Union

from pydantic import BaseModel, Field

# Import common configuration
from common.core.config import UnifiedBackupConfig
from common.core.models import ChunkingConfig, CompressionConfig


class GameVaultConfig(UnifiedBackupConfig):
    """Game-specific configuration extending UnifiedBackupConfig."""
    
    # Override backup directory default for games
    backup_dir: Path = Field(
        default_factory=lambda: Path.home() / ".gamevault",
        description="Directory where all backups will be stored"
    )
    
    # Game-specific ignore patterns (extends common patterns)
    ignore_patterns: List[str] = Field(
        default_factory=lambda: [
            "*.tmp", "*.temp", "*.log", "*.bak",
            ".git/*", ".svn/*", ".vscode/*", ".idea/*",
            "__pycache__/*", "*.pyc",
            "Temp/*", "Library/PackageCache/*",  # Unity specific
            "Saved/*", "Intermediate/*",  # Unreal specific
            "Build/*", "Builds/*", "Build-*/*",  # Build directories
            "*.meta", "*.csproj", "*.sln",  # Unity project files
            "*.uproject", "Binaries/*", "DerivedDataCache/*",  # Unreal project files
            "node_modules/*", "*.pdb", "*.vshost.exe",  # Development files
            ".vs/*", "obj/*", "bin/*"  # Visual Studio files
        ],
        description="File patterns to ignore during backup"
    )
    
    # Game-specific binary extensions (extends common extensions)
    binary_extensions: Set[str] = Field(
        default_factory=lambda: {
            # Images
            ".png", ".jpg", ".jpeg", ".bmp", ".tga", ".gif", ".psd", ".tif", ".tiff",
            ".hdr", ".exr", ".dds", ".pvr", ".ktx", ".astc",
            # 3D Models
            ".fbx", ".obj", ".blend", ".dae", ".3ds", ".max", ".ma", ".mb",
            ".c4d", ".lwo", ".lws", ".ply", ".stl", ".x3d", ".gltf", ".glb",
            # Audio
            ".wav", ".mp3", ".ogg", ".flac", ".aif", ".aiff", ".wma", ".m4a",
            ".opus", ".vorbis", ".ac3", ".dts",
            # Video
            ".mp4", ".avi", ".mov", ".wmv", ".webm", ".flv", ".mkv", ".m4v",
            ".ogv", ".3gp", ".asf", ".vob",
            # Game Engines
            ".unity", ".uasset", ".umap", ".upk", ".pak",  # Unity and Unreal
            ".godot", ".tscn", ".tres", ".gd",  # Godot
            ".scene", ".scn", ".mesh", ".material",  # Generic engine assets
            # Other Binary Formats
            ".zip", ".rar", ".7z", ".tar", ".gz", ".exe", ".dll", ".so", ".dylib",
            # Game-specific binary assets
            ".asset", ".prefab", ".controller", ".anim", ".animset",  # Unity
            ".cube", ".lightmap", ".navmesh", ".terrain",  # Unreal and others
            ".bank", ".fev", ".fsb", ".fmod",  # FMOD audio
            ".wwise", ".bnk", ".wem", ".wpk"  # Wwise audio
        },
        description="File extensions to treat as binary files"
    )
    
    # Game-specific default platforms
    default_platforms: List[str] = Field(
        default_factory=lambda: ["pc", "mobile", "console", "vr", "web"],
        description="Default platforms to track for configuration management"
    )
    
    # Game-specific chunking strategy
    chunking_strategy: str = "game_asset"
    
    # Game-specific features
    enable_asset_optimization: bool = Field(
        default=True,
        description="Enable asset optimization features"
    )
    
    enable_playtest_recording: bool = Field(
        default=True,
        description="Enable playtest recording features"
    )
    
    enable_feedback_system: bool = Field(
        default=True,
        description="Enable feedback collection system"
    )
    
    # Milestone management
    auto_milestone_detection: bool = Field(
        default=True,
        description="Automatically detect milestones based on version patterns"
    )
    
    milestone_patterns: List[str] = Field(
        default_factory=lambda: [
            "alpha", "beta", "rc", "release", "final",
            "milestone", "demo", "preview", "build"
        ],
        description="Patterns to detect milestones in version names"
    )
    
    # Platform-specific settings
    platform_build_paths: Dict[str, str] = Field(
        default_factory=lambda: {
            "pc": "Builds/PC",
            "mobile": "Builds/Mobile", 
            "console": "Builds/Console",
            "vr": "Builds/VR",
            "web": "Builds/WebGL"
        },
        description="Platform-specific build output paths"
    )


# Singleton instance that can be imported and used throughout the codebase
default_config = GameVaultConfig()


def get_config() -> GameVaultConfig:
    """
    Get the current configuration.
    
    Returns:
        GameVaultConfig: The current configuration instance
    """
    return default_config


def configure(config_dict: Dict) -> GameVaultConfig:
    """
    Update the configuration with new values.
    
    Args:
        config_dict: Dictionary of configuration values to update
    
    Returns:
        GameVaultConfig: The updated configuration instance
    """
    global default_config
    default_config = GameVaultConfig(**{**default_config.dict(), **config_dict})
    
    # Ensure backup directory exists
    os.makedirs(default_config.backup_dir, exist_ok=True)
    
    return default_config


def get_game_chunking_config() -> ChunkingConfig:
    """
    Get game-specific chunking configuration.
    
    Returns:
        ChunkingConfig: Game-optimized chunking configuration
    """
    config = get_config()
    return ChunkingConfig(
        strategy="game_asset",
        window_size=48,
        polynomial=0x3DA3358B4DC173,
        chunk_size_min=config.chunk_size_min,
        chunk_size_max=config.chunk_size_max,
        boundary_mask=0x1FFF  # 8KB average chunk size for games
    )


def get_game_compression_config() -> CompressionConfig:
    """
    Get game-specific compression configuration.
    
    Returns:
        CompressionConfig: Game-optimized compression configuration
    """
    config = get_config()
    return CompressionConfig(
        algorithm="zstd",
        level=config.compression_level,
        enable_delta_compression=True,
        delta_threshold=0.4  # Slightly higher threshold for game assets
    )