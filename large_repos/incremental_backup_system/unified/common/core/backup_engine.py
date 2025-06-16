"""
Core backup engine for the unified backup system.
"""

import time
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Any, Iterator

from .chunking import create_chunker, ChunkingStrategy
from .config import ConfigManager, UnifiedBackupConfig
from .exceptions import BackupSystemError, SnapshotError, RestoreError
from .file_utils import scan_directory, get_file_info, ensure_directory, normalize_path
from .models import (
    FileInfo, SnapshotInfo, ChangeInfo, ChangeSet, ChangeType, 
    StorageStats
)
from .storage import ContentAddressedStorage, MetadataStorage


class BackupEngine(ABC):
    """Abstract base class for backup engines."""
    
    @abstractmethod
    def create_snapshot(self, source_path: Path, tags: Optional[Set[str]] = None) -> SnapshotInfo:
        """Create a new backup snapshot."""
        pass
        
    @abstractmethod
    def restore_snapshot(self, snapshot_id: str, target_path: Path, 
                        selective_files: Optional[List[Path]] = None) -> None:
        """Restore files from a snapshot."""
        pass
        
    @abstractmethod
    def list_snapshots(self) -> List[SnapshotInfo]:
        """List all available snapshots."""
        pass
        
    @abstractmethod
    def get_snapshot_info(self, snapshot_id: str) -> SnapshotInfo:
        """Get detailed information about a snapshot."""
        pass
        
    @abstractmethod
    def compare_snapshots(self, from_snapshot: str, to_snapshot: str) -> ChangeSet:
        """Compare two snapshots and return changes."""
        pass
        
    @abstractmethod  
    def delete_snapshot(self, snapshot_id: str) -> None:
        """Delete a snapshot and clean up storage."""
        pass


class UnifiedBackupEngine(BackupEngine):
    """Unified backup engine with chunking and deduplication."""
    
    def __init__(self, config: UnifiedBackupConfig):
        """
        Initialize unified backup engine.
        
        Args:
            config: Backup configuration
        """
        self.config = config
        self.storage = ContentAddressedStorage(
            config.backup_dir / "storage", 
            config
        )
        self.metadata_storage = MetadataStorage(
            config.backup_dir / "metadata"
        )
        self.chunker = create_chunker(
            config.chunking_strategy,
            config.chunking_config
        )
        
        # Ensure backup directory exists
        ensure_directory(config.backup_dir)
        
    def create_snapshot(self, source_path: Path, tags: Optional[Set[str]] = None) -> SnapshotInfo:
        """
        Create a new backup snapshot.
        
        Args:
            source_path: Path to directory or file to backup
            tags: Optional tags for the snapshot
            
        Returns:
            SnapshotInfo for the created snapshot
            
        Raises:
            SnapshotError: If snapshot creation fails
        """
        try:
            source_path = Path(source_path).resolve()
            if not source_path.exists():
                raise SnapshotError(f"Source path does not exist: {source_path}")
                
            # Generate snapshot ID
            snapshot_id = self._generate_snapshot_id()
            
            # Get parent snapshot for incremental backup
            parent_id = self._get_latest_snapshot_id(source_path)
            parent_files = self._get_snapshot_files(parent_id) if parent_id else {}
            
            # Scan files in source
            current_files = self._scan_source_files(source_path)
            
            # Calculate changes
            changes = self._calculate_changes(parent_files, current_files)
            
            # Store chunks for new/modified files
            stored_files = self._store_file_chunks(current_files, changes)
            
            # Create snapshot info
            snapshot = SnapshotInfo(
                id=snapshot_id,
                timestamp=datetime.now(),
                source_path=source_path,
                parent_id=parent_id,
                files=list(stored_files.values()),
                changes=changes,
                tags=tags or set()
            )
            
            # Store snapshot metadata
            self._store_snapshot_metadata(snapshot)
            
            return snapshot
            
        except Exception as e:
            raise SnapshotError(f"Failed to create snapshot: {e}")
            
    def restore_snapshot(self, snapshot_id: str, target_path: Path, 
                        selective_files: Optional[List[Path]] = None) -> None:
        """
        Restore files from a snapshot.
        
        Args:
            snapshot_id: ID of snapshot to restore
            target_path: Directory to restore files to
            selective_files: Optional list of specific files to restore
            
        Raises:
            RestoreError: If restoration fails
        """
        try:
            snapshot = self.get_snapshot_info(snapshot_id)
            target_path = Path(target_path)
            
            # Ensure target directory exists
            ensure_directory(target_path)
            
            # Filter files if selective restore
            files_to_restore = snapshot.files
            if selective_files:
                selective_paths = {normalize_path(p) for p in selective_files}
                files_to_restore = [
                    f for f in snapshot.files 
                    if normalize_path(f.path, snapshot.source_path) in selective_paths
                ]
                
            # Restore each file
            for file_info in files_to_restore:
                self._restore_file(file_info, target_path, snapshot.source_path)
                
        except Exception as e:
            raise RestoreError(f"Failed to restore snapshot {snapshot_id}: {e}")
            
    def list_snapshots(self) -> List[SnapshotInfo]:
        """
        List all available snapshots.
        
        Returns:
            List of SnapshotInfo objects sorted by timestamp
        """
        try:
            snapshot_ids = self.metadata_storage.list_snapshots()
            snapshots = []
            
            for snapshot_id in snapshot_ids:
                try:
                    snapshot = self.get_snapshot_info(snapshot_id)
                    snapshots.append(snapshot)
                except Exception:
                    # Skip corrupted snapshots
                    continue
                    
            # Sort by timestamp (newest first)
            snapshots.sort(key=lambda s: s.timestamp, reverse=True)
            return snapshots
            
        except Exception as e:
            raise BackupSystemError(f"Failed to list snapshots: {e}")
            
    def get_snapshot_info(self, snapshot_id: str) -> SnapshotInfo:
        """
        Get detailed information about a snapshot.
        
        Args:
            snapshot_id: ID of the snapshot
            
        Returns:
            SnapshotInfo object
            
        Raises:
            SnapshotError: If snapshot not found or corrupted
        """
        try:
            metadata = self.metadata_storage.retrieve_snapshot_metadata(snapshot_id)
            
            # Convert metadata back to SnapshotInfo
            return SnapshotInfo(
                id=metadata["id"],
                timestamp=datetime.fromisoformat(metadata["timestamp"]),
                source_path=Path(metadata["source_path"]),
                parent_id=metadata.get("parent_id"),
                files=[FileInfo(**f) for f in metadata["files"]],
                changes=[self._dict_to_change_info(c) for c in metadata.get("changes", [])],
                tags=set(metadata.get("tags", [])),
                metadata=metadata.get("metadata", {})
            )
            
        except Exception as e:
            raise SnapshotError(f"Failed to get snapshot info {snapshot_id}: {e}")
            
    def compare_snapshots(self, from_snapshot: str, to_snapshot: str) -> ChangeSet:
        """
        Compare two snapshots and return changes.
        
        Args:
            from_snapshot: ID of the source snapshot
            to_snapshot: ID of the target snapshot
            
        Returns:
            ChangeSet describing the differences
            
        Raises:
            BackupSystemError: If comparison fails
        """
        try:
            from_snap = self.get_snapshot_info(from_snapshot)
            to_snap = self.get_snapshot_info(to_snapshot)
            
            from_files = {f.path: f for f in from_snap.files}
            to_files = {f.path: f for f in to_snap.files}
            
            changes = []
            
            # Find added and modified files
            for path, file_info in to_files.items():
                if path not in from_files:
                    changes.append(ChangeInfo(
                        file_path=path,
                        change_type=ChangeType.ADDED,
                        new_file=file_info
                    ))
                elif from_files[path].hash != file_info.hash:
                    changes.append(ChangeInfo(
                        file_path=path,
                        change_type=ChangeType.MODIFIED,
                        old_file=from_files[path],
                        new_file=file_info
                    ))
                    
            # Find deleted files
            for path, file_info in from_files.items():
                if path not in to_files:
                    changes.append(ChangeInfo(
                        file_path=path,
                        change_type=ChangeType.DELETED,
                        old_file=file_info
                    ))
                    
            return ChangeSet(
                from_snapshot=from_snapshot,
                to_snapshot=to_snapshot,
                changes=changes
            )
            
        except Exception as e:
            raise BackupSystemError(f"Failed to compare snapshots: {e}")
            
    def delete_snapshot(self, snapshot_id: str) -> None:
        """
        Delete a snapshot and clean up storage.
        
        Args:
            snapshot_id: ID of snapshot to delete
            
        Raises:
            SnapshotError: If deletion fails
        """
        try:
            snapshot = self.get_snapshot_info(snapshot_id)
            
            # Remove chunk references
            for file_info in snapshot.files:
                for chunk_hash in file_info.chunk_hashes:
                    self.storage.delete_chunk(chunk_hash)
                    
            # Delete snapshot metadata
            self.metadata_storage.delete_snapshot_metadata(snapshot_id)
            
        except Exception as e:
            raise SnapshotError(f"Failed to delete snapshot {snapshot_id}: {e}")
            
    def get_storage_stats(self) -> StorageStats:
        """
        Get storage statistics.
        
        Returns:
            StorageStats object
        """
        return self.storage.get_storage_stats()
        
    def cleanup_storage(self) -> int:
        """
        Clean up orphaned chunks and optimize storage.
        
        Returns:
            Number of chunks cleaned up
        """
        return self.storage.cleanup_orphaned_chunks()
        
    def verify_snapshot_integrity(self, snapshot_id: str) -> bool:
        """
        Verify integrity of a snapshot.
        
        Args:
            snapshot_id: ID of snapshot to verify
            
        Returns:
            True if snapshot is intact
        """
        try:
            snapshot = self.get_snapshot_info(snapshot_id)
            
            # Verify all chunks exist
            for file_info in snapshot.files:
                for chunk_hash in file_info.chunk_hashes:
                    if not self.storage.chunk_exists(chunk_hash):
                        return False
                        
            return True
            
        except Exception:
            return False
            
    def _generate_snapshot_id(self) -> str:
        """Generate unique snapshot ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"snapshot_{timestamp}_{int(time.time() * 1000000) % 1000000:06d}"
        
    def _get_latest_snapshot_id(self, source_path: Path) -> Optional[str]:
        """Get ID of latest snapshot for source path."""
        try:
            snapshots = self.list_snapshots()
            for snapshot in snapshots:
                if snapshot.source_path == source_path:
                    return snapshot.id
            return None
        except Exception:
            return None
            
    def _get_snapshot_files(self, snapshot_id: str) -> Dict[Path, FileInfo]:
        """Get files from a snapshot as a path->FileInfo mapping."""
        try:
            snapshot = self.get_snapshot_info(snapshot_id)
            return {f.path: f for f in snapshot.files}
        except Exception:
            return {}
            
    def _scan_source_files(self, source_path: Path) -> Dict[Path, FileInfo]:
        """Scan source path and return file information."""
        files = {}
        
        if source_path.is_file():
            # Single file backup
            try:
                file_info = get_file_info(source_path, self.config.hash_algorithm)
                files[source_path] = file_info
            except Exception:
                pass
        else:
            # Directory backup
            for file_path in scan_directory(
                source_path,
                ignore_patterns=self.config.ignore_patterns,
                follow_symlinks=self.config.follow_symlinks,
                include_hidden=self.config.include_hidden_files
            ):
                try:
                    file_info = get_file_info(file_path, self.config.hash_algorithm)
                    files[file_path] = file_info
                except Exception:
                    # Skip files that can't be accessed
                    continue
                    
        return files
        
    def _calculate_changes(self, old_files: Dict[Path, FileInfo], 
                         new_files: Dict[Path, FileInfo]) -> List[ChangeInfo]:
        """Calculate changes between file sets."""
        changes = []
        
        # Find added and modified files
        for path, new_file in new_files.items():
            if path not in old_files:
                changes.append(ChangeInfo(
                    file_path=path,
                    change_type=ChangeType.ADDED,
                    new_file=new_file
                ))
            elif old_files[path].hash != new_file.hash:
                changes.append(ChangeInfo(
                    file_path=path,
                    change_type=ChangeType.MODIFIED,
                    old_file=old_files[path],
                    new_file=new_file
                ))
                
        # Find deleted files
        for path, old_file in old_files.items():
            if path not in new_files:
                changes.append(ChangeInfo(
                    file_path=path,
                    change_type=ChangeType.DELETED,
                    old_file=old_file
                ))
                
        return changes
        
    def _store_file_chunks(self, files: Dict[Path, FileInfo], 
                          changes: List[ChangeInfo]) -> Dict[Path, FileInfo]:
        """Store chunks for files that need backing up."""
        stored_files = {}
        
        # Determine which files need chunk storage
        files_to_store = set()
        for change in changes:
            if change.change_type in (ChangeType.ADDED, ChangeType.MODIFIED):
                files_to_store.add(change.file_path)
                
        # Store chunks for each file
        for file_path, file_info in files.items():
            if file_path in files_to_store:
                # Read file and create chunks
                try:
                    with open(file_path, 'rb') as f:
                        file_data = f.read()
                        
                    chunks = self.chunker.chunk_data(file_data)
                    
                    # Store chunks
                    self.storage.store_file_chunks(chunks, file_data)
                    
                    # Update file info with chunk information
                    file_info.chunks = chunks
                    file_info.chunk_hashes = [c.hash for c in chunks]
                    
                except Exception:
                    # Skip files that can't be read
                    continue
                    
            stored_files[file_path] = file_info
            
        return stored_files
        
    def _restore_file(self, file_info: FileInfo, target_path: Path, source_base: Path) -> None:
        """Restore a single file from chunks."""
        # Calculate relative path from source base
        try:
            relative_path = file_info.path.relative_to(source_base)
        except ValueError:
            # Path is not relative to source base, use name only
            relative_path = file_info.path.name
            
        # Determine target file path
        target_file_path = target_path / relative_path
        
        # Ensure target directory exists
        ensure_directory(target_file_path.parent)
        
        # Reconstruct file from chunks
        if file_info.chunks:
            file_data = self.storage.retrieve_file_from_chunks(file_info.chunks)
        else:
            # Fallback: try to reconstruct from chunk hashes
            total_data = bytearray()
            for chunk_hash in file_info.chunk_hashes:
                chunk_data = self.storage.retrieve_chunk(chunk_hash)
                total_data.extend(chunk_data)
            file_data = bytes(total_data)
            
        # Write file
        with open(target_file_path, 'wb') as f:
            f.write(file_data)
            
        # Preserve modification time
        import os
        os.utime(target_file_path, (file_info.modified_time.timestamp(), 
                                   file_info.modified_time.timestamp()))
                                   
    def _store_snapshot_metadata(self, snapshot: SnapshotInfo) -> None:
        """Store snapshot metadata."""
        metadata = {
            "id": snapshot.id,
            "timestamp": snapshot.timestamp.isoformat(),
            "source_path": str(snapshot.source_path),
            "parent_id": snapshot.parent_id,
            "files": [self._file_info_to_dict(f) for f in snapshot.files],
            "changes": [self._change_info_to_dict(c) for c in snapshot.changes],
            "tags": list(snapshot.tags),
            "metadata": snapshot.metadata
        }
        
        self.metadata_storage.store_snapshot_metadata(snapshot.id, metadata)
        
    def _file_info_to_dict(self, file_info: FileInfo) -> Dict[str, Any]:
        """Convert FileInfo to dictionary."""
        return {
            "path": str(file_info.path),
            "size": file_info.size,
            "hash": file_info.hash,
            "modified_time": file_info.modified_time.isoformat(),
            "file_type": file_info.file_type.value,
            "content_type": file_info.content_type,
            "chunk_hashes": file_info.chunk_hashes,
            "chunks": [
                {
                    "hash": c.hash,
                    "size": c.size,
                    "offset": c.offset,
                    "compressed_size": c.compressed_size
                } for c in file_info.chunks
            ],
            "metadata": file_info.metadata
        }
        
    def _change_info_to_dict(self, change_info: ChangeInfo) -> Dict[str, Any]:
        """Convert ChangeInfo to dictionary."""
        return {
            "file_path": str(change_info.file_path),
            "change_type": change_info.change_type.value,
            "old_file": self._file_info_to_dict(change_info.old_file) if change_info.old_file else None,
            "new_file": self._file_info_to_dict(change_info.new_file) if change_info.new_file else None
        }
        
    def _dict_to_change_info(self, change_dict: Dict[str, Any]) -> ChangeInfo:
        """Convert dictionary to ChangeInfo."""
        return ChangeInfo(
            file_path=Path(change_dict["file_path"]),
            change_type=ChangeType(change_dict["change_type"]),
            old_file=self._dict_to_file_info(change_dict["old_file"]) if change_dict.get("old_file") else None,
            new_file=self._dict_to_file_info(change_dict["new_file"]) if change_dict.get("new_file") else None
        )
        
    def _dict_to_file_info(self, file_dict: Dict[str, Any]) -> FileInfo:
        """Convert dictionary to FileInfo."""
        from .models import FileType, ChunkInfo
        
        chunks = []
        for chunk_dict in file_dict.get("chunks", []):
            chunks.append(ChunkInfo(
                hash=chunk_dict["hash"],
                size=chunk_dict["size"],
                offset=chunk_dict["offset"],
                compressed_size=chunk_dict.get("compressed_size")
            ))
            
        return FileInfo(
            path=Path(file_dict["path"]),
            size=file_dict["size"],
            hash=file_dict["hash"],
            modified_time=datetime.fromisoformat(file_dict["modified_time"]),
            file_type=FileType(file_dict["file_type"]),
            content_type=file_dict.get("content_type", ""),
            chunk_hashes=file_dict.get("chunk_hashes", []),
            chunks=chunks,
            metadata=file_dict.get("metadata", {})
        )