"""
Asset management framework for backup systems.

This module provides abstract base classes and utilities for tracking asset relationships,
dependencies, and deduplication that can be extended by persona implementations.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from enum import Enum

from .models import FileInfo


class AssetType(Enum):
    """Types of assets that can be tracked."""
    IMAGE = "image"
    MODEL_3D = "model_3d"
    AUDIO = "audio"
    VIDEO = "video"
    TEXTURE = "texture"
    FONT = "font"
    DOCUMENT = "document"
    PROJECT = "project"
    BINARY = "binary"
    OTHER = "other"


class DependencyType(Enum):
    """Types of dependencies between assets."""
    DIRECT = "direct"        # Direct reference (e.g., texture used in material)
    INDIRECT = "indirect"    # Indirect reference (e.g., through another asset)
    SIMILAR = "similar"      # Similar content (for deduplication)
    DERIVED = "derived"      # One asset derived from another


@dataclass
class AssetInfo:
    """Information about an asset."""
    path: Path
    asset_type: AssetType
    size: int
    hash: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[Path] = field(default_factory=list)
    dependents: List[Path] = field(default_factory=list)


@dataclass
class DependencyInfo:
    """Information about a dependency relationship."""
    source: Path
    target: Path
    dependency_type: DependencyType
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReferenceMap:
    """Map of asset references and dependencies."""
    assets_to_projects: Dict[str, List[str]] = field(default_factory=dict)
    projects_to_assets: Dict[str, List[str]] = field(default_factory=dict)
    deduplication_map: Dict[str, str] = field(default_factory=dict)
    asset_metadata: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    dependencies: List[DependencyInfo] = field(default_factory=list)


class BaseAssetTracker(ABC):
    """Abstract base class for asset tracking and relationship management."""
    
    def __init__(self, project_path: Path):
        """Initialize the asset tracker.
        
        Args:
            project_path: Root path of the project to track
        """
        self.project_path = project_path
        self._asset_cache: Dict[str, AssetInfo] = {}
    
    @abstractmethod
    def scan_project(self, ignore_patterns: Optional[List[str]] = None) -> ReferenceMap:
        """Scan the project directory for assets and build reference map.
        
        Args:
            ignore_patterns: List of patterns to ignore during scanning
            
        Returns:
            ReferenceMap containing all discovered assets and relationships
        """
        pass
    
    @abstractmethod
    def track_dependencies(self, file_path: Path) -> List[DependencyInfo]:
        """Track dependencies for a specific file.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            List of dependency information
        """
        pass
    
    @abstractmethod
    def find_duplicates(self, threshold: float = 0.95) -> Dict[str, List[Path]]:
        """Find duplicate or similar assets.
        
        Args:
            threshold: Similarity threshold (0.0 to 1.0)
            
        Returns:
            Dictionary mapping canonical paths to lists of duplicates
        """
        pass
    
    def get_asset_info(self, file_path: Path) -> Optional[AssetInfo]:
        """Get cached asset information.
        
        Args:
            file_path: Path to the asset
            
        Returns:
            AssetInfo if available, None otherwise
        """
        return self._asset_cache.get(str(file_path))
    
    def update_asset_cache(self, asset_info: AssetInfo) -> None:
        """Update the asset cache with new information.
        
        Args:
            asset_info: Asset information to cache
        """
        self._asset_cache[str(asset_info.path)] = asset_info
    
    def get_dependents(self, file_path: Path) -> List[Path]:
        """Get all files that depend on the given file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            List of dependent file paths
        """
        asset_info = self.get_asset_info(file_path)
        return asset_info.dependents if asset_info else []
    
    def get_dependencies(self, file_path: Path) -> List[Path]:
        """Get all files that the given file depends on.
        
        Args:
            file_path: Path to the file
            
        Returns:
            List of dependency file paths
        """
        asset_info = self.get_asset_info(file_path)
        return asset_info.dependencies if asset_info else []


class AssetUtils:
    """Utility functions for asset management."""
    
    @staticmethod
    def classify_asset_type(file_path: Path) -> AssetType:
        """Classify an asset based on its file extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            AssetType classification
        """
        ext = file_path.suffix.lower()
        
        image_exts = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}
        model_3d_exts = {'.obj', '.fbx', '.dae', '.3ds', '.stl', '.ply', '.gltf', '.glb'}
        audio_exts = {'.wav', '.mp3', '.ogg', '.flac', '.aac', '.wma'}
        video_exts = {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv'}
        texture_exts = {'.dds', '.hdr', '.exr'}
        font_exts = {'.ttf', '.otf', '.woff', '.woff2'}
        document_exts = {'.pdf', '.doc', '.docx', '.txt', '.md'}
        project_exts = {'.psd', '.ai', '.blend', '.max', '.ma', '.mb'}
        
        if ext in image_exts:
            return AssetType.IMAGE
        elif ext in model_3d_exts:
            return AssetType.MODEL_3D
        elif ext in audio_exts:
            return AssetType.AUDIO
        elif ext in video_exts:
            return AssetType.VIDEO
        elif ext in texture_exts:
            return AssetType.TEXTURE
        elif ext in font_exts:
            return AssetType.FONT
        elif ext in document_exts:
            return AssetType.DOCUMENT
        elif ext in project_exts:
            return AssetType.PROJECT
        else:
            return AssetType.OTHER
    
    @staticmethod
    def calculate_content_similarity(file1: Path, file2: Path) -> float:
        """Calculate content similarity between two files.
        
        Args:
            file1: Path to the first file
            file2: Path to the second file
            
        Returns:
            Similarity score between 0.0 and 1.0
        """
        # This is a placeholder implementation
        # Real implementation would use content-based comparison
        if file1.stat().st_size == file2.stat().st_size:
            return 0.8  # Assume similar if same size
        return 0.0
    
    @staticmethod
    def extract_asset_metadata(file_path: Path) -> Dict[str, Any]:
        """Extract metadata from an asset file.
        
        Args:
            file_path: Path to the asset file
            
        Returns:
            Dictionary containing extracted metadata
        """
        metadata = {
            "size": file_path.stat().st_size,
            "modified_time": file_path.stat().st_mtime,
            "asset_type": AssetUtils.classify_asset_type(file_path).value
        }
        
        # Add format-specific metadata extraction here
        # This would typically use specialized libraries
        
        return metadata
    
    @staticmethod
    def find_asset_references(file_path: Path, content: str) -> List[Path]:
        """Find asset references within file content.
        
        Args:
            file_path: Path to the file being analyzed
            content: Text content of the file
            
        Returns:
            List of referenced asset paths
        """
        references = []
        
        # This is a basic implementation that looks for file paths
        # Real implementations would be format-specific
        import re
        
        # Look for common file extensions in the content
        patterns = [
            r'[\"\']([^\"\']+\.(png|jpg|jpeg|gif|bmp|obj|fbx|wav|mp3))[\"\']]',
            r'src\s*=\s*[\"\']([^\"\']+)[\"\']]',
            r'href\s*=\s*[\"\']([^\"\']+)[\"\']]'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    ref_path = match[0]
                else:
                    ref_path = match
                
                # Convert relative paths to absolute
                if not Path(ref_path).is_absolute():
                    ref_path = file_path.parent / ref_path
                
                if Path(ref_path).exists():
                    references.append(Path(ref_path))
        
        return references