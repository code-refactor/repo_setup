"""
Unified backup system common library.

This package provides shared functionality for all backup system implementations:
- Core backup engine with incremental backups and deduplication
- Content-addressed storage with compression
- File chunking strategies for optimal storage
- Configuration management and utilities

Usage:
    from common import core
    from common.core import UnifiedBackupEngine, UnifiedBackupConfig
"""

from . import core

__version__ = "1.0.0"
__all__ = ['core']
