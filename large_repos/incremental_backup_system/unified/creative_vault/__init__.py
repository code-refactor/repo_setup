"""
CreativeVault - Advanced backup system for digital artists and creative professionals.

This package provides comprehensive backup functionality with specialized features
for creative workflows including visual diffs, asset tracking, and workspace capture.
"""

from creative_vault.backup_engine.incremental_backup import DeltaBackupEngine
from creative_vault.visual_diff.diff_generator import CreativeVisualDiffGenerator
from creative_vault.timeline.timeline_manager import CreativeTimelineManager
from creative_vault.element_extraction.extractor import CreativeElementExtractor
from creative_vault.asset_tracker.reference_tracker import CreativeAssetReferenceTracker
from creative_vault.workspace_capture.environment_capture import CreativeEnvironmentCapture
from creative_vault.utils import BackupConfig, FileInfo
from creative_vault.__main__ import CreativeVault

__all__ = [
    'CreativeVault',
    'DeltaBackupEngine',
    'CreativeVisualDiffGenerator',
    'CreativeTimelineManager',
    'CreativeElementExtractor',
    'CreativeAssetReferenceTracker',
    'CreativeEnvironmentCapture',
    'BackupConfig',
    'FileInfo'
]

__version__ = '1.0.0'