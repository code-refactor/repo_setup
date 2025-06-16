"""
Shared enumerations for file system analyzer implementations.

This module provides common enumerations used across both the Security Auditor
and Database Administrator implementations.
"""

from enum import Enum


class Priority(str, Enum):
    """Priority levels for recommendations and findings."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class SeverityLevel(str, Enum):
    """Severity levels for analysis results."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AnalysisStatus(str, Enum):
    """Status of analysis operations."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class FileType(str, Enum):
    """Common file types encountered in analysis."""
    DATABASE = "database"
    LOG = "log"
    BACKUP = "backup"
    CONFIG = "config"
    DATA = "data"
    INDEX = "index"
    TEMP = "temp"
    ARCHIVE = "archive"
    DOCUMENT = "document"
    EXECUTABLE = "executable"
    UNKNOWN = "unknown"


class RecommendationType(str, Enum):
    """Types of recommendations that can be generated."""
    OPTIMIZATION = "optimization"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    MAINTENANCE = "maintenance"
    CLEANUP = "cleanup"
    MONITORING = "monitoring"