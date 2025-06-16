"""
Core data models for GameVault.

This module contains the game-specific data models and extends common models.
"""

import uuid
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Union

from pydantic import BaseModel, Field

# Import common models to extend and reuse
from common.core.models import (
    FileInfo as CommonFileInfo, 
    SnapshotInfo as CommonSnapshotInfo,
    ChangeInfo as CommonChangeInfo,
    ChangeSet as CommonChangeSet,
    ChangeType,
    FileType,
    ChunkInfo
)


class GameVersionType(str, Enum):
    """Type of game version/milestone."""
    
    DEVELOPMENT = "development"
    FIRST_PLAYABLE = "first_playable"
    ALPHA = "alpha"
    BETA = "beta"
    RELEASE_CANDIDATE = "release_candidate"
    RELEASE = "release"
    PATCH = "patch"
    HOTFIX = "hotfix"


class PlatformType(str, Enum):
    """Type of target platform."""
    
    PC = "pc"
    MOBILE = "mobile"
    CONSOLE = "console"
    VR = "vr"
    WEB = "web"
    OTHER = "other"


class FileInfo(CommonFileInfo):
    """Game-specific file information extending common FileInfo."""

    # Additional game-specific fields
    is_binary: bool = Field(..., description="Whether the file is binary or text")
    chunks: Optional[List[str]] = Field(None, description="List of chunk IDs for binary files")
    storage_path: Optional[str] = Field(None, description="Path where the file is stored in the backup")
    
    @classmethod
    def from_common_file_info(cls, common_file_info: CommonFileInfo, is_binary: bool = False, 
                             chunks: Optional[List[str]] = None, storage_path: Optional[str] = None) -> 'FileInfo':
        """Create GameVault FileInfo from common FileInfo."""
        return cls(
            path=common_file_info.path,
            size=common_file_info.size,
            hash=common_file_info.hash,
            modified_time=common_file_info.modified_time,
            file_type=common_file_info.file_type,
            content_type=common_file_info.content_type,
            chunk_hashes=common_file_info.chunk_hashes,
            chunks=chunks,
            metadata=common_file_info.metadata,
            is_binary=is_binary,
            storage_path=storage_path
        )


class ProjectVersion(BaseModel):
    """Represents a version of a game project, compatible with common SnapshotInfo."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique ID of the version")
    timestamp: float = Field(..., description="Creation time as Unix timestamp")
    name: str = Field(..., description="Name of the version")  # Game-specific extension
    parent_id: Optional[str] = Field(None, description="ID of the parent version")
    type: GameVersionType = Field(default=GameVersionType.DEVELOPMENT, description="Type of this version")  # Game-specific
    tags: List[str] = Field(default_factory=list, description="List of tags for this version")
    description: Optional[str] = Field(None, description="Description of this version")
    files: Dict[str, FileInfo] = Field(default_factory=dict, description="Map of file paths to file info")
    is_milestone: bool = Field(default=False, description="Whether this version is a milestone")  # Game-specific
    
    def to_common_snapshot_info(self, source_path: Path) -> CommonSnapshotInfo:
        """Convert to common SnapshotInfo."""
        return CommonSnapshotInfo(
            id=self.id,
            timestamp=datetime.fromtimestamp(self.timestamp),
            source_path=source_path,
            parent_id=self.parent_id,
            files=[file_info for file_info in self.files.values()],
            changes=[],  # Would need to be populated from version tracking
            tags=set(self.tags),
            metadata={
                "name": self.name,
                "type": self.type.value,
                "description": self.description,
                "is_milestone": self.is_milestone
            }
        )
    
    @classmethod
    def from_common_snapshot_info(cls, snapshot: CommonSnapshotInfo, name: str, 
                                 version_type: GameVersionType = GameVersionType.DEVELOPMENT,
                                 is_milestone: bool = False) -> 'ProjectVersion':
        """Create ProjectVersion from common SnapshotInfo."""
        files_dict = {}
        for file_info in snapshot.files:
            if isinstance(file_info, FileInfo):
                files_dict[str(file_info.path)] = file_info
            else:
                # Convert common FileInfo to game FileInfo
                game_file_info = FileInfo.from_common_file_info(file_info)
                files_dict[str(file_info.path)] = game_file_info
        
        return cls(
            id=snapshot.id,
            timestamp=snapshot.timestamp.timestamp(),
            name=name,
            parent_id=snapshot.parent_id,
            type=version_type,
            tags=list(snapshot.tags),
            description=snapshot.metadata.get("description"),
            files=files_dict,
            is_milestone=is_milestone
        )


class FeedbackEntry(BaseModel):
    """A single piece of feedback from a player."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique ID of the feedback")
    player_id: str = Field(..., description="ID of the player who provided the feedback")
    version_id: str = Field(..., description="ID of the game version this feedback is for")
    timestamp: float = Field(..., description="Time the feedback was recorded as Unix timestamp")
    category: str = Field(..., description="Category of the feedback (bug, suggestion, etc.)")
    content: str = Field(..., description="Actual feedback text")
    metadata: Dict[str, Union[str, int, float, bool]] = Field(default_factory=dict, description="Additional metadata")
    tags: List[str] = Field(default_factory=list, description="Tags assigned to this feedback")
    priority: Optional[int] = Field(None, description="Priority level (if applicable)")
    resolved: bool = Field(default=False, description="Whether this feedback has been addressed")


class PlaytestSession(BaseModel):
    """Information about a playtest session."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique ID of the session")
    version_id: str = Field(..., description="ID of the game version used in this session")
    player_id: str = Field(..., description="ID of the player who participated")
    timestamp: float = Field(..., description="Start time of the session as Unix timestamp")
    duration: float = Field(..., description="Duration of the session in seconds")
    completed: bool = Field(default=False, description="Whether the session was completed")
    events: List[Dict] = Field(default_factory=list, description="List of recorded game events")
    metrics: Dict[str, float] = Field(default_factory=dict, description="Metrics recorded during the session")
    checkpoint_ids: List[str] = Field(default_factory=list, description="IDs of saved game states")


class PlatformConfig(BaseModel):
    """Configuration for a specific platform."""

    platform: PlatformType = Field(..., description="Target platform")
    settings: Dict[str, Union[str, int, float, bool]] = Field(
        default_factory=dict, description="Platform-specific settings"
    )
    build_flags: Dict[str, str] = Field(default_factory=dict, description="Build flags for this platform")
    resolution: Optional[Dict[str, Union[int, float]]] = Field(None, description="Screen resolution settings")
    performance_targets: Optional[Dict[str, float]] = Field(None, description="Performance target metrics")
    required_features: Set[str] = Field(default_factory=set, description="Features required for this platform")
    disabled_features: Set[str] = Field(default_factory=set, description="Features disabled on this platform")