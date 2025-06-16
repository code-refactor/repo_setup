from typing import Optional
from pydantic import BaseModel, Field

from .models import Position, Direction
from .buffer import TextBuffer


class Cursor(BaseModel):
    """Manages cursor position and movement within a text buffer."""
    
    position: Position = Field(default_factory=lambda: Position(line=0, column=0))
    preferred_column: Optional[int] = None
    
    def move(self, direction: Direction, buffer: TextBuffer, count: int = 1) -> Position:
        """Move the cursor in the specified direction."""
        for _ in range(count):
            self._move_once(direction, buffer)
        return self.position
    
    def _move_once(self, direction: Direction, buffer: TextBuffer) -> None:
        """Move the cursor once in the specified direction."""
        if direction == Direction.LEFT:
            self._move_left(buffer)
        elif direction == Direction.RIGHT:
            self._move_right(buffer)
        elif direction == Direction.UP:
            self._move_up(buffer)
        elif direction == Direction.DOWN:
            self._move_down(buffer)
        elif direction == Direction.HOME:
            self._move_home()
        elif direction == Direction.END:
            self._move_end(buffer)
        elif direction == Direction.PAGE_UP:
            self._move_page_up(buffer)
        elif direction == Direction.PAGE_DOWN:
            self._move_page_down(buffer)
    
    def _move_left(self, buffer: TextBuffer) -> None:
        """Move cursor left by one character."""
        if self.position.column > 0:
            self.position.column -= 1
            self.preferred_column = None
        elif self.position.line > 0:
            # Move to end of previous line
            self.position.line -= 1
            line = buffer.get_line(self.position.line)
            self.position.column = len(line)
            self.preferred_column = None
    
    def _move_right(self, buffer: TextBuffer) -> None:
        """Move cursor right by one character."""
        line = buffer.get_line(self.position.line)
        if self.position.column < len(line):
            self.position.column += 1
            self.preferred_column = None
        elif self.position.line < buffer.get_line_count() - 1:
            # Move to beginning of next line
            self.position.line += 1
            self.position.column = 0
            self.preferred_column = None
    
    def _move_up(self, buffer: TextBuffer) -> None:
        """Move cursor up by one line."""
        if self.position.line > 0:
            # Store preferred column if not already set
            if self.preferred_column is None:
                self.preferred_column = self.position.column
            
            self.position.line -= 1
            line = buffer.get_line(self.position.line)
            self.position.column = min(self.preferred_column, len(line))
    
    def _move_down(self, buffer: TextBuffer) -> None:
        """Move cursor down by one line."""
        if self.position.line < buffer.get_line_count() - 1:
            # Store preferred column if not already set
            if self.preferred_column is None:
                self.preferred_column = self.position.column
            
            self.position.line += 1
            line = buffer.get_line(self.position.line)
            self.position.column = min(self.preferred_column, len(line))
    
    def _move_home(self) -> None:
        """Move cursor to the beginning of the current line."""
        self.position.column = 0
        self.preferred_column = None
    
    def _move_end(self, buffer: TextBuffer) -> None:
        """Move cursor to the end of the current line."""
        line = buffer.get_line(self.position.line)
        self.position.column = len(line)
        self.preferred_column = None
    
    def _move_page_up(self, buffer: TextBuffer, page_size: int = 20) -> None:
        """Move cursor up by one page."""
        if self.preferred_column is None:
            self.preferred_column = self.position.column
        
        self.position.line = max(0, self.position.line - page_size)
        line = buffer.get_line(self.position.line)
        self.position.column = min(self.preferred_column, len(line))
    
    def _move_page_down(self, buffer: TextBuffer, page_size: int = 20) -> None:
        """Move cursor down by one page."""
        if self.preferred_column is None:
            self.preferred_column = self.position.column
        
        self.position.line = min(buffer.get_line_count() - 1, self.position.line + page_size)
        line = buffer.get_line(self.position.line)
        self.position.column = min(self.preferred_column, len(line))
    
    def move_to_position(self, position: Position, buffer: TextBuffer) -> None:
        """Move cursor to a specific position."""
        normalized_pos = buffer._normalize_position(position)
        self.position = normalized_pos
        self.preferred_column = None
    
    def move_to_line(self, line_num: int, buffer: TextBuffer) -> None:
        """Move cursor to a specific line, keeping column if possible."""
        line_num = max(0, min(line_num, buffer.get_line_count() - 1))
        self.position.line = line_num
        
        line = buffer.get_line(line_num)
        self.position.column = min(self.position.column, len(line))
        self.preferred_column = None
    
    def move_word_left(self, buffer: TextBuffer) -> None:
        """Move cursor to the beginning of the previous word."""
        line = buffer.get_line(self.position.line)
        
        # If at beginning of line, move to previous line
        if self.position.column == 0:
            if self.position.line > 0:
                self.position.line -= 1
                line = buffer.get_line(self.position.line)
                self.position.column = len(line)
            return
        
        # Move backwards to find word boundary
        col = self.position.column - 1
        
        # Skip trailing whitespace
        while col > 0 and line[col].isspace():
            col -= 1
        
        # Skip non-whitespace characters (the word)
        while col > 0 and not line[col - 1].isspace():
            col -= 1
        
        self.position.column = col
        self.preferred_column = None
    
    def move_word_right(self, buffer: TextBuffer) -> None:
        """Move cursor to the beginning of the next word."""
        line = buffer.get_line(self.position.line)
        
        # If at end of line, move to next line
        if self.position.column >= len(line):
            if self.position.line < buffer.get_line_count() - 1:
                self.position.line += 1
                self.position.column = 0
            return
        
        # Move forward to find word boundary
        col = self.position.column
        
        # Skip current word
        while col < len(line) and not line[col].isspace():
            col += 1
        
        # Skip whitespace
        while col < len(line) and line[col].isspace():
            col += 1
        
        self.position.column = col
        self.preferred_column = None
    
    def get_position(self) -> Position:
        """Get the current cursor position."""
        return self.position.model_copy()
    
    def is_at_beginning_of_line(self) -> bool:
        """Check if cursor is at the beginning of a line."""
        return self.position.column == 0
    
    def is_at_end_of_line(self, buffer: TextBuffer) -> bool:
        """Check if cursor is at the end of a line."""
        line = buffer.get_line(self.position.line)
        return self.position.column >= len(line)
    
    def is_at_beginning_of_buffer(self) -> bool:
        """Check if cursor is at the very beginning of the buffer."""
        return self.position.line == 0 and self.position.column == 0
    
    def is_at_end_of_buffer(self, buffer: TextBuffer) -> bool:
        """Check if cursor is at the very end of the buffer."""
        if self.position.line >= buffer.get_line_count() - 1:
            line = buffer.get_line(self.position.line)
            return self.position.column >= len(line)
        return False