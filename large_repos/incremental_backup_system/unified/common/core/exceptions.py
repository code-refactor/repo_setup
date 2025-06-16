"""
Common exception classes for the unified backup system.
"""


class BackupSystemError(Exception):
    """Base exception for all backup system errors."""
    pass


class StorageError(BackupSystemError):
    """Raised when storage operations fail."""
    pass


class CompressionError(BackupSystemError):
    """Raised when compression/decompression fails."""
    pass


class ChunkingError(BackupSystemError):
    """Raised when file chunking fails."""
    pass


class HashError(BackupSystemError):
    """Raised when hash calculation fails."""
    pass


class ConfigurationError(BackupSystemError):
    """Raised when configuration is invalid."""
    pass


class SnapshotError(BackupSystemError):
    """Raised when snapshot operations fail."""
    pass


class RestoreError(BackupSystemError):
    """Raised when restore operations fail."""
    pass


class FileNotFoundError(BackupSystemError):
    """Raised when a required file is not found."""
    pass


class CorruptedDataError(BackupSystemError):
    """Raised when data integrity checks fail."""
    pass