from abc import ABC, abstractmethod
from typing import List, Optional

from ..core.models import Position, Selection, Direction, Match
from ..core.search import SearchOptions


class EditorInterface(ABC):
    """Abstract interface for text editor functionality."""
    
    @abstractmethod
    def get_content(self) -> str:
        """Get the entire content of the editor."""
        pass
    
    @abstractmethod
    def insert_text(self, text: str, position: Optional[Position] = None) -> None:
        """Insert text at the specified position or cursor position."""
        pass
    
    @abstractmethod
    def delete_text(self, start: Position, end: Position) -> str:
        """Delete text between positions and return the deleted content."""
        pass
    
    @abstractmethod
    def replace_text(self, start: Position, end: Position, replacement: str) -> str:
        """Replace text between positions with new text."""
        pass
    
    @abstractmethod
    def get_cursor_position(self) -> Position:
        """Get the current cursor position."""
        pass
    
    @abstractmethod
    def move_cursor(self, direction: Direction, count: int = 1) -> Position:
        """Move the cursor in the specified direction."""
        pass
    
    @abstractmethod
    def move_cursor_to_position(self, position: Position) -> None:
        """Move cursor to a specific position."""
        pass
    
    @abstractmethod
    def set_selection(self, start: Position, end: Position) -> None:
        """Set the current text selection."""
        pass
    
    @abstractmethod
    def get_selection(self) -> Optional[Selection]:
        """Get the current text selection."""
        pass
    
    @abstractmethod
    def clear_selection(self) -> None:
        """Clear the current selection."""
        pass
    
    @abstractmethod
    def get_selection_text(self) -> str:
        """Get the text content of the current selection."""
        pass
    
    @abstractmethod
    def delete_selection(self) -> str:
        """Delete the current selection and return the deleted text."""
        pass
    
    @abstractmethod
    def find_text(self, pattern: str, options: Optional[SearchOptions] = None) -> List[Match]:
        """Find all occurrences of a pattern in the text."""
        pass
    
    @abstractmethod
    def find_next(self) -> Optional[Match]:
        """Find the next occurrence of the last search pattern."""
        pass
    
    @abstractmethod
    def find_previous(self) -> Optional[Match]:
        """Find the previous occurrence of the last search pattern."""
        pass
    
    @abstractmethod
    def replace_all(self, pattern: str, replacement: str, 
                   options: Optional[SearchOptions] = None) -> int:
        """Replace all occurrences of a pattern with replacement text."""
        pass
    
    @abstractmethod
    def replace_next(self, replacement: str) -> bool:
        """Replace the next occurrence of the last search pattern."""
        pass
    
    @abstractmethod
    def undo(self) -> bool:
        """Undo the last operation."""
        pass
    
    @abstractmethod
    def redo(self) -> bool:
        """Redo the last undone operation."""
        pass
    
    @abstractmethod
    def can_undo(self) -> bool:
        """Check if undo is available."""
        pass
    
    @abstractmethod
    def can_redo(self) -> bool:
        """Check if redo is available."""
        pass
    
    @abstractmethod
    def get_word_count(self) -> int:
        """Get the total word count."""
        pass
    
    @abstractmethod
    def get_char_count(self) -> int:
        """Get the total character count."""
        pass
    
    @abstractmethod
    def get_line_count(self) -> int:
        """Get the total line count."""
        pass
    
    @abstractmethod
    def is_modified(self) -> bool:
        """Check if the content has been modified."""
        pass


class ExtendedEditorInterface(EditorInterface):
    """Extended editor interface with additional functionality."""
    
    @abstractmethod
    def goto_line(self, line_number: int) -> None:
        """Go to a specific line number (1-indexed)."""
        pass
    
    @abstractmethod
    def select_all(self) -> None:
        """Select all text in the editor."""
        pass
    
    @abstractmethod
    def select_word_at_cursor(self) -> None:
        """Select the word at the cursor position."""
        pass
    
    @abstractmethod
    def select_line_at_cursor(self) -> None:
        """Select the entire line at the cursor position."""
        pass
    
    @abstractmethod
    def insert_line_above(self) -> None:
        """Insert a new line above the current line."""
        pass
    
    @abstractmethod
    def insert_line_below(self) -> None:
        """Insert a new line below the current line."""
        pass
    
    @abstractmethod
    def delete_line(self) -> None:
        """Delete the current line."""
        pass
    
    @abstractmethod
    def duplicate_line(self) -> None:
        """Duplicate the current line."""
        pass
    
    @abstractmethod
    def move_line_up(self) -> None:
        """Move the current line up."""
        pass
    
    @abstractmethod
    def move_line_down(self) -> None:
        """Move the current line down."""
        pass
    
    @abstractmethod
    def indent_selection(self) -> None:
        """Indent the current selection or line."""
        pass
    
    @abstractmethod
    def unindent_selection(self) -> None:
        """Unindent the current selection or line."""
        pass
    
    @abstractmethod
    def comment_selection(self) -> None:
        """Comment out the current selection or line."""
        pass
    
    @abstractmethod
    def uncomment_selection(self) -> None:
        """Uncomment the current selection or line."""
        pass
    
    @abstractmethod
    def toggle_comment(self) -> None:
        """Toggle comment state of the current selection or line."""
        pass