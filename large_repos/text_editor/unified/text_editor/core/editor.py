"""
Core editor implementation that combines buffer and cursor functionality.
Refactored to use the unified common library.
"""
from typing import List, Optional, Dict, Any, Tuple
from pydantic import BaseModel, Field
import time

from common.core import Editor as CommonEditor, Position, Direction


class Editor(BaseModel):
    """
    Core editor class that combines buffer and cursor functionality.
    
    This class wraps the common editor and provides backward compatibility
    for the student persona while leveraging the unified common library.
    """
    common_editor: CommonEditor = Field(default_factory=CommonEditor, exclude=True)

    def __init__(self, content: str = "", file_path: Optional[str] = None):
        """
        Initialize a new editor with the given content.

        Args:
            content: Initial text content (defaults to empty string)
            file_path: Path to the file being edited (optional)
        """
        super().__init__()
        self.common_editor = CommonEditor()
        
        if content:
            self.common_editor.buffer.set_content(content)
        
        if file_path:
            self.common_editor.load_file(file_path)
    
    def get_content(self) -> str:
        """
        Get the entire content of the editor.
        
        Returns:
            The content as a string
        """
        return self.common_editor.get_content()
    
    def get_cursor_position(self) -> Tuple[int, int]:
        """
        Get the current cursor position.
        
        Returns:
            A tuple of (line, column)
        """
        pos = self.common_editor.get_cursor_position()
        return (pos.line, pos.column)
    
    def insert_text(self, text: str) -> None:
        """
        Insert text at the current cursor position.

        Args:
            text: The text to insert
        """
        self.common_editor.insert_text(text)
    
    def delete_char_before_cursor(self) -> None:
        """Delete the character before the cursor (backspace operation)."""
        pos = self.common_editor.get_cursor_position()
        
        if pos.column > 0:
            # Delete character in the current line
            start = Position(line=pos.line, column=pos.column - 1)
            end = Position(line=pos.line, column=pos.column)
            self.common_editor.delete_text(start, end)
        elif pos.line > 0:
            # At the beginning of a line, join with the previous line
            prev_line_length = len(self.common_editor.buffer.get_line(pos.line - 1))
            start = Position(line=pos.line - 1, column=prev_line_length)
            end = Position(line=pos.line, column=0)
            self.common_editor.delete_text(start, end)
    
    def delete_char_after_cursor(self) -> None:
        """Delete the character after the cursor (delete key operation)."""
        pos = self.common_editor.get_cursor_position()
        line_length = len(self.common_editor.buffer.get_line(pos.line))

        if pos.column < line_length:
            # Delete character in the current line
            start = Position(line=pos.line, column=pos.column)
            end = Position(line=pos.line, column=pos.column + 1)
            self.common_editor.delete_text(start, end)
        elif pos.line < self.common_editor.buffer.get_line_count() - 1:
            # At the end of a line, join with the next line
            start = Position(line=pos.line, column=line_length)
            end = Position(line=pos.line + 1, column=0)
            self.common_editor.delete_text(start, end)
    
    def new_line(self) -> None:
        """Insert a new line at the cursor position."""
        self.insert_text("\n")
    
    def move_cursor(self, direction: str, count: int = 1) -> None:
        """
        Move the cursor in the specified direction.
        
        Args:
            direction: One of "up", "down", "left", "right", 
                      "line_start", "line_end", "buffer_start", "buffer_end"
            count: Number of units to move (for up, down, left, right)
        """
        # Map old direction strings to new Direction enum
        direction_map = {
            "up": Direction.UP,
            "down": Direction.DOWN,
            "left": Direction.LEFT,
            "right": Direction.RIGHT,
            "line_start": Direction.HOME,
            "line_end": Direction.END,
            "buffer_start": Direction.HOME,  # Will move to beginning of buffer
            "buffer_end": Direction.END      # Will move to end of buffer
        }
        
        if direction in direction_map:
            if direction in ["up", "down", "left", "right"]:
                self.common_editor.move_cursor(direction_map[direction], count)
            elif direction == "line_start":
                self.common_editor.move_cursor(Direction.HOME)
            elif direction == "line_end":
                self.common_editor.move_cursor(Direction.END)
            elif direction == "buffer_start":
                self.common_editor.move_cursor_to_position(Position(line=0, column=0))
            elif direction == "buffer_end":
                last_line = self.common_editor.buffer.get_line_count() - 1
                last_col = len(self.common_editor.buffer.get_line(last_line))
                self.common_editor.move_cursor_to_position(Position(line=last_line, column=last_col))
        else:
            raise ValueError(f"Unknown direction: {direction}")
    
    def set_cursor_position(self, line: int, column: int) -> None:
        """
        Set the cursor to the specified position.
        
        Args:
            line: Line number (0-indexed)
            column: Column number (0-indexed)
        """
        self.common_editor.move_cursor_to_position(Position(line=line, column=column))
    
    def get_line(self, line_number: int) -> str:
        """
        Get a specific line from the buffer.
        
        Args:
            line_number: The line number to retrieve (0-indexed)
            
        Returns:
            The requested line as a string
        """
        return self.common_editor.buffer.get_line(line_number)
    
    def get_line_count(self) -> int:
        """
        Get the total number of lines in the buffer.
        
        Returns:
            The number of lines
        """
        return self.common_editor.buffer.get_line_count()
    
    def replace_text(self, start_line: int, start_col: int,
                    end_line: int, end_col: int, new_text: str) -> str:
        """
        Replace text between the specified positions with new text.

        Args:
            start_line: Starting line number (0-indexed)
            start_col: Starting column number (0-indexed)
            end_line: Ending line number (0-indexed)
            end_col: Ending column number (0-indexed)
            new_text: The text to insert

        Returns:
            The replaced text
        """
        start = Position(line=start_line, column=start_col)
        end = Position(line=end_line, column=end_col)
        return self.common_editor.replace_text(start, end, new_text)
    
    def clear(self) -> None:
        """Clear the editor, removing all content."""
        self.common_editor.buffer.clear()
        self.common_editor.move_cursor_to_position(Position(line=0, column=0))

    def undo(self) -> bool:
        """
        Undo the last operation.

        Returns:
            True if an operation was undone, False otherwise
        """
        return self.common_editor.undo()

    def redo(self) -> bool:
        """
        Redo the last undone operation.

        Returns:
            True if an operation was redone, False otherwise
        """
        return self.common_editor.redo()

    def load_file(self, file_path: str) -> None:
        """
        Load content from a file.

        Args:
            file_path: Path to the file to load
        """
        self.common_editor.load_file(file_path)

    def save_file(self, file_path: Optional[str] = None) -> None:
        """
        Save content to a file.

        Args:
            file_path: Path to save to (if None, uses current path)
        """
        self.common_editor.save_file(file_path)

    def get_current_file_path(self) -> Optional[str]:
        """
        Get the current file path.

        Returns:
            The current file path, or None if no file is open
        """
        return self.common_editor.get_file_path()

    def is_file_modified(self) -> bool:
        """
        Check if the file has been modified since it was last saved.

        Returns:
            True if the file has been modified, False otherwise
        """
        return self.common_editor.is_modified()
    
    # Backward compatibility properties to access common editor components
    @property
    def buffer(self):
        """Access to the underlying buffer for backward compatibility."""
        return self.common_editor.buffer
    
    @property
    def cursor(self):
        """Access to the underlying cursor for backward compatibility."""
        return self.common_editor.cursor
    
    @property
    def history(self):
        """Access to the underlying history for backward compatibility."""
        return self.common_editor.history
    
    @property
    def file_manager(self):
        """Access to the underlying file manager for backward compatibility."""
        return self.common_editor.file_manager