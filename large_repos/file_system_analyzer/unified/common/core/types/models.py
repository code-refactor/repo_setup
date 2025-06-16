"""
Shared Pydantic models for file system analyzer implementations.

This module provides common data models used across both the Security Auditor
and Database Administrator implementations.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

from pydantic import BaseModel, Field

from .enums import Priority, SeverityLevel, AnalysisStatus, FileType, RecommendationType


class TimestampedModel(BaseModel):
    """Base model with timestamp fields."""
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None


class FileInfo(BaseModel):
    """Common file information model."""
    file_path: str
    file_name: str
    file_size: int
    file_type: Optional[str] = None
    mime_type: Optional[str] = None
    last_modified: datetime
    creation_time: Optional[datetime] = None
    last_accessed: Optional[datetime] = None
    hash_sha256: Optional[str] = None
    exists: bool = True
    is_file: bool = True
    is_dir: bool = False
    is_symlink: bool = False
    permissions: Optional[str] = None


class AnalysisResult(TimestampedModel):
    """Base analysis result structure."""
    analysis_id: str
    status: AnalysisStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    
    @property
    def is_complete(self) -> bool:
        """Check if analysis is complete."""
        return self.status in [AnalysisStatus.COMPLETED, AnalysisStatus.FAILED]
    
    @property
    def is_successful(self) -> bool:
        """Check if analysis completed successfully."""
        return self.status == AnalysisStatus.COMPLETED


class RecommendationModel(TimestampedModel):
    """Base recommendation model."""
    title: str
    description: str
    priority: Priority
    recommendation_type: RecommendationType
    estimated_effort: Optional[str] = None
    estimated_impact: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Optional fields for different implementations
    estimated_space_savings_bytes: Optional[int] = None  # DB admin
    compliance_framework: Optional[str] = None  # Security auditor
    file_path: Optional[str] = None
    line_number: Optional[int] = None


class ScanSummary(TimestampedModel):
    """Summary of scan operations."""
    total_files: int
    total_size_bytes: int
    files_processed: int
    files_with_issues: int = 0
    files_with_errors: int = 0
    duration: float
    start_time: datetime
    end_time: datetime
    
    # Flexible fields for different implementations
    additional_metrics: Dict[str, Any] = Field(default_factory=dict)


class CacheEntry(TimestampedModel):
    """Cache entry model for result caching."""
    key: str
    value: Any
    ttl_seconds: int = 3600
    expires_at: datetime
    
    @property
    def is_expired(self) -> bool:
        """Check if cache entry is expired."""
        return datetime.now() > self.expires_at


class ConfigurationModel(BaseModel):
    """Base configuration model."""
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    max_workers: int = 10
    recursive: bool = True
    follow_symlinks: bool = False
    skip_hidden: bool = True
    output_dir: Optional[str] = None
    
    # File filtering options
    include_extensions: List[str] = Field(default_factory=list)
    exclude_extensions: List[str] = Field(default_factory=list)
    include_patterns: List[str] = Field(default_factory=list)
    exclude_patterns: List[str] = Field(default_factory=list)
    
    # Analysis options
    enable_caching: bool = True
    cache_ttl_seconds: int = 3600
    notification_threshold: Priority = Priority.HIGH
    
    # Additional configuration
    metadata: Dict[str, Any] = Field(default_factory=dict)