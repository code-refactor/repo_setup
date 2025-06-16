"""
Incremental Backup Engine for artistic content.

This module provides the core functionality for detecting changes, creating
deltas, and maintaining version history of creative files.
"""

import json
import os
import shutil
import tempfile
import time
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import numpy as np
from pydantic import BaseModel, Field

from common.core.backup_engine import UnifiedBackupEngine
from common.core.config import UnifiedBackupConfig
from common.core.models import SnapshotInfo, FileInfo, ChangeInfo, ChangeType
from common.core.exceptions import SnapshotError, RestoreError, BackupSystemError
from creative_vault.interfaces import BackupEngine
from creative_vault.utils import (create_timestamp, create_unique_id, 
                                load_json, save_json)


# SnapshotInfo is now imported from common.core.models
# Keeping a compatibility alias for existing code
CreativeSnapshotInfo = SnapshotInfo


class DeltaBackupEngine(UnifiedBackupEngine):
    """Implementation of the incremental backup engine using delta storage.
    
    This class extends the unified backup engine with creative-specific functionality
    while maintaining backward compatibility with the existing interface.
    """
    
    def __init__(self, config: Optional[Union[UnifiedBackupConfig, Dict[str, Any]]] = None):
        """Initialize the backup engine.
        
        Args:
            config: Optional configuration for the backup engine
        """
        # Convert old config format to new format for backward compatibility
        if config is None:
            unified_config = UnifiedBackupConfig(backup_dir=Path("backups"))
        elif isinstance(config, dict):
            # Handle old BackupConfig dict format
            backup_dir = config.get('repository_path', Path("backups"))
            unified_config = UnifiedBackupConfig(
                backup_dir=backup_dir,
                compression_level=config.get('compression_level', 3),
                enable_deduplication=config.get('deduplication_enabled', True)
            )
        elif hasattr(config, 'repository_path'):
            # Handle old BackupConfig object
            unified_config = UnifiedBackupConfig(
                backup_dir=config.repository_path,
                compression_level=getattr(config, 'compression_level', 3),
                enable_deduplication=getattr(config, 'deduplication_enabled', True)
            )
        else:
            unified_config = config
            
        # Initialize the parent unified backup engine
        super().__init__(unified_config)
        
        # Maintain backward compatibility properties
        self._repository_path = self.config.backup_dir
        self._snapshots_path = self._repository_path / "snapshots"
        self._objects_path = self._repository_path / "objects"
        self._metadata_path = self._repository_path / "metadata"
        
        # Cache of file hashes to avoid recalculating
        self._hash_cache: Dict[Path, str] = {}
        
        # Cache of file metadata
        self._file_metadata_cache: Dict[Path, Dict[str, Any]] = {}
    
    def initialize_repository(self, root_path: Path) -> bool:
        """Initialize a new backup repository at the specified path.
        
        Args:
            root_path: Path where the backup repository will be created
            
        Returns:
            bool: True if initialization was successful
        """
        try:
            # Update repository path in config and reinitialize storage
            old_backup_dir = self.config.backup_dir
            self.config.backup_dir = root_path
            
            # Update internal paths
            self._repository_path = root_path
            self._snapshots_path = self._repository_path / "snapshots"
            self._objects_path = self._repository_path / "objects"
            self._metadata_path = self._repository_path / "metadata"
            
            # Reinitialize storage with new path
            from common.core.storage import ContentAddressedStorage, MetadataStorage
            self.storage = ContentAddressedStorage(
                self.config.backup_dir / "storage", 
                self.config
            )
            self.metadata_storage = MetadataStorage(
                self.config.backup_dir / "metadata"
            )
            
            # Create directory structure (legacy compatibility)
            self._snapshots_path.mkdir(parents=True, exist_ok=True)
            self._objects_path.mkdir(parents=True, exist_ok=True)
            self._metadata_path.mkdir(parents=True, exist_ok=True)
            
            # Create repository metadata
            repo_metadata = {
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "config": self.config.dict(),
            }
            save_json(repo_metadata, self._repository_path / "repository.json")
            
            return True
        except Exception as e:
            print(f"Failed to initialize repository: {e}")
            return False
    
    def create_snapshot(self, source_path: Path, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Create a new snapshot of the source directory.
        
        Args:
            source_path: Path to the directory to backup
            metadata: Optional metadata to store with the snapshot
            
        Returns:
            str: Unique ID of the created snapshot
        """
        try:
            # Use the parent's create_snapshot method for core functionality
            tags = set()
            if metadata:
                tags = set(metadata.get('tags', []))
                
            snapshot_info = super().create_snapshot(source_path, tags)
            
            # Add creative-specific metadata and legacy compatibility
            snapshot_id = snapshot_info.id
            snapshot_path = self._snapshots_path / snapshot_id
            snapshot_path.mkdir(parents=True, exist_ok=True)
            
            # Calculate creative-specific statistics
            new_files = []
            modified_files = []
            deleted_files = []
            
            for change in snapshot_info.changes:
                if change.change_type == ChangeType.ADDED:
                    new_files.append(str(change.file_path))
                elif change.change_type == ChangeType.MODIFIED:
                    modified_files.append(str(change.file_path))
                elif change.change_type == ChangeType.DELETED:
                    deleted_files.append(str(change.file_path))
            
            # Create legacy-compatible snapshot info
            legacy_snapshot_info = {
                "id": snapshot_id,
                "timestamp": snapshot_info.timestamp.isoformat(),
                "source_path": str(snapshot_info.source_path),
                "files_count": len(snapshot_info.files),
                "total_size": sum(f.size for f in snapshot_info.files),
                "new_files": new_files,
                "modified_files": modified_files,
                "deleted_files": deleted_files,
                "metadata": metadata or {}
            }
            
            # Save legacy snapshot metadata for backward compatibility
            save_json(legacy_snapshot_info, snapshot_path / "info.json")
            
            # Save file list in legacy format
            file_list = [{
                "path": str(f.path),
                "size": f.size,
                "modified_time": f.modified_time.timestamp(),
                "hash": f.hash,
                "content_type": f.content_type,
                "metadata": f.metadata
            } for f in snapshot_info.files]
            save_json(file_list, snapshot_path / "files.json")
            
            # Create legacy manifest
            manifest = {
                "id": snapshot_id,
                "timestamp": snapshot_info.timestamp.isoformat(),
                "files": {}
            }
            
            for file_info in snapshot_info.files:
                manifest["files"][str(file_info.path)] = {
                    "hash": file_info.hash,
                    "size": file_info.size,
                    "modified_time": file_info.modified_time.timestamp(),
                    "content_type": file_info.content_type
                }
            
            # Save the manifest
            save_json(manifest, snapshot_path / "manifest.json")
            
            return snapshot_id
            
        except Exception as e:
            raise SnapshotError(f"Failed to create creative snapshot: {e}")
    
    def restore_snapshot(self, snapshot_id: str, target_path: Path) -> bool:
        """Restore a specific snapshot to the target path.
        
        Args:
            snapshot_id: ID of the snapshot to restore
            target_path: Path where the snapshot will be restored
            
        Returns:
            bool: True if restore was successful
        """
        try:
            # Use the parent's restore method for core functionality
            super().restore_snapshot(snapshot_id, target_path)
            return True
            
        except RestoreError as e:
            print(f"Error restoring snapshot {snapshot_id}: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error restoring snapshot {snapshot_id}: {e}")
            return False
    
    def get_snapshot_info(self, snapshot_id: str) -> Dict[str, Any]:
        """Get metadata about a specific snapshot.
        
        Args:
            snapshot_id: ID of the snapshot
            
        Returns:
            Dict containing snapshot metadata
        """
        # Try legacy format first for backward compatibility
        snapshot_path = self._snapshots_path / snapshot_id
        info_path = snapshot_path / "info.json"
        
        if info_path.exists():
            return load_json(info_path)
        
        # Fall back to unified format
        try:
            snapshot_info = super().get_snapshot_info(snapshot_id)
            
            # Convert to legacy format
            new_files = []
            modified_files = []
            deleted_files = []
            
            for change in snapshot_info.changes:
                if change.change_type == ChangeType.ADDED:
                    new_files.append(str(change.file_path))
                elif change.change_type == ChangeType.MODIFIED:
                    modified_files.append(str(change.file_path))
                elif change.change_type == ChangeType.DELETED:
                    deleted_files.append(str(change.file_path))
            
            return {
                "id": snapshot_info.id,
                "timestamp": snapshot_info.timestamp.isoformat(),
                "source_path": str(snapshot_info.source_path),
                "files_count": len(snapshot_info.files),
                "total_size": sum(f.size for f in snapshot_info.files),
                "new_files": new_files,
                "modified_files": modified_files,
                "deleted_files": deleted_files,
                "metadata": snapshot_info.metadata
            }
            
        except Exception as e:
            raise ValueError(f"Snapshot {snapshot_id} does not exist or is corrupted: {e}")
    
    def list_snapshots(self, filter_criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """List all snapshots matching the filter criteria.
        
        Args:
            filter_criteria: Optional criteria to filter snapshots
            
        Returns:
            List of dictionaries containing snapshot metadata
        """
        result = []
        
        # Check for legacy snapshots first
        if self._snapshots_path.exists():
            for snapshot_dir in self._snapshots_path.iterdir():
                if not snapshot_dir.is_dir():
                    continue
                
                info_path = snapshot_dir / "info.json"
                if not info_path.exists():
                    continue
                
                try:
                    info = load_json(info_path)
                    
                    # Apply filters if provided
                    if filter_criteria:
                        match = True
                        for key, value in filter_criteria.items():
                            if key not in info or info[key] != value:
                                match = False
                                break
                        
                        if not match:
                            continue
                    
                    result.append(info)
                except Exception as e:
                    print(f"Error reading snapshot info {snapshot_dir.name}: {e}")
        
        # Add unified snapshots
        try:
            unified_snapshots = super().list_snapshots()
            for snapshot_info in unified_snapshots:
                # Convert to legacy format
                new_files = []
                modified_files = []
                deleted_files = []
                
                for change in snapshot_info.changes:
                    if change.change_type == ChangeType.ADDED:
                        new_files.append(str(change.file_path))
                    elif change.change_type == ChangeType.MODIFIED:
                        modified_files.append(str(change.file_path))
                    elif change.change_type == ChangeType.DELETED:
                        deleted_files.append(str(change.file_path))
                
                legacy_info = {
                    "id": snapshot_info.id,
                    "timestamp": snapshot_info.timestamp.isoformat(),
                    "source_path": str(snapshot_info.source_path),
                    "files_count": len(snapshot_info.files),
                    "total_size": sum(f.size for f in snapshot_info.files),
                    "new_files": new_files,
                    "modified_files": modified_files,
                    "deleted_files": deleted_files,
                    "metadata": snapshot_info.metadata
                }
                
                # Apply filters if provided
                if filter_criteria:
                    match = True
                    for key, value in filter_criteria.items():
                        if key not in legacy_info or legacy_info[key] != value:
                            match = False
                            break
                    
                    if not match:
                        continue
                
                # Avoid duplicates
                if not any(existing['id'] == legacy_info['id'] for existing in result):
                    result.append(legacy_info)
                    
        except Exception as e:
            print(f"Error reading unified snapshots: {e}")
        
        # Sort by timestamp
        result.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return result
    
    def _get_latest_snapshot(self) -> Optional[str]:
        """Get the ID of the most recent snapshot.
        
        Returns:
            str: The ID of the most recent snapshot, or None if no snapshots exist
        """
        snapshots = self.list_snapshots()
        if not snapshots:
            return None
        
        return snapshots[0]["id"]
    
    # Legacy _store_file method removed - now handled by parent UnifiedBackupEngine
    
    def _get_object_path(self, file_hash: str) -> Path:
        """Get the path where an object file should be stored (legacy compatibility).
        
        Args:
            file_hash: The hash of the file
            
        Returns:
            Path: The path in the objects storage
        """
        return self._objects_path / file_hash[:2] / file_hash[2:4] / file_hash
        
    # Additional creative-specific methods
    def get_creative_stats(self, snapshot_id: str) -> Dict[str, Any]:
        """Get creative-specific statistics for a snapshot.
        
        Args:
            snapshot_id: ID of the snapshot
            
        Returns:
            Dictionary with creative statistics
        """
        try:
            snapshot_info = super().get_snapshot_info(snapshot_id)
            
            # Count file types
            file_type_counts = {}
            for file_info in snapshot_info.files:
                file_type = file_info.file_type.value
                file_type_counts[file_type] = file_type_counts.get(file_type, 0) + 1
            
            # Calculate size by type
            size_by_type = {}
            for file_info in snapshot_info.files:
                file_type = file_info.file_type.value
                size_by_type[file_type] = size_by_type.get(file_type, 0) + file_info.size
            
            return {
                "file_type_counts": file_type_counts,
                "size_by_type": size_by_type,
                "total_files": len(snapshot_info.files),
                "total_size": sum(f.size for f in snapshot_info.files),
                "snapshot_timestamp": snapshot_info.timestamp.isoformat(),
                "change_summary": {
                    "added": len([c for c in snapshot_info.changes if c.change_type == ChangeType.ADDED]),
                    "modified": len([c for c in snapshot_info.changes if c.change_type == ChangeType.MODIFIED]),
                    "deleted": len([c for c in snapshot_info.changes if c.change_type == ChangeType.DELETED])
                }
            }
            
        except Exception as e:
            raise BackupSystemError(f"Failed to get creative stats for snapshot {snapshot_id}: {e}")
            
    def compare_creative_snapshots(self, from_snapshot: str, to_snapshot: str) -> Dict[str, Any]:
        """Compare two snapshots with creative-specific analysis.
        
        Args:
            from_snapshot: ID of the source snapshot
            to_snapshot: ID of the target snapshot
            
        Returns:
            Dictionary with creative comparison analysis
        """
        try:
            change_set = super().compare_snapshots(from_snapshot, to_snapshot)
            
            # Analyze changes by file type
            changes_by_type = {}
            for change in change_set.changes:
                if change.new_file:
                    file_type = change.new_file.file_type.value
                elif change.old_file:
                    file_type = change.old_file.file_type.value
                else:
                    file_type = "unknown"
                    
                if file_type not in changes_by_type:
                    changes_by_type[file_type] = {
                        "added": 0,
                        "modified": 0,
                        "deleted": 0
                    }
                    
                changes_by_type[file_type][change.change_type.value] += 1
            
            return {
                "summary": change_set.summary,
                "changes_by_type": changes_by_type,
                "total_changes": len(change_set.changes),
                "from_snapshot": from_snapshot,
                "to_snapshot": to_snapshot
            }
            
        except Exception as e:
            raise BackupSystemError(f"Failed to compare creative snapshots: {e}")