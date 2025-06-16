"""
Core components of the unified backup system.

This module provides the foundational components that can be used
across all persona implementations:
- Data models and configuration
- Backup engine with chunking and deduplication
- Content-addressed storage system
- File utilities and hashing
- Compression and chunking strategies
- Visual processing and timeline management
- Asset tracking and workspace management
"""

from .backup_engine import BackupEngine, UnifiedBackupEngine
from .chunking import ChunkingStrategy, FixedSizeChunker, RollingHashChunker, GameAssetChunker, create_chunker
from .compression import compress_data, decompress_data, DeltaCompressor
from .config import UnifiedBackupConfig, ConfigManager, load_config, save_config
from .exceptions import (
    BackupSystemError, StorageError, CompressionError, ChunkingError,
    HashError, ConfigurationError, SnapshotError, RestoreError,
    FileNotFoundError, CorruptedDataError
)
from .file_utils import (
    scan_directory, get_file_type, is_binary_file, get_file_info,
    compare_files, ensure_directory, safe_file_copy, normalize_path
)
from .hashing import calculate_file_hash, calculate_data_hash, verify_file_hash, RollingHasher
from .models import (
    FileInfo, ChunkInfo, SnapshotInfo, ChangeInfo, ChangeSet,
    BackupConfig, ChunkingConfig, CompressionConfig, StorageStats,
    FileType, ChangeType, CreativeFileType, GameFileType, Platform,
    TimelineEntry, ReferenceInfo, ReferenceMap, WorkspaceState,
    FILE_TYPE_MAPPINGS
)
from .storage import ContentAddressedStorage, MetadataStorage

# New framework components
from .visual import (
    BaseVisualDiffGenerator, BaseTimelineManager, ImageDiffUtils, ModelDiffUtils,
    DiffType, DiffResult, TimelineEntry
)
from .assets import (
    BaseAssetTracker, AssetUtils, AssetInfo, DependencyInfo, ReferenceMap,
    AssetType, DependencyType
)
from .workspace import (
    BaseWorkspaceCapture, WorkspaceUtils, ApplicationInfo, WorkspaceState,
    ApplicationType, PlatformType
)

__all__ = [
    # Abstract base classes
    'BackupEngine',
    'ChunkingStrategy',
    'BaseVisualDiffGenerator',
    'BaseTimelineManager',
    'BaseAssetTracker',
    'BaseWorkspaceCapture',
    
    # Core implementations
    'UnifiedBackupEngine',
    'ContentAddressedStorage',
    'MetadataStorage',
    
    # Chunking strategies
    'FixedSizeChunker',
    'RollingHashChunker', 
    'GameAssetChunker',
    'create_chunker',
    
    # Compression
    'compress_data',
    'decompress_data',
    'DeltaCompressor',
    
    # Configuration
    'UnifiedBackupConfig',
    'ConfigManager',
    'load_config',
    'save_config',
    
    # Data models
    'FileInfo',
    'ChunkInfo',
    'SnapshotInfo',
    'ChangeInfo',
    'ChangeSet',
    'BackupConfig',
    'ChunkingConfig',
    'CompressionConfig',
    'StorageStats',
    
    # Framework data models
    'DiffResult',
    'TimelineEntry',
    'ReferenceInfo',
    'ReferenceMap',
    'WorkspaceState',
    'AssetInfo',
    'DependencyInfo',
    'ApplicationInfo',
    
    # Enums
    'FileType',
    'ChangeType',
    'CreativeFileType',
    'GameFileType',
    'Platform',
    'DiffType',
    'AssetType',
    'DependencyType',
    'ApplicationType',
    'PlatformType',
    'FILE_TYPE_MAPPINGS',
    
    # File utilities
    'scan_directory',
    'get_file_type',
    'is_binary_file',
    'get_file_info',
    'compare_files',
    'ensure_directory',
    'safe_file_copy',
    'normalize_path',
    
    # Framework utilities
    'ImageDiffUtils',
    'ModelDiffUtils',
    'AssetUtils',
    'WorkspaceUtils',
    
    # Hashing
    'calculate_file_hash',
    'calculate_data_hash',
    'verify_file_hash',
    'RollingHasher',
    
    # Exceptions
    'BackupSystemError',
    'StorageError',
    'CompressionError',
    'ChunkingError',
    'HashError',
    'ConfigurationError',
    'SnapshotError',
    'RestoreError',
    'FileNotFoundError',
    'CorruptedDataError',
]
