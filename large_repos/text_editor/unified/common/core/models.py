from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid

from pydantic import BaseModel, Field


class Position(BaseModel):
    """Represents a position within text content."""
    line: int = Field(ge=0, description="Line number (0-indexed)")
    column: int = Field(ge=0, description="Column number (0-indexed)")

    def __lt__(self, other: "Position") -> bool:
        """Compare positions for ordering."""
        if self.line != other.line:
            return self.line < other.line
        return self.column < other.column

    def __le__(self, other: "Position") -> bool:
        """Compare positions for ordering."""
        return self < other or self == other

    def __gt__(self, other: "Position") -> bool:
        """Compare positions for ordering."""
        return not self <= other

    def __ge__(self, other: "Position") -> bool:
        """Compare positions for ordering."""
        return not self < other


class Selection(BaseModel):
    """Represents a selected region of text."""
    start: Position
    end: Position
    
    @property
    def is_valid(self) -> bool:
        """Check if the selection is valid (start <= end)."""
        return self.start <= self.end
    
    @property
    def is_empty(self) -> bool:
        """Check if the selection is empty (start == end)."""
        return self.start == self.end


class Direction(str, Enum):
    """Movement directions for cursor navigation."""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    HOME = "home"
    END = "end"
    PAGE_UP = "page_up"
    PAGE_DOWN = "page_down"


class ChangeType(str, Enum):
    """Types of changes that can be made to text."""
    INSERT = "insert"
    DELETE = "delete"
    REPLACE = "replace"


class Change(BaseModel):
    """Represents a change made to the text buffer."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    type: ChangeType
    position: Position
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def reverse(self) -> "Change":
        """Create the reverse of this change for undo operations."""
        if self.type == ChangeType.INSERT:
            return Change(
                type=ChangeType.DELETE,
                position=self.position,
                content=self.content,
                metadata=self.metadata
            )
        elif self.type == ChangeType.DELETE:
            return Change(
                type=ChangeType.INSERT,
                position=self.position,
                content=self.content,
                metadata=self.metadata
            )
        else:  # REPLACE
            # For replace, metadata should contain the original content
            original_content = self.metadata.get("original_content", "")
            return Change(
                type=ChangeType.REPLACE,
                position=self.position,
                content=original_content,
                metadata={"original_content": self.content}
            )


class NavigationHistory(BaseModel):
    """Tracks navigation history for jumping between positions."""
    positions: List[Position] = Field(default_factory=list)
    current_index: int = 0
    max_history: int = 100
    
    def add_position(self, position: Position) -> None:
        """Add a new position to the navigation history."""
        # Remove any positions after current index if we're not at the end
        if self.current_index < len(self.positions) - 1:
            self.positions = self.positions[:self.current_index + 1]
        
        # Add new position
        self.positions.append(position)
        
        # Limit history size
        if len(self.positions) > self.max_history:
            self.positions = self.positions[-self.max_history:]
        
        self.current_index = len(self.positions) - 1
    
    def can_go_back(self) -> bool:
        """Check if we can navigate backward."""
        return self.current_index > 0
    
    def can_go_forward(self) -> bool:
        """Check if we can navigate forward."""
        return self.current_index < len(self.positions) - 1
    
    def go_back(self) -> Optional[Position]:
        """Navigate to the previous position."""
        if self.can_go_back():
            self.current_index -= 1
            return self.positions[self.current_index]
        return None
    
    def go_forward(self) -> Optional[Position]:
        """Navigate to the next position."""
        if self.can_go_forward():
            self.current_index += 1
            return self.positions[self.current_index]
        return None


class Match(BaseModel):
    """Represents a search match within text."""
    position: Position
    length: int
    content: str
    groups: List[str] = Field(default_factory=list)


class FileInfo(BaseModel):
    """Information about a file."""
    path: Optional[str] = None
    encoding: str = "utf-8"
    modified: bool = False
    last_modified: Optional[datetime] = None
    size: int = 0


class EditorState(BaseModel):
    """Complete state of the editor."""
    cursor_position: Position = Field(default_factory=lambda: Position(line=0, column=0))
    selection: Optional[Selection] = None
    file_info: FileInfo = Field(default_factory=FileInfo)
    navigation_history: NavigationHistory = Field(default_factory=NavigationHistory)
    modified: bool = False