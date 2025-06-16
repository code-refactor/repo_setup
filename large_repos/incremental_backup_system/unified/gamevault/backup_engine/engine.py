"""
Core backup engine for GameVault.

This module provides game-specific backup engine functionality extending common engine.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union, cast

import bsdiff4

# Import common backup engine
from common.core.backup_engine import UnifiedBackupEngine
from common.core.models import SnapshotInfo as CommonSnapshotInfo, ChangeInfo, ChangeType
from common.core.exceptions import BackupSystemError, SnapshotError

from gamevault.backup_engine.chunker import ChunkingStrategy, RollingHashChunker
from gamevault.backup_engine.storage import StorageManager
from gamevault.backup_engine.version_tracker import VersionTracker
from gamevault.config import get_config, get_game_chunking_config, GameVaultConfig
from gamevault.models import FileInfo, GameVersionType, ProjectVersion
from gamevault.utils import (generate_timestamp, get_file_hash, get_file_size,
                           get_file_modification_time, is_binary_file,
                           scan_directory)


class BackupEngine(UnifiedBackupEngine):
    """
    Game-specific backup engine extending UnifiedBackupEngine.
    
    This class provides game development workflow features while leveraging
    the common backup infrastructure.
    """
    
    def __init__(
        self,
        project_name: str,
        project_path: Union[str, Path],
        storage_dir: Optional[Union[str, Path]] = None,
        chunking_strategy: Optional[ChunkingStrategy] = None
    ):
        """
        Initialize the game backup engine.
        
        Args:
            project_name: Name of the project
            project_path: Path to the project directory
            storage_dir: Directory where backups will be stored. If None, uses the default from config.
            chunking_strategy: Strategy for chunking binary files. If None, uses RollingHashChunker.
        """
        # Get game-specific configuration
        game_config = get_config()
        self.game_config = game_config
        self.project_name = project_name
        self.project_path = Path(project_path)
        
        # Directory for storing backups
        backup_dir = Path(storage_dir) if storage_dir else game_config.backup_dir
        
        # Create unified config for the common engine
        unified_config = GameVaultConfig(
            backup_dir=backup_dir,
            chunk_size_min=game_config.chunk_size_min,
            chunk_size_max=game_config.chunk_size_max,
            compression_level=game_config.compression_level,
            ignore_patterns=game_config.ignore_patterns,
            binary_extensions=game_config.binary_extensions,
            chunking_strategy="game_asset",
            chunking_config=get_game_chunking_config()
        )
        
        # Initialize the common backup engine
        super().__init__(unified_config)
        
        # Initialize game-specific components
        self.storage_manager = StorageManager(backup_dir)
        self.version_tracker = VersionTracker(project_name, backup_dir)
        self.chunking_strategy = chunking_strategy or RollingHashChunker(
            min_chunk_size=unified_config.chunk_size_min,
            max_chunk_size=unified_config.chunk_size_max
        )
    
    def _scan_project_files(self) -> Dict[str, Dict]:
        """
        Scan the project directory for files.
        
        Returns:
            Dict[str, Dict]: Dictionary of file paths to file metadata
        """
        files = {}
        
        for file_path in scan_directory(self.project_path, self.config.ignore_patterns):
            rel_path = str(file_path.relative_to(self.project_path))
            
            files[rel_path] = {
                "path": rel_path,
                "size": get_file_size(file_path),
                "modified_time": get_file_modification_time(file_path),
                "is_binary": is_binary_file(file_path, self.config.binary_extensions),
                "abs_path": str(file_path)
            }
        
        return files
    
    def _detect_changes(
        self, 
        current_files: Dict[str, Dict], 
        prev_version: Optional[ProjectVersion] = None
    ) -> Tuple[Dict[str, Dict], Dict[str, FileInfo], Set[str]]:
        """
        Detect changes between the current state and the previous version.
        
        Args:
            current_files: Dictionary of current file paths to file metadata
            prev_version: Previous version to compare against
            
        Returns:
            Tuple containing:
                Dict[str, Dict]: Files that have changed
                Dict[str, FileInfo]: Files from the previous version that haven't changed
                Set[str]: Paths that have been deleted
        """
        if prev_version is None:
            # No previous version, all files are new
            return current_files, {}, set()
        
        changed_files = {}
        unchanged_files = {}
        deleted_files = set()
        
        # Check for changed or unchanged files
        for rel_path, file_meta in current_files.items():
            if rel_path in prev_version.files:
                prev_file = prev_version.files[rel_path]
                abs_path = file_meta["abs_path"]
                
                # Calculate current file hash to properly detect changes
                current_hash = get_file_hash(abs_path)
                
                # Check if content has actually changed by comparing hash values
                if current_hash != prev_file.hash or file_meta["modified_time"] > prev_file.modified_time:
                    changed_files[rel_path] = file_meta
                else:
                    # File hasn't changed, use info from previous version
                    unchanged_files[rel_path] = prev_file
            else:
                # New file
                changed_files[rel_path] = file_meta
        
        # Check for deleted files
        for rel_path in prev_version.files:
            if rel_path not in current_files:
                deleted_files.add(rel_path)
        
        return changed_files, unchanged_files, deleted_files
    
    def _process_text_file(self, file_path: Union[str, Path]) -> Tuple[str, str]:
        """
        Process a text file for backup.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Tuple[str, str]: File ID (hash) and storage path
        """
        return self.storage_manager.store_file(file_path)
    
    def _process_binary_file(self, file_path: Union[str, Path]) -> Tuple[str, List[str]]:
        """
        Process a binary file for backup using chunking.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Tuple[str, List[str]]: File hash and list of chunk IDs
        """
        file_path = Path(file_path)
        
        with open(file_path, "rb") as f:
            data = f.read()
        
        # Calculate file hash
        file_hash = get_file_hash(file_path)
        
        # Chunk the file
        chunks = self.chunking_strategy.chunk_data(data)
        
        # Store chunks
        chunk_ids = []
        for chunk in chunks:
            chunk_id = self.storage_manager.store_chunk(chunk)
            chunk_ids.append(chunk_id)
        
        return file_hash, chunk_ids
    
    def _process_file(self, file_path: Union[str, Path], is_binary: bool) -> FileInfo:
        """
        Process a file for backup.
        
        Args:
            file_path: Path to the file
            is_binary: Whether the file is binary
            
        Returns:
            FileInfo: Information about the processed file
        """
        file_path = Path(file_path)
        rel_path = str(file_path.relative_to(self.project_path))
        size = get_file_size(file_path)
        modified_time = get_file_modification_time(file_path)
        
        if is_binary:
            file_hash, chunks = self._process_binary_file(file_path)
            return FileInfo(
                path=rel_path,
                size=size,
                hash=file_hash,
                modified_time=modified_time,
                is_binary=True,
                chunks=chunks
            )
        else:
            file_hash, storage_path = self._process_text_file(file_path)
            return FileInfo(
                path=rel_path,
                size=size,
                hash=file_hash,
                modified_time=modified_time,
                is_binary=False,
                storage_path=storage_path
            )
    
    def create_backup(
        self,
        name: str,
        version_type: GameVersionType = GameVersionType.DEVELOPMENT,
        description: Optional[str] = None,
        is_milestone: bool = False,
        tags: Optional[List[str]] = None
    ) -> ProjectVersion:
        """
        Create a backup of the project using unified engine infrastructure.
        
        Args:
            name: Name of the backup version
            version_type: Type of the version
            description: Description of the version
            is_milestone: Whether this version is a milestone
            tags: List of tags for this version
            
        Returns:
            ProjectVersion: The created version
        """
        try:
            # Convert tags to set for common engine
            snapshot_tags = set(tags) if tags else set()
            snapshot_tags.add(f"version_type:{version_type.value}")
            if is_milestone:
                snapshot_tags.add("milestone")
            
            # Create snapshot using common engine
            snapshot = self.create_snapshot(
                source_path=self.project_path,
                tags=snapshot_tags
            )
            
            # Convert snapshot to ProjectVersion for game-specific interface
            project_version = ProjectVersion.from_common_snapshot_info(
                snapshot=snapshot,
                name=name,
                version_type=version_type,
                is_milestone=is_milestone
            )
            
            # Store game-specific metadata in the version tracker
            self.version_tracker.store_version_metadata(project_version)
            
            return project_version
            
        except Exception as e:
            raise BackupSystemError(f"Failed to create backup: {e}")
    
    def restore_version(
        self,
        version_id: str,
        output_path: Optional[Union[str, Path]] = None,
        excluded_paths: Optional[List[str]] = None
    ) -> Path:
        """
        Restore a version of the project using unified engine infrastructure.
        
        Args:
            version_id: ID of the version to restore
            output_path: Path where the version should be restored. If None, creates a new directory.
            excluded_paths: List of file paths to exclude from restoration
            
        Returns:
            Path: Path to the restored project
            
        Raises:
            FileNotFoundError: If the version doesn't exist
        """
        try:
            # Determine output path
            if output_path is None:
                timestamp = int(generate_timestamp())
                output_path = self.project_path.parent / f"{self.project_name}_restore_{timestamp}"
            
            output_path = Path(output_path)
            
            # Convert excluded paths to Path objects
            excluded_path_objects = None
            if excluded_paths:
                excluded_path_objects = [Path(p) for p in excluded_paths]
            
            # Use common engine restore functionality
            self.restore_snapshot(
                snapshot_id=version_id,
                target_path=output_path,
                selective_files=excluded_path_objects
            )
            
            return output_path
            
        except Exception as e:
            raise BackupSystemError(f"Failed to restore version {version_id}: {e}")
    
    def get_version_diff(
        self, 
        version_id1: str, 
        version_id2: str
    ) -> Dict[str, str]:
        """
        Get the differences between two versions using unified engine infrastructure.
        
        Args:
            version_id1: ID of the first version
            version_id2: ID of the second version
            
        Returns:
            Dict[str, str]: Dictionary of file paths to change types
                (added, modified, deleted, unchanged)
        """
        try:
            # Use common engine to compare snapshots
            changeset = self.compare_snapshots(version_id1, version_id2)
            
            # Convert to game-specific format
            diff = {}
            for change in changeset.changes:
                path_str = str(change.file_path)
                if change.change_type == ChangeType.ADDED:
                    diff[path_str] = "added"
                elif change.change_type == ChangeType.MODIFIED:
                    diff[path_str] = "modified"
                elif change.change_type == ChangeType.DELETED:
                    diff[path_str] = "deleted"
                else:
                    diff[path_str] = "unchanged"
            
            return diff
            
        except Exception as e:
            raise BackupSystemError(f"Failed to get version diff: {e}")
    
    def get_storage_stats(self) -> Dict[str, int]:
        """
        Get statistics about the backup storage using unified engine infrastructure.
        
        Returns:
            Dict[str, int]: Dictionary with storage statistics
        """
        try:
            # Use common engine storage stats
            storage_stats = super().get_storage_stats()
            
            # Convert to game-specific format for backward compatibility
            return {
                "total_files": storage_stats.total_files,
                "total_size": storage_stats.total_size,
                "compressed_size": storage_stats.compressed_size,
                "unique_chunks": storage_stats.unique_chunks,
                "deduplicated_chunks": storage_stats.deduplicated_chunks
            }
            
        except Exception as e:
            # Fallback to legacy implementation if needed
            return self.storage_manager.get_storage_size()
    
    def list_versions(self) -> List[ProjectVersion]:
        """
        List all available project versions.
        
        Returns:
            List[ProjectVersion]: List of project versions
        """
        try:
            # Get snapshots from common engine
            snapshots = self.list_snapshots()
            
            # Convert to ProjectVersion objects
            versions = []
            for snapshot in snapshots:
                # Try to get game-specific metadata from version tracker
                try:
                    project_version = self.version_tracker.get_version(snapshot.id)
                    versions.append(project_version)
                except:
                    # Fallback: convert from snapshot
                    name = snapshot.metadata.get("name", f"Snapshot {snapshot.id[:8]}")
                    version_type_str = snapshot.metadata.get("type", "development")
                    version_type = GameVersionType(version_type_str)
                    is_milestone = snapshot.metadata.get("is_milestone", False)
                    
                    project_version = ProjectVersion.from_common_snapshot_info(
                        snapshot=snapshot,
                        name=name,
                        version_type=version_type,
                        is_milestone=is_milestone
                    )
                    versions.append(project_version)
            
            return versions
            
        except Exception as e:
            raise BackupSystemError(f"Failed to list versions: {e}")
    
    def get_version(self, version_id: str) -> ProjectVersion:
        """
        Get a specific project version.
        
        Args:
            version_id: ID of the version to retrieve
            
        Returns:
            ProjectVersion: The requested version
        """
        try:
            # Try version tracker first
            return self.version_tracker.get_version(version_id)
        except:
            # Fallback: get from common engine and convert
            snapshot = self.get_snapshot_info(version_id)
            
            name = snapshot.metadata.get("name", f"Snapshot {snapshot.id[:8]}")
            version_type_str = snapshot.metadata.get("type", "development")
            version_type = GameVersionType(version_type_str)
            is_milestone = snapshot.metadata.get("is_milestone", False)
            
            return ProjectVersion.from_common_snapshot_info(
                snapshot=snapshot,
                name=name,
                version_type=version_type,
                is_milestone=is_milestone
            )


# Import chunker here to avoid circular imports
from gamevault.backup_engine.chunker import ChunkingStrategy, RollingHashChunker