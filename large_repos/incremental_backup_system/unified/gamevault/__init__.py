"""
GameVault - Incremental Backup System for Game Development.

A specialized incremental backup system designed for indie game developers 
who create frequent iterations with extensive playtesting feedback.

Now powered by the unified backup system infrastructure for enhanced 
reliability and performance.
"""

from gamevault.backup_engine import BackupEngine
from gamevault.config import get_config, configure, GameVaultConfig
from gamevault.models import (
    GameVersionType, PlatformType, FileInfo, ProjectVersion,
    FeedbackEntry, PlaytestSession, PlatformConfig
)

# Game-specific feature modules
from gamevault import (
    asset_optimization,
    feedback_system,
    milestone_management,
    platform_config,
    playtest_recorder
)

__version__ = "0.1.0"

__all__ = [
    'BackupEngine',
    'get_config',
    'configure', 
    'GameVaultConfig',
    'GameVersionType',
    'PlatformType',
    'FileInfo',
    'ProjectVersion',
    'FeedbackEntry',
    'PlaytestSession',
    'PlatformConfig',
    'asset_optimization',
    'feedback_system',
    'milestone_management',
    'platform_config',
    'playtest_recorder'
]