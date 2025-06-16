from typing import List, Optional
from pydantic import BaseModel, Field

from .models import Position, Change, ChangeType


class TextBuffer(BaseModel):
    """Unified text buffer that manages text content as lines."""
    
    lines: List[str] = Field(default_factory=list)
    encoding: str = "utf-8"
    modified: bool = False
    
    def __init__(self, **data):
        super().__init__(**data)
        if not self.lines:
            self.lines = [""]
    
    def get_line_count(self) -> int:
        """Get the total number of lines."""
        return len(self.lines)
    
    def get_line(self, line_num: int) -> str:
        """Get the content of a specific line."""
        if 0 <= line_num < len(self.lines):
            return self.lines[line_num]
        return ""
    
    def get_content(self) -> str:
        """Get the entire buffer content as a string."""
        return "\n".join(self.lines)
    
    def get_text(self, start: Optional[Position] = None, end: Optional[Position] = None) -> str:
        """Get text content in the specified range."""
        if start is None:
            start = Position(line=0, column=0)
        if end is None:
            end = Position(line=len(self.lines) - 1, column=len(self.lines[-1]) if self.lines else 0)
        
        # Normalize positions
        start = self._normalize_position(start)
        end = self._normalize_position(end)
        
        if start == end:
            return ""
        
        if start.line == end.line:
            # Single line selection
            line = self.get_line(start.line)
            return line[start.column:end.column]
        
        # Multi-line selection
        result = []
        
        # First line
        first_line = self.get_line(start.line)
        result.append(first_line[start.column:])
        
        # Middle lines
        for line_num in range(start.line + 1, end.line):
            result.append(self.get_line(line_num))
        
        # Last line
        if end.line < len(self.lines):
            last_line = self.get_line(end.line)
            result.append(last_line[:end.column])
        
        return "\n".join(result)
    
    def insert_text(self, position: Position, text: str) -> Change:
        """Insert text at the specified position."""
        position = self._normalize_position(position)
        
        if not text:
            return Change(
                type=ChangeType.INSERT,
                position=position,
                content=""
            )
        
        lines_to_insert = text.split("\n")
        
        if len(lines_to_insert) == 1:
            # Single line insertion
            current_line = self.get_line(position.line)
            new_line = current_line[:position.column] + text + current_line[position.column:]
            self.lines[position.line] = new_line
        else:
            # Multi-line insertion
            current_line = self.get_line(position.line)
            
            # Split current line
            before = current_line[:position.column]
            after = current_line[position.column:]
            
            # Replace current line with first inserted line
            self.lines[position.line] = before + lines_to_insert[0]
            
            # Insert middle lines
            for i, line in enumerate(lines_to_insert[1:-1], 1):
                self.lines.insert(position.line + i, line)
            
            # Insert last line with remaining content
            self.lines.insert(position.line + len(lines_to_insert) - 1, lines_to_insert[-1] + after)
        
        self.modified = True
        
        return Change(
            type=ChangeType.INSERT,
            position=position,
            content=text
        )
    
    def delete_text(self, start: Position, end: Position) -> Change:
        """Delete text between positions and return the deleted content."""
        start = self._normalize_position(start)
        end = self._normalize_position(end)
        
        if start >= end:
            return Change(
                type=ChangeType.DELETE,
                position=start,
                content=""
            )
        
        deleted_content = self.get_text(start, end)
        
        if start.line == end.line:
            # Single line deletion
            line = self.get_line(start.line)
            new_line = line[:start.column] + line[end.column:]
            self.lines[start.line] = new_line
        else:
            # Multi-line deletion
            first_line = self.get_line(start.line)
            last_line = self.get_line(end.line)
            
            # Combine the parts before start and after end
            new_line = first_line[:start.column] + last_line[end.column:]
            
            # Replace first line
            self.lines[start.line] = new_line
            
            # Remove lines in between (including the last line)
            for _ in range(end.line - start.line):
                if start.line + 1 < len(self.lines):
                    del self.lines[start.line + 1]
        
        self.modified = True
        
        return Change(
            type=ChangeType.DELETE,
            position=start,
            content=deleted_content
        )
    
    def replace_text(self, start: Position, end: Position, replacement: str) -> Change:
        """Replace text between positions."""
        start = self._normalize_position(start)
        end = self._normalize_position(end)
        
        original_content = self.get_text(start, end)
        
        # Delete the old content first
        self.delete_text(start, end)
        
        # Insert the new content
        self.insert_text(start, replacement)
        
        return Change(
            type=ChangeType.REPLACE,
            position=start,
            content=replacement,
            metadata={"original_content": original_content}
        )
    
    def get_word_count(self) -> int:
        """Get the total word count."""
        content = self.get_content()
        if not content.strip():
            return 0
        return len(content.split())
    
    def get_char_count(self) -> int:
        """Get the total character count."""
        return len(self.get_content())
    
    def get_char_count_no_spaces(self) -> int:
        """Get character count excluding whitespace."""
        content = self.get_content()
        return len(content.replace(" ", "").replace("\t", "").replace("\n", ""))
    
    def _normalize_position(self, position: Position) -> Position:
        """Normalize a position to ensure it's within valid bounds."""
        line_num = max(0, min(position.line, len(self.lines) - 1))
        line = self.get_line(line_num)
        column = max(0, min(position.column, len(line)))
        return Position(line=line_num, column=column)
    
    def is_valid_position(self, position: Position) -> bool:
        """Check if a position is valid within the buffer."""
        if position.line < 0 or position.line >= len(self.lines):
            return False
        line = self.get_line(position.line)
        return 0 <= position.column <= len(line)
    
    def set_content(self, content: str) -> None:
        """Set the entire buffer content."""
        self.lines = content.split("\n") if content else [""]
        self.modified = True
    
    def clear(self) -> None:
        """Clear all content from the buffer."""
        self.lines = [""]
        self.modified = True