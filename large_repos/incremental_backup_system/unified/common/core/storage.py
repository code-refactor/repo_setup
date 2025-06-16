"""
Content-addressed storage system for the unified backup system.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from datetime import datetime

from .compression import compress_data, decompress_data, compress_with_fallback
from .exceptions import StorageError, CorruptedDataError
from .file_utils import ensure_directory, safe_file_copy
from .hashing import calculate_data_hash, verify_file_hash
from .models import ChunkInfo, StorageStats, BackupConfig


class ContentAddressedStorage:
    """Content-addressed storage system with compression and deduplication."""
    
    def __init__(self, storage_path: Path, config: BackupConfig):
        """
        Initialize content-addressed storage.
        
        Args:
            storage_path: Base directory for storage
            config: Backup configuration
        """
        self.storage_path = Path(storage_path)
        self.config = config
        self.chunks_dir = self.storage_path / "chunks"
        self.metadata_dir = self.storage_path / "metadata"
        self.refs_dir = self.storage_path / "refs"
        
        # Ensure directories exist
        ensure_directory(self.chunks_dir)
        ensure_directory(self.metadata_dir)
        ensure_directory(self.refs_dir)
        
        # Reference counting for chunks
        self._ref_counts: Dict[str, int] = {}
        self._load_ref_counts()
        
    def store_chunk(self, chunk_hash: str, data: bytes) -> None:
        """
        Store chunk data with content-addressed naming.
        
        Args:
            chunk_hash: Hash of the chunk data
            data: Chunk data to store
            
        Raises:
            StorageError: If storage fails
        """
        try:
            # Verify hash matches data
            actual_hash = calculate_data_hash(data, self.config.hash_algorithm)
            if actual_hash != chunk_hash:
                raise StorageError(f"Hash mismatch: expected {chunk_hash}, got {actual_hash}")
                
            chunk_path = self._get_chunk_path(chunk_hash)
            
            # Skip if chunk already exists
            if chunk_path.exists():
                self._increment_ref_count(chunk_hash)
                return
                
            # Ensure chunk directory exists
            ensure_directory(chunk_path.parent)
            
            # Compress data if beneficial
            if self.config.enable_compression and len(data) > 1024:
                compressed_data, algorithm_used = compress_with_fallback(
                    data, "zstd", "zlib", self.config.compression_level
                )
                
                # Store compression metadata
                chunk_metadata = {
                    "original_size": len(data),
                    "compressed_size": len(compressed_data),
                    "compression_algorithm": algorithm_used,
                    "hash_algorithm": self.config.hash_algorithm,
                    "stored_at": datetime.now().isoformat()
                }
                
                # Store compressed data
                chunk_path.write_bytes(compressed_data)
                
                # Store metadata
                metadata_path = self._get_metadata_path(chunk_hash)
                with open(metadata_path, 'w') as f:
                    json.dump(chunk_metadata, f)
            else:
                # Store uncompressed
                chunk_path.write_bytes(data)
                
                # Store minimal metadata
                chunk_metadata = {
                    "original_size": len(data),
                    "compressed_size": len(data),
                    "compression_algorithm": "none",
                    "hash_algorithm": self.config.hash_algorithm,
                    "stored_at": datetime.now().isoformat()
                }
                
                metadata_path = self._get_metadata_path(chunk_hash)
                with open(metadata_path, 'w') as f:
                    json.dump(chunk_metadata, f)
                    
            self._increment_ref_count(chunk_hash)
            
        except Exception as e:
            raise StorageError(f"Failed to store chunk {chunk_hash}: {e}")
            
    def retrieve_chunk(self, chunk_hash: str) -> bytes:
        """
        Retrieve chunk data by hash.
        
        Args:
            chunk_hash: Hash of the chunk to retrieve
            
        Returns:
            Chunk data
            
        Raises:
            StorageError: If retrieval fails
        """
        try:
            chunk_path = self._get_chunk_path(chunk_hash)
            
            if not chunk_path.exists():
                raise StorageError(f"Chunk not found: {chunk_hash}")
                
            # Load metadata
            metadata_path = self._get_metadata_path(chunk_hash)
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                    
                compression_algorithm = metadata.get("compression_algorithm", "none")
                original_size = metadata.get("original_size", 0)
            else:
                # No metadata, assume uncompressed
                compression_algorithm = "none"
                original_size = chunk_path.stat().st_size
                
            # Read and decompress data
            compressed_data = chunk_path.read_bytes()
            
            if compression_algorithm != "none":
                data = decompress_data(compressed_data, compression_algorithm)
            else:
                data = compressed_data
                
            # Verify size if available
            if original_size > 0 and len(data) != original_size:
                raise CorruptedDataError(f"Size mismatch for chunk {chunk_hash}")
                
            # Verify hash
            actual_hash = calculate_data_hash(data, self.config.hash_algorithm)
            if actual_hash != chunk_hash:
                raise CorruptedDataError(f"Hash mismatch for chunk {chunk_hash}")
                
            return data
            
        except Exception as e:
            if isinstance(e, (StorageError, CorruptedDataError)):
                raise
            raise StorageError(f"Failed to retrieve chunk {chunk_hash}: {e}")
            
    def chunk_exists(self, chunk_hash: str) -> bool:
        """
        Check if chunk exists in storage.
        
        Args:
            chunk_hash: Hash of the chunk
            
        Returns:
            True if chunk exists
        """
        chunk_path = self._get_chunk_path(chunk_hash)
        return chunk_path.exists()
        
    def store_file_chunks(self, chunks: List[ChunkInfo], file_data: bytes) -> None:
        """
        Store all chunks for a file.
        
        Args:
            chunks: List of chunk information
            file_data: Complete file data
            
        Raises:
            StorageError: If storage fails
        """
        for chunk_info in chunks:
            chunk_start = chunk_info.offset
            chunk_end = chunk_start + chunk_info.size
            chunk_data = file_data[chunk_start:chunk_end]
            
            self.store_chunk(chunk_info.hash, chunk_data)
            
    def retrieve_file_from_chunks(self, chunks: List[ChunkInfo]) -> bytes:
        """
        Reconstruct file data from chunks.
        
        Args:
            chunks: List of chunk information in order
            
        Returns:
            Complete file data
            
        Raises:
            StorageError: If reconstruction fails
        """
        file_data = bytearray()
        
        for chunk_info in chunks:
            chunk_data = self.retrieve_chunk(chunk_info.hash)
            
            # Verify chunk size
            if len(chunk_data) != chunk_info.size:
                raise StorageError(f"Chunk size mismatch: expected {chunk_info.size}, got {len(chunk_data)}")
                
            file_data.extend(chunk_data)
            
        return bytes(file_data)
        
    def delete_chunk(self, chunk_hash: str) -> None:
        """
        Delete chunk from storage (with reference counting).
        
        Args:
            chunk_hash: Hash of the chunk to delete
        """
        self._decrement_ref_count(chunk_hash)
        
        # Only physically delete if no more references
        if self._get_ref_count(chunk_hash) <= 0:
            chunk_path = self._get_chunk_path(chunk_hash)
            metadata_path = self._get_metadata_path(chunk_hash)
            
            try:
                if chunk_path.exists():
                    chunk_path.unlink()
                if metadata_path.exists():
                    metadata_path.unlink()
                    
                # Remove from ref counts
                self._ref_counts.pop(chunk_hash, None)
                self._save_ref_counts()
                
            except Exception as e:
                raise StorageError(f"Failed to delete chunk {chunk_hash}: {e}")
                
    def get_storage_stats(self) -> StorageStats:
        """
        Get storage statistics.
        
        Returns:
            StorageStats object with current statistics
        """
        stats = StorageStats()
        
        try:
            # Count chunks and calculate sizes
            for chunk_dir in self.chunks_dir.iterdir():
                if not chunk_dir.is_dir():
                    continue
                    
                for subdir in chunk_dir.iterdir():
                    if not subdir.is_dir():
                        continue
                        
                    for chunk_file in subdir.iterdir():
                        if chunk_file.is_file():
                            chunk_hash = chunk_file.name
                            
                            # Get metadata
                            metadata_path = self._get_metadata_path(chunk_hash)
                            if metadata_path.exists():
                                with open(metadata_path, 'r') as f:
                                    metadata = json.load(f)
                                    
                                original_size = metadata.get("original_size", 0)
                                compressed_size = metadata.get("compressed_size", chunk_file.stat().st_size)
                                
                                stats.total_size += original_size
                                stats.compressed_size += compressed_size
                                
                            ref_count = self._get_ref_count(chunk_hash)
                            if ref_count > 1:
                                stats.deduplicated_chunks += ref_count - 1
                                
                            stats.unique_chunks += 1
                            
            # Calculate ratios
            if stats.total_size > 0:
                stats.compression_ratio = stats.compressed_size / stats.total_size
                
            total_chunk_refs = stats.unique_chunks + stats.deduplicated_chunks
            if total_chunk_refs > 0:
                stats.deduplication_ratio = stats.deduplicated_chunks / total_chunk_refs
                
        except Exception:
            # Return partial stats on error
            pass
            
        return stats
        
    def cleanup_orphaned_chunks(self) -> int:
        """
        Remove chunks with zero references.
        
        Returns:
            Number of chunks cleaned up
        """
        cleaned_up = 0
        
        try:
            for chunk_hash, ref_count in list(self._ref_counts.items()):
                if ref_count <= 0:
                    self.delete_chunk(chunk_hash)
                    cleaned_up += 1
                    
        except Exception as e:
            raise StorageError(f"Cleanup failed: {e}")
            
        return cleaned_up
        
    def _get_chunk_path(self, chunk_hash: str) -> Path:
        """Get file path for chunk storage."""
        # Use hierarchical storage: first 2 chars / next 2 chars / full hash
        return self.chunks_dir / chunk_hash[:2] / chunk_hash[2:4] / chunk_hash
        
    def _get_metadata_path(self, chunk_hash: str) -> Path:
        """Get file path for chunk metadata."""
        return self.metadata_dir / chunk_hash[:2] / chunk_hash[2:4] / f"{chunk_hash}.json"
        
    def _get_ref_count(self, chunk_hash: str) -> int:
        """Get reference count for chunk."""
        return self._ref_counts.get(chunk_hash, 0)
        
    def _increment_ref_count(self, chunk_hash: str) -> None:
        """Increment reference count for chunk."""
        self._ref_counts[chunk_hash] = self._get_ref_count(chunk_hash) + 1
        self._save_ref_counts()
        
    def _decrement_ref_count(self, chunk_hash: str) -> None:
        """Decrement reference count for chunk."""
        current_count = self._get_ref_count(chunk_hash)
        if current_count > 0:
            self._ref_counts[chunk_hash] = current_count - 1
            self._save_ref_counts()
            
    def _load_ref_counts(self) -> None:
        """Load reference counts from storage."""
        ref_counts_file = self.refs_dir / "ref_counts.json"
        
        if ref_counts_file.exists():
            try:
                with open(ref_counts_file, 'r') as f:
                    self._ref_counts = json.load(f)
            except Exception:
                self._ref_counts = {}
        else:
            self._ref_counts = {}
            
    def _save_ref_counts(self) -> None:
        """Save reference counts to storage."""
        ref_counts_file = self.refs_dir / "ref_counts.json"
        
        try:
            ensure_directory(ref_counts_file.parent)
            with open(ref_counts_file, 'w') as f:
                json.dump(self._ref_counts, f)
        except Exception as e:
            raise StorageError(f"Failed to save reference counts: {e}")


class MetadataStorage:
    """Storage for backup metadata and indexes."""
    
    def __init__(self, metadata_path: Path):
        """
        Initialize metadata storage.
        
        Args:
            metadata_path: Base directory for metadata
        """
        self.metadata_path = Path(metadata_path)
        self.snapshots_dir = self.metadata_path / "snapshots"
        self.indexes_dir = self.metadata_path / "indexes"
        
        ensure_directory(self.snapshots_dir)
        ensure_directory(self.indexes_dir)
        
    def store_snapshot_metadata(self, snapshot_id: str, metadata: Dict[str, Any]) -> None:
        """
        Store snapshot metadata.
        
        Args:
            snapshot_id: Unique snapshot identifier
            metadata: Snapshot metadata
            
        Raises:
            StorageError: If storage fails
        """
        try:
            snapshot_file = self.snapshots_dir / f"{snapshot_id}.json"
            
            with open(snapshot_file, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
                
        except Exception as e:
            raise StorageError(f"Failed to store snapshot metadata {snapshot_id}: {e}")
            
    def retrieve_snapshot_metadata(self, snapshot_id: str) -> Dict[str, Any]:
        """
        Retrieve snapshot metadata.
        
        Args:
            snapshot_id: Unique snapshot identifier
            
        Returns:
            Snapshot metadata
            
        Raises:
            StorageError: If retrieval fails
        """
        try:
            snapshot_file = self.snapshots_dir / f"{snapshot_id}.json"
            
            if not snapshot_file.exists():
                raise StorageError(f"Snapshot metadata not found: {snapshot_id}")
                
            with open(snapshot_file, 'r') as f:
                return json.load(f)
                
        except Exception as e:
            if isinstance(e, StorageError):
                raise
            raise StorageError(f"Failed to retrieve snapshot metadata {snapshot_id}: {e}")
            
    def list_snapshots(self) -> List[str]:
        """
        List all available snapshots.
        
        Returns:
            List of snapshot IDs
        """
        try:
            snapshots = []
            for snapshot_file in self.snapshots_dir.glob("*.json"):
                snapshot_id = snapshot_file.stem
                snapshots.append(snapshot_id)
                
            return sorted(snapshots)
            
        except Exception as e:
            raise StorageError(f"Failed to list snapshots: {e}")
            
    def delete_snapshot_metadata(self, snapshot_id: str) -> None:
        """
        Delete snapshot metadata.
        
        Args:
            snapshot_id: Unique snapshot identifier
            
        Raises:
            StorageError: If deletion fails
        """
        try:
            snapshot_file = self.snapshots_dir / f"{snapshot_id}.json"
            
            if snapshot_file.exists():
                snapshot_file.unlink()
                
        except Exception as e:
            raise StorageError(f"Failed to delete snapshot metadata {snapshot_id}: {e}")
            
    def store_index(self, index_name: str, index_data: Dict[str, Any]) -> None:
        """
        Store index data.
        
        Args:
            index_name: Name of the index
            index_data: Index data
            
        Raises:
            StorageError: If storage fails
        """
        try:
            index_file = self.indexes_dir / f"{index_name}.json"
            
            with open(index_file, 'w') as f:
                json.dump(index_data, f, indent=2, default=str)
                
        except Exception as e:
            raise StorageError(f"Failed to store index {index_name}: {e}")
            
    def retrieve_index(self, index_name: str) -> Dict[str, Any]:
        """
        Retrieve index data.
        
        Args:
            index_name: Name of the index
            
        Returns:
            Index data
            
        Raises:
            StorageError: If retrieval fails
        """
        try:
            index_file = self.indexes_dir / f"{index_name}.json"
            
            if not index_file.exists():
                return {}
                
            with open(index_file, 'r') as f:
                return json.load(f)
                
        except Exception as e:
            raise StorageError(f"Failed to retrieve index {index_name}: {e}")