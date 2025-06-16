from typing import List, Optional
from pydantic import BaseModel, Field

from .models import Change, ChangeType, Position
from .buffer import TextBuffer


class History(BaseModel):
    """Manages undo/redo history for text buffer operations."""
    
    changes: List[Change] = Field(default_factory=list)
    current_index: int = -1
    max_history: int = 1000
    
    def record_change(self, change: Change) -> None:
        """Record a new change in the history."""
        # Remove any changes after current index if we're not at the end
        if self.current_index < len(self.changes) - 1:
            self.changes = self.changes[:self.current_index + 1]
        
        # Add new change
        self.changes.append(change)
        
        # Limit history size
        if len(self.changes) > self.max_history:
            self.changes = self.changes[-self.max_history:]
        
        self.current_index = len(self.changes) - 1
    
    def can_undo(self) -> bool:
        """Check if there are changes that can be undone."""
        return self.current_index >= 0
    
    def can_redo(self) -> bool:
        """Check if there are changes that can be redone."""
        return self.current_index < len(self.changes) - 1
    
    def undo(self, buffer: TextBuffer) -> Optional[Change]:
        """Undo the last change and return the change that was undone."""
        if not self.can_undo():
            return None
        
        change = self.changes[self.current_index]
        self.current_index -= 1
        
        # Apply the reverse of the change
        reverse_change = change.reverse()
        self._apply_change(buffer, reverse_change)
        
        return change
    
    def redo(self, buffer: TextBuffer) -> Optional[Change]:
        """Redo the next change and return the change that was redone."""
        if not self.can_redo():
            return None
        
        self.current_index += 1
        change = self.changes[self.current_index]
        
        # Apply the change
        self._apply_change(buffer, change)
        
        return change
    
    def _apply_change(self, buffer: TextBuffer, change: Change) -> None:
        """Apply a change to the buffer without recording it in history."""
        original_modified = buffer.modified
        
        if change.type == ChangeType.INSERT:
            buffer.insert_text(change.position, change.content)
        elif change.type == ChangeType.DELETE:
            # Calculate end position based on content
            end_pos = self._calculate_end_position(change.position, change.content)
            buffer.delete_text(change.position, end_pos)
        elif change.type == ChangeType.REPLACE:
            # Calculate end position based on original content
            original_content = change.metadata.get("original_content", "")
            end_pos = self._calculate_end_position(change.position, original_content)
            buffer.replace_text(change.position, end_pos, change.content)
        
        # Restore original modified state to prevent double-marking
        buffer.modified = original_modified
    
    def _calculate_end_position(self, start: Position, content: str) -> Position:
        """Calculate the end position given a start position and content."""
        if not content:
            return start
        
        lines = content.split("\n")
        if len(lines) == 1:
            # Single line
            return Position(line=start.line, column=start.column + len(content))
        else:
            # Multi-line
            return Position(line=start.line + len(lines) - 1, column=len(lines[-1]))
    
    def get_current_change(self) -> Optional[Change]:
        """Get the current change in the history."""
        if 0 <= self.current_index < len(self.changes):
            return self.changes[self.current_index]
        return None
    
    def get_history_info(self) -> dict:
        """Get information about the current history state."""
        return {
            "total_changes": len(self.changes),
            "current_index": self.current_index,
            "can_undo": self.can_undo(),
            "can_redo": self.can_redo(),
            "next_undo": self.get_current_change().type.value if self.can_undo() else None,
            "next_redo": (self.changes[self.current_index + 1].type.value 
                         if self.can_redo() else None)
        }
    
    def clear(self) -> None:
        """Clear all history."""
        self.changes.clear()
        self.current_index = -1
    
    def compact_history(self, max_size: Optional[int] = None) -> None:
        """Compact the history by removing old changes."""
        if max_size is None:
            max_size = self.max_history // 2
        
        if len(self.changes) > max_size:
            # Keep the most recent changes
            changes_to_remove = len(self.changes) - max_size
            self.changes = self.changes[changes_to_remove:]
            self.current_index = max(-1, self.current_index - changes_to_remove)
    
    def get_recent_changes(self, count: int = 10) -> List[Change]:
        """Get the most recent changes."""
        start_index = max(0, len(self.changes) - count)
        return self.changes[start_index:]
    
    def create_checkpoint(self) -> int:
        """Create a checkpoint in the history and return its index."""
        return self.current_index
    
    def revert_to_checkpoint(self, checkpoint: int, buffer: TextBuffer) -> bool:
        """Revert to a specific checkpoint in the history."""
        if checkpoint < -1 or checkpoint >= len(self.changes):
            return False
        
        # Undo changes until we reach the checkpoint
        while self.current_index > checkpoint:
            self.undo(buffer)
        
        # Redo changes if we need to go forward
        while self.current_index < checkpoint:
            self.redo(buffer)
        
        return True