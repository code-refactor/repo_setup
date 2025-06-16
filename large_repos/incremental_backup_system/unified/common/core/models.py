"""
Core data models for the unified backup system.

This module defines the shared data structures used across all persona implementations.
"""

from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union

from pydantic import BaseModel, Field


class FileType(str, Enum):
    """File type classification for backup processing."""
    IMAGE = "image"
    MODEL_3D = "model_3d"
    AUDIO = "audio"
    VIDEO = "video"
    TEXT = "text"
    BINARY = "binary"
    ARCHIVE = "archive"
    DOCUMENT = "document"
    PROJECT = "project"
    UNKNOWN = "unknown"


class CreativeFileType(str, Enum):
    """Creative-specific file type classifications."""
    ADOBE_PROJECT = "adobe_project"
    BLENDER_PROJECT = "blender_project"
    MAYA_PROJECT = "maya_project"
    SUBSTANCE_PROJECT = "substance_project"
    SKETCH_PROJECT = "sketch_project"
    FIGMA_FILE = "figma_file"
    TEXTURE = "texture"
    HDR = "hdr"
    NORMAL_MAP = "normal_map"
    HEIGHT_MAP = "height_map"
    

class GameFileType(str, Enum):
    """Game development specific file type classifications."""
    GAME_ASSET = "game_asset"
    TEXTURE_ATLAS = "texture_atlas"
    ANIMATION = "animation"
    SHADER = "shader"
    LEVEL_DATA = "level_data"
    SCRIPT = "script"
    BUILD_ARTIFACT = "build_artifact"
    PLATFORM_BINARY = "platform_binary"
    

class Platform(str, Enum):
    """Supported game development platforms."""
    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "macos"
    ANDROID = "android"
    IOS = "ios"
    WEB = "web"
    CONSOLE = "console"


class ChangeType(str, Enum):
    """Type of change detected in file comparison."""
    ADDED = "added"
    MODIFIED = "modified"
    DELETED = "deleted"
    MOVED = "moved"
    UNCHANGED = "unchanged"


@dataclass
class ChunkInfo:
    """Information about a file chunk."""
    hash: str
    size: int
    offset: int
    compressed_size: Optional[int] = None


@dataclass
class FileInfo:
    """Comprehensive file metadata for backup tracking."""
    path: Path
    size: int
    hash: str
    modified_time: datetime
    file_type: FileType
    content_type: str = ""
    chunk_hashes: List[str] = field(default_factory=list)
    chunks: List[ChunkInfo] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Ensure path is a Path object and normalize it."""
        if isinstance(self.path, str):
            self.path = Path(self.path)
        self.path = self.path.resolve()


@dataclass
class ChangeInfo:
    """Information about a file change between versions."""
    file_path: Path
    change_type: ChangeType
    old_file: Optional[FileInfo] = None
    new_file: Optional[FileInfo] = None
    
    def __post_init__(self):
        """Ensure path is a Path object."""
        if isinstance(self.file_path, str):
            self.file_path = Path(self.file_path)


@dataclass
class SnapshotInfo:
    """Information about a backup snapshot."""
    id: str
    timestamp: datetime
    source_path: Path
    parent_id: Optional[str] = None
    files: List[FileInfo] = field(default_factory=list)
    changes: List[ChangeInfo] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: Set[str] = field(default_factory=set)
    
    def __post_init__(self):
        """Ensure source_path is a Path object."""
        if isinstance(self.source_path, str):
            self.source_path = Path(self.source_path)


@dataclass
class ChangeSet:
    """Collection of changes between two snapshots."""
    from_snapshot: str
    to_snapshot: str
    changes: List[ChangeInfo]
    summary: Dict[str, int] = field(default_factory=dict)
    
    def __post_init__(self):
        """Calculate change summary."""
        if not self.summary:
            self.summary = {
                "added": sum(1 for c in self.changes if c.change_type == ChangeType.ADDED),
                "modified": sum(1 for c in self.changes if c.change_type == ChangeType.MODIFIED),
                "deleted": sum(1 for c in self.changes if c.change_type == ChangeType.DELETED),
                "moved": sum(1 for c in self.changes if c.change_type == ChangeType.MOVED),
            }


class BackupConfig(BaseModel):
    """Base configuration for backup operations."""
    backup_dir: Path
    chunk_size_min: int = Field(default=1024, ge=256)
    chunk_size_max: int = Field(default=1024*1024, ge=1024)
    compression_level: int = Field(default=3, ge=0, le=22)
    ignore_patterns: List[str] = Field(default_factory=list)
    binary_extensions: Set[str] = Field(default_factory=lambda: {
        '.exe', '.dll', '.so', '.dylib', '.bin', '.dat', '.pak', '.wad'
    })
    enable_deduplication: bool = True
    enable_compression: bool = True
    hash_algorithm: str = "sha256"
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True
        
    def __init__(self, **data):
        """Initialize with Path conversion."""
        if 'backup_dir' in data and isinstance(data['backup_dir'], str):
            data['backup_dir'] = Path(data['backup_dir'])
        super().__init__(**data)


class ChunkingConfig(BaseModel):
    """Configuration for chunking strategies."""
    strategy: str = "rolling_hash"
    window_size: int = 64
    polynomial: int = 0x3DA3358B4DC173
    chunk_size_min: int = 1024
    chunk_size_max: int = 1024 * 1024
    boundary_mask: int = 0xFFF  # 4KB average chunk size


class CompressionConfig(BaseModel):
    """Configuration for compression settings."""
    algorithm: str = "zstd"
    level: int = 3
    enable_delta_compression: bool = True
    delta_threshold: float = 0.3  # Must achieve 30% size reduction


@dataclass
class StorageStats:
    """Statistics about storage usage."""
    total_files: int = 0
    total_size: int = 0
    compressed_size: int = 0
    deduplicated_chunks: int = 0
    unique_chunks: int = 0
    compression_ratio: float = 0.0
    deduplication_ratio: float = 0.0
    
    def __post_init__(self):
        """Calculate ratios."""
        if self.total_size > 0:
            self.compression_ratio = self.compressed_size / self.total_size
        if self.unique_chunks > 0:
            self.deduplication_ratio = self.deduplicated_chunks / (self.deduplicated_chunks + self.unique_chunks)


@dataclass
class TimelineEntry:
    """Represents a point in a file's timeline."""
    snapshot_id: str
    timestamp: datetime
    file_path: Path
    file_info: FileInfo
    change_type: ChangeType
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Ensure path is a Path object."""
        if isinstance(self.file_path, str):
            self.file_path = Path(self.file_path)


@dataclass
class ReferenceInfo:
    """Information about file references and dependencies."""
    source_file: Path
    referenced_file: Path
    reference_type: str
    line_number: Optional[int] = None
    context: Optional[str] = None
    
    def __post_init__(self):
        """Ensure paths are Path objects."""
        if isinstance(self.source_file, str):
            self.source_file = Path(self.source_file)
        if isinstance(self.referenced_file, str):
            self.referenced_file = Path(self.referenced_file)


@dataclass
class ReferenceMap:
    """Maps file dependencies and references."""
    project_root: Path
    references: List[ReferenceInfo] = field(default_factory=list)
    reverse_references: Dict[Path, List[ReferenceInfo]] = field(default_factory=dict)
    
    def __post_init__(self):
        """Build reverse reference mapping."""
        if isinstance(self.project_root, str):
            self.project_root = Path(self.project_root)
        
        self.reverse_references = {}
        for ref in self.references:
            if ref.referenced_file not in self.reverse_references:
                self.reverse_references[ref.referenced_file] = []
            self.reverse_references[ref.referenced_file].append(ref)


@dataclass  
class WorkspaceState:
    """Represents the state of a workspace at a point in time."""
    timestamp: datetime
    application: str
    version: str
    open_files: List[Path] = field(default_factory=list)
    active_projects: List[Path] = field(default_factory=list)
    environment_vars: Dict[str, str] = field(default_factory=dict)
    settings: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Ensure paths are Path objects."""
        self.open_files = [Path(f) if isinstance(f, str) else f for f in self.open_files]
        self.active_projects = [Path(p) if isinstance(p, str) else p for p in self.active_projects]




# File type detection mappings
FILE_TYPE_MAPPINGS = {
    # Images
    '.png': FileType.IMAGE,
    '.jpg': FileType.IMAGE,
    '.jpeg': FileType.IMAGE,
    '.gif': FileType.IMAGE,
    '.bmp': FileType.IMAGE,
    '.tiff': FileType.IMAGE,
    '.tga': FileType.IMAGE,
    '.webp': FileType.IMAGE,
    '.svg': FileType.IMAGE,
    '.psd': FileType.IMAGE,
    '.xcf': FileType.IMAGE,
    
    # 3D Models
    '.obj': FileType.MODEL_3D,
    '.fbx': FileType.MODEL_3D,
    '.dae': FileType.MODEL_3D,
    '.3ds': FileType.MODEL_3D,
    '.blend': FileType.MODEL_3D,
    '.max': FileType.MODEL_3D,
    '.ma': FileType.MODEL_3D,
    '.mb': FileType.MODEL_3D,
    '.c4d': FileType.MODEL_3D,
    '.lwo': FileType.MODEL_3D,
    '.stl': FileType.MODEL_3D,
    '.ply': FileType.MODEL_3D,
    '.gltf': FileType.MODEL_3D,
    '.glb': FileType.MODEL_3D,
    
    # Audio
    '.wav': FileType.AUDIO,
    '.mp3': FileType.AUDIO,
    '.ogg': FileType.AUDIO,
    '.flac': FileType.AUDIO,
    '.aac': FileType.AUDIO,
    '.m4a': FileType.AUDIO,
    '.wma': FileType.AUDIO,
    
    # Video
    '.mp4': FileType.VIDEO,
    '.avi': FileType.VIDEO,
    '.mov': FileType.VIDEO,
    '.mkv': FileType.VIDEO,
    '.wmv': FileType.VIDEO,
    '.flv': FileType.VIDEO,
    '.webm': FileType.VIDEO,
    
    # Text
    '.txt': FileType.TEXT,
    '.py': FileType.TEXT,
    '.js': FileType.TEXT,
    '.css': FileType.TEXT,
    '.html': FileType.TEXT,
    '.xml': FileType.TEXT,
    '.json': FileType.TEXT,
    '.yaml': FileType.TEXT,
    '.yml': FileType.TEXT,
    '.md': FileType.TEXT,
    '.rst': FileType.TEXT,
    '.c': FileType.TEXT,
    '.cpp': FileType.TEXT,
    '.h': FileType.TEXT,
    '.hpp': FileType.TEXT,
    '.cs': FileType.TEXT,
    '.java': FileType.TEXT,
    '.go': FileType.TEXT,
    '.rs': FileType.TEXT,
    
    # Archives
    '.zip': FileType.ARCHIVE,
    '.rar': FileType.ARCHIVE,
    '.7z': FileType.ARCHIVE,
    '.tar': FileType.ARCHIVE,
    '.gz': FileType.ARCHIVE,
    '.bz2': FileType.ARCHIVE,
    '.xz': FileType.ARCHIVE,
    
    # Documents
    '.pdf': FileType.DOCUMENT,
    '.doc': FileType.DOCUMENT,
    '.docx': FileType.DOCUMENT,
    '.xls': FileType.DOCUMENT,
    '.xlsx': FileType.DOCUMENT,
    '.ppt': FileType.DOCUMENT,
    '.pptx': FileType.DOCUMENT,
    
    # Project files
    '.sln': FileType.PROJECT,
    '.vcxproj': FileType.PROJECT,
    '.csproj': FileType.PROJECT,
    '.vbproj': FileType.PROJECT,
    '.unity': FileType.PROJECT,
    '.unitypackage': FileType.PROJECT,
    '.uproject': FileType.PROJECT,
    '.uasset': FileType.PROJECT,
}