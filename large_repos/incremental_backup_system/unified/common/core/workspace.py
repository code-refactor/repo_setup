"""
Workspace management framework for backup systems.

This module provides abstract base classes and utilities for capturing and managing
workspace states, application configurations, and environment settings.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
from enum import Enum
import platform


class ApplicationType(Enum):
    """Types of applications that can be managed."""
    CREATIVE_SUITE = "creative_suite"      # Adobe CC, Affinity, etc.
    IDE = "ide"                           # VS Code, IntelliJ, etc.
    GAME_ENGINE = "game_engine"           # Unity, Unreal, Godot, etc.
    MODELING_3D = "modeling_3d"           # Blender, Maya, 3ds Max, etc.
    BROWSER = "browser"                   # Chrome, Firefox, etc.
    OTHER = "other"


class PlatformType(Enum):
    """Supported platforms."""
    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"


@dataclass
class ApplicationInfo:
    """Information about an application."""
    name: str
    app_type: ApplicationType
    version: Optional[str] = None
    install_path: Optional[Path] = None
    config_paths: List[Path] = field(default_factory=list)
    data_paths: List[Path] = field(default_factory=list)
    process_name: Optional[str] = None


@dataclass
class WorkspaceState:
    """Represents the state of a workspace."""
    name: str
    timestamp: float
    platform: PlatformType
    applications: List[ApplicationInfo] = field(default_factory=list)
    environment_vars: Dict[str, str] = field(default_factory=dict)
    config_files: Dict[str, Path] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseWorkspaceCapture(ABC):
    """Abstract base class for workspace state capture."""
    
    def __init__(self, workspace_name: str = "default"):
        """Initialize the workspace capture.
        
        Args:
            workspace_name: Name of the workspace to manage
        """
        self.workspace_name = workspace_name
        self.platform = self._detect_platform()
    
    @abstractmethod
    def capture_workspace(self, output_path: Path) -> WorkspaceState:
        """Capture the current workspace state.
        
        Args:
            output_path: Path to save the workspace state
            
        Returns:
            WorkspaceState containing captured information
        """
        pass
    
    @abstractmethod
    def restore_workspace(self, workspace_state: WorkspaceState, target_path: Path) -> bool:
        """Restore a workspace state.
        
        Args:
            workspace_state: The workspace state to restore
            target_path: Path to restore the workspace to
            
        Returns:
            True if restoration was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_supported_applications(self) -> List[ApplicationType]:
        """Get the list of application types supported by this implementation.
        
        Returns:
            List of supported application types
        """
        pass
    
    def _detect_platform(self) -> PlatformType:
        """Detect the current platform.
        
        Returns:
            PlatformType for the current platform
        """
        system = platform.system().lower()
        if system == "windows":
            return PlatformType.WINDOWS
        elif system == "darwin":
            return PlatformType.MACOS
        elif system == "linux":
            return PlatformType.LINUX
        else:
            return PlatformType.LINUX  # Default fallback
    
    def is_application_running(self, app_info: ApplicationInfo) -> bool:
        """Check if an application is currently running.
        
        Args:
            app_info: Application information
            
        Returns:
            True if the application is running, False otherwise
        """
        if not app_info.process_name:
            return False
        
        try:
            import psutil
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] and app_info.process_name.lower() in proc.info['name'].lower():
                    return True
        except ImportError:
            # psutil not available, return False
            pass
        
        return False
    
    def get_application_info(self, app_name: str) -> Optional[ApplicationInfo]:
        """Get information about a specific application.
        
        Args:
            app_name: Name of the application
            
        Returns:
            ApplicationInfo if found, None otherwise
        """
        # This would be implemented by subclasses with specific application knowledge
        return None


class WorkspaceUtils:
    """Utility functions for workspace management."""
    
    @staticmethod
    def get_default_config_paths(platform: PlatformType) -> Dict[str, Path]:
        """Get default configuration paths for a platform.
        
        Args:
            platform: The target platform
            
        Returns:
            Dictionary mapping config types to paths
        """
        home = Path.home()
        
        if platform == PlatformType.WINDOWS:
            return {
                "appdata": Path.home() / "AppData",
                "local_appdata": Path.home() / "AppData" / "Local",
                "roaming_appdata": Path.home() / "AppData" / "Roaming",
                "documents": Path.home() / "Documents",
                "temp": Path.home() / "AppData" / "Local" / "Temp"
            }
        elif platform == PlatformType.MACOS:
            return {
                "library": home / "Library",
                "preferences": home / "Library" / "Preferences",
                "application_support": home / "Library" / "Application Support",
                "caches": home / "Library" / "Caches",
                "documents": home / "Documents"
            }
        elif platform == PlatformType.LINUX:
            return {
                "config": home / ".config",
                "local": home / ".local",
                "cache": home / ".cache",
                "documents": home / "Documents",
                "temp": Path("/tmp")
            }
        else:
            return {}
    
    @staticmethod
    def backup_config_file(config_path: Path, backup_dir: Path) -> Optional[Path]:
        """Backup a configuration file.
        
        Args:
            config_path: Path to the configuration file
            backup_dir: Directory to store the backup
            
        Returns:
            Path to the backed up file, or None if backup failed
        """
        if not config_path.exists():
            return None
        
        try:
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup_path = backup_dir / config_path.name
            
            import shutil
            shutil.copy2(config_path, backup_path)
            return backup_path
        except Exception:
            return None
    
    @staticmethod
    def restore_config_file(backup_path: Path, target_path: Path) -> bool:
        """Restore a configuration file from backup.
        
        Args:
            backup_path: Path to the backup file
            target_path: Path to restore the file to
            
        Returns:
            True if restoration was successful, False otherwise
        """
        if not backup_path.exists():
            return False
        
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            import shutil
            shutil.copy2(backup_path, target_path)
            return True
        except Exception:
            return False
    
    @staticmethod
    def create_workspace_archive(workspace_state: WorkspaceState, output_path: Path) -> bool:
        """Create a ZIP archive of a workspace state.
        
        Args:
            workspace_state: The workspace state to archive
            output_path: Path to the output ZIP file
            
        Returns:
            True if archive creation was successful, False otherwise
        """
        try:
            import zipfile
            import json
            
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add workspace metadata
                metadata = {
                    "name": workspace_state.name,
                    "timestamp": workspace_state.timestamp,
                    "platform": workspace_state.platform.value,
                    "applications": [
                        {
                            "name": app.name,
                            "app_type": app.app_type.value,
                            "version": app.version,
                            "install_path": str(app.install_path) if app.install_path else None,
                            "process_name": app.process_name
                        }
                        for app in workspace_state.applications
                    ],
                    "environment_vars": workspace_state.environment_vars,
                    "metadata": workspace_state.metadata
                }
                
                zipf.writestr("workspace_metadata.json", json.dumps(metadata, indent=2))
                
                # Add configuration files
                for config_name, config_path in workspace_state.config_files.items():
                    if config_path.exists():
                        zipf.write(config_path, f"configs/{config_name}")
            
            return True
        except Exception:
            return False
    
    @staticmethod
    def extract_workspace_archive(archive_path: Path, output_dir: Path) -> Optional[WorkspaceState]:
        """Extract a workspace state from a ZIP archive.
        
        Args:
            archive_path: Path to the ZIP archive
            output_dir: Directory to extract files to
            
        Returns:
            WorkspaceState if extraction was successful, None otherwise
        """
        try:
            import zipfile
            import json
            
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                # Extract all files
                zipf.extractall(output_dir)
                
                # Read metadata
                metadata_path = output_dir / "workspace_metadata.json"
                if metadata_path.exists():
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                    
                    # Reconstruct workspace state
                    applications = []
                    for app_data in metadata.get("applications", []):
                        app_info = ApplicationInfo(
                            name=app_data["name"],
                            app_type=ApplicationType(app_data["app_type"]),
                            version=app_data.get("version"),
                            install_path=Path(app_data["install_path"]) if app_data.get("install_path") else None,
                            process_name=app_data.get("process_name")
                        )
                        applications.append(app_info)
                    
                    # Find extracted config files
                    config_files = {}
                    configs_dir = output_dir / "configs"
                    if configs_dir.exists():
                        for config_file in configs_dir.iterdir():
                            if config_file.is_file():
                                config_files[config_file.name] = config_file
                    
                    workspace_state = WorkspaceState(
                        name=metadata["name"],
                        timestamp=metadata["timestamp"],
                        platform=PlatformType(metadata["platform"]),
                        applications=applications,
                        environment_vars=metadata.get("environment_vars", {}),
                        config_files=config_files,
                        metadata=metadata.get("metadata", {})
                    )
                    
                    return workspace_state
            
        except Exception:
            pass
        
        return None