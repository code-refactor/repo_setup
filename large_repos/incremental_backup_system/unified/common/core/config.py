"""
Configuration management for the unified backup system.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Set

from pydantic import BaseModel, Field, validator

from .models import BackupConfig, ChunkingConfig, CompressionConfig


class UnifiedBackupConfig(BackupConfig):
    """Extended configuration for unified backup system."""
    
    # Chunking configuration
    chunking_strategy: str = "rolling_hash"
    chunking_config: ChunkingConfig = Field(default_factory=ChunkingConfig)
    
    # Compression configuration
    compression_config: CompressionConfig = Field(default_factory=CompressionConfig)
    
    # Storage configuration
    storage_retention_days: int = Field(default=365, ge=1)
    max_storage_size_gb: Optional[int] = Field(default=None, ge=1)
    cleanup_threshold: float = Field(default=0.8, ge=0.1, le=1.0)
    
    # Performance configuration
    max_concurrent_operations: int = Field(default=4, ge=1, le=32)
    chunk_cache_size_mb: int = Field(default=256, ge=64, le=2048)
    
    # Backup behavior
    follow_symlinks: bool = False
    include_hidden_files: bool = False
    verify_integrity: bool = True
    create_thumbnails: bool = True
    
    # Advanced options
    delta_compression_threshold: float = Field(default=0.3, ge=0.1, le=0.9)
    reference_tracking_enabled: bool = True
    workspace_capture_enabled: bool = True
    
    @validator('backup_dir')
    def validate_backup_dir(cls, v):
        """Ensure backup directory is valid."""
        if isinstance(v, str):
            v = Path(v)
        if not v.exists():
            v.mkdir(parents=True, exist_ok=True)
        return v
        
    @validator('ignore_patterns')
    def validate_ignore_patterns(cls, v):
        """Ensure ignore patterns are valid."""
        if not v:
            return [
                "*.tmp", "*.temp", "*.log", "*.swp", "*.bak",
                ".DS_Store", "Thumbs.db", ".git/*", ".svn/*",
                "__pycache__/*", "*.pyc", "node_modules/*"
            ]
        return v


def load_config(config_path: Optional[Path] = None) -> UnifiedBackupConfig:
    """
    Load configuration from file or create default.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        UnifiedBackupConfig instance
    """
    if config_path and config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            return UnifiedBackupConfig(**config_data)
        except Exception as e:
            raise ValueError(f"Failed to load config from {config_path}: {e}")
    else:
        # Return default configuration
        return UnifiedBackupConfig(
            backup_dir=Path.home() / "backup_system"
        )


def save_config(config: UnifiedBackupConfig, config_path: Path) -> None:
    """
    Save configuration to file.
    
    Args:
        config: Configuration to save
        config_path: Path to save configuration
    """
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            json.dump(
                config.dict(), 
                f, 
                indent=2, 
                default=str
            )
    except Exception as e:
        raise ValueError(f"Failed to save config to {config_path}: {e}")


def get_default_config_path() -> Path:
    """
    Get default configuration file path.
    
    Returns:
        Default configuration file path
    """
    return Path.home() / ".backup_system" / "config.json"


def create_config_template(output_path: Path) -> None:
    """
    Create a configuration template file.
    
    Args:
        output_path: Path to write template
    """
    template_config = UnifiedBackupConfig(
        backup_dir=Path("./backup_data"),
        chunk_size_min=4096,
        chunk_size_max=1024*1024,
        compression_level=3,
        ignore_patterns=[
            "*.tmp", "*.temp", "*.log", "*.swp", "*.bak",
            ".DS_Store", "Thumbs.db", ".git/*", ".svn/*",
            "__pycache__/*", "*.pyc", "node_modules/*"
        ],
        chunking_strategy="rolling_hash",
        storage_retention_days=365,
        max_concurrent_operations=4,
        follow_symlinks=False,
        include_hidden_files=False,
        verify_integrity=True
    )
    
    save_config(template_config, output_path)


class ConfigManager:
    """Configuration manager with validation and persistence."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path or get_default_config_path()
        self._config: Optional[UnifiedBackupConfig] = None
        
    @property
    def config(self) -> UnifiedBackupConfig:
        """Get current configuration, loading if necessary."""
        if self._config is None:
            self._config = load_config(self.config_path)
        return self._config
        
    def reload_config(self) -> None:
        """Reload configuration from file."""
        self._config = load_config(self.config_path)
        
    def save_config(self) -> None:
        """Save current configuration to file."""
        if self._config:
            save_config(self._config, self.config_path)
            
    def update_config(self, **kwargs) -> None:
        """
        Update configuration values.
        
        Args:
            **kwargs: Configuration values to update
        """
        if self._config is None:
            self._config = load_config(self.config_path)
            
        # Create new config with updated values
        config_dict = self._config.dict()
        config_dict.update(kwargs)
        self._config = UnifiedBackupConfig(**config_dict)
        
    def get_chunking_config(self) -> ChunkingConfig:
        """Get chunking configuration."""
        return self.config.chunking_config
        
    def get_compression_config(self) -> CompressionConfig:
        """Get compression configuration."""
        return self.config.compression_config
        
    def validate_config(self) -> List[str]:
        """
        Validate current configuration.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        try:
            config = self.config
            
            # Validate backup directory
            if not config.backup_dir.exists():
                try:
                    config.backup_dir.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    errors.append(f"Cannot create backup directory: {e}")
                    
            # Validate chunk size settings
            if config.chunk_size_min >= config.chunk_size_max:
                errors.append("Minimum chunk size must be less than maximum chunk size")
                
            # Validate compression level
            if config.compression_level < 0 or config.compression_level > 22:
                errors.append("Compression level must be between 0 and 22")
                
            # Validate retention settings
            if config.storage_retention_days < 1:
                errors.append("Storage retention must be at least 1 day")
                
            # Validate performance settings
            if config.max_concurrent_operations < 1:
                errors.append("Max concurrent operations must be at least 1")
                
            if config.chunk_cache_size_mb < 64:
                errors.append("Chunk cache size must be at least 64 MB")
                
        except Exception as e:
            errors.append(f"Configuration validation failed: {e}")
            
        return errors
        
    def get_effective_ignore_patterns(self) -> List[str]:
        """
        Get effective ignore patterns including defaults.
        
        Returns:
            Complete list of ignore patterns
        """
        patterns = list(self.config.ignore_patterns)
        
        # Add default system patterns if not already present
        default_patterns = [
            "*.tmp", "*.temp", "*.log", "*.swp", "*.bak",
            ".DS_Store", "Thumbs.db", ".git/*", ".svn/*",
            "__pycache__/*", "*.pyc", "node_modules/*"
        ]
        
        for pattern in default_patterns:
            if pattern not in patterns:
                patterns.append(pattern)
                
        return patterns
        
    def get_binary_extensions(self) -> Set[str]:
        """
        Get set of binary file extensions.
        
        Returns:
            Set of binary file extensions
        """
        return self.config.binary_extensions.copy()
        
    def is_file_ignored(self, file_path: Path) -> bool:
        """
        Check if file should be ignored based on patterns.
        
        Args:
            file_path: File path to check
            
        Returns:
            True if file should be ignored
        """
        patterns = self.get_effective_ignore_patterns()
        
        for pattern in patterns:
            if file_path.match(pattern) or file_path.name.match(pattern):
                return True
                
        return False