from typing import List, Optional
from pydantic import BaseModel, Field

from .models import Position, Selection, Direction, Change, EditorState
from .buffer import TextBuffer
from .cursor import Cursor
from .history import History
from .file_manager import FileManager
from .search import SearchEngine, SearchOptions, Match


class Editor(BaseModel):
    """Main editor class that orchestrates all core functionality."""
    
    buffer: TextBuffer = Field(default_factory=TextBuffer)
    cursor: Cursor = Field(default_factory=Cursor)
    history: History = Field(default_factory=History)
    file_manager: FileManager = Field(default_factory=FileManager)
    search_engine: SearchEngine = Field(default_factory=SearchEngine)
    selection: Optional[Selection] = None
    
    def get_content(self) -> str:
        """Get the entire buffer content."""
        return self.buffer.get_content()
    
    def insert_text(self, text: str, position: Optional[Position] = None) -> None:
        """Insert text at the specified position or cursor position."""
        if position is None:
            position = self.cursor.get_position()
        
        # Record the change
        change = self.buffer.insert_text(position, text)
        self.history.record_change(change)
        
        # Update cursor position
        if position == self.cursor.get_position():
            # Move cursor to end of inserted text
            lines = text.split('\n')
            if len(lines) == 1:
                new_pos = Position(line=position.line, column=position.column + len(text))
            else:
                new_pos = Position(line=position.line + len(lines) - 1, column=len(lines[-1]))
            self.cursor.move_to_position(new_pos, self.buffer)
        
        # Clear selection if it exists
        self.selection = None
    
    def delete_text(self, start: Position, end: Position) -> str:
        """Delete text between positions."""
        change = self.buffer.delete_text(start, end)
        self.history.record_change(change)
        
        # Move cursor to start position
        self.cursor.move_to_position(start, self.buffer)
        
        # Clear selection
        self.selection = None
        
        return change.content
    
    def replace_text(self, start: Position, end: Position, replacement: str) -> str:
        """Replace text between positions."""
        change = self.buffer.replace_text(start, end, replacement)
        self.history.record_change(change)
        
        # Move cursor to end of replacement
        lines = replacement.split('\n')
        if len(lines) == 1:
            new_pos = Position(line=start.line, column=start.column + len(replacement))
        else:
            new_pos = Position(line=start.line + len(lines) - 1, column=len(lines[-1]))
        self.cursor.move_to_position(new_pos, self.buffer)
        
        # Clear selection
        self.selection = None
        
        return change.metadata.get("original_content", "")
    
    def delete_selection(self) -> str:
        """Delete the current selection."""
        if not self.selection or self.selection.is_empty:
            return ""
        
        return self.delete_text(self.selection.start, self.selection.end)
    
    def get_selection_text(self) -> str:
        """Get the text of the current selection."""
        if not self.selection or self.selection.is_empty:
            return ""
        
        return self.buffer.get_text(self.selection.start, self.selection.end)
    
    def move_cursor(self, direction: Direction, count: int = 1) -> Position:
        """Move the cursor in the specified direction."""
        return self.cursor.move(direction, self.buffer, count)
    
    def move_cursor_to_position(self, position: Position) -> None:
        """Move cursor to a specific position."""
        self.cursor.move_to_position(position, self.buffer)
    
    def get_cursor_position(self) -> Position:
        """Get the current cursor position."""
        return self.cursor.get_position()
    
    def set_selection(self, start: Position, end: Position) -> None:
        """Set the current selection."""
        self.selection = Selection(start=start, end=end)
    
    def clear_selection(self) -> None:
        """Clear the current selection."""
        self.selection = None
    
    def select_all(self) -> None:
        """Select all text in the buffer."""
        start = Position(line=0, column=0)
        last_line = self.buffer.get_line_count() - 1
        last_line_content = self.buffer.get_line(last_line)
        end = Position(line=last_line, column=len(last_line_content))
        self.set_selection(start, end)
    
    def select_word_at_cursor(self) -> None:
        """Select the word at the cursor position."""
        pos = self.cursor.get_position()
        line = self.buffer.get_line(pos.line)
        
        if pos.column >= len(line):
            return
        
        # Find word boundaries
        start_col = pos.column
        end_col = pos.column
        
        # Move start to beginning of word
        while start_col > 0 and not line[start_col - 1].isspace():
            start_col -= 1
        
        # Move end to end of word
        while end_col < len(line) and not line[end_col].isspace():
            end_col += 1
        
        start_pos = Position(line=pos.line, column=start_col)
        end_pos = Position(line=pos.line, column=end_col)
        self.set_selection(start_pos, end_pos)
    
    def select_line_at_cursor(self) -> None:
        """Select the entire line at the cursor position."""
        pos = self.cursor.get_position()
        start_pos = Position(line=pos.line, column=0)
        line = self.buffer.get_line(pos.line)
        end_pos = Position(line=pos.line, column=len(line))
        self.set_selection(start_pos, end_pos)
    
    def undo(self) -> bool:
        """Undo the last change."""
        change = self.history.undo(self.buffer)
        if change:
            # Move cursor to the change position
            self.cursor.move_to_position(change.position, self.buffer)
            return True
        return False
    
    def redo(self) -> bool:
        """Redo the next change."""
        change = self.history.redo(self.buffer)
        if change:
            # Move cursor to the change position
            self.cursor.move_to_position(change.position, self.buffer)
            return True
        return False
    
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return self.history.can_undo()
    
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return self.history.can_redo()
    
    def find_text(self, pattern: str, options: Optional[SearchOptions] = None) -> List[Match]:
        """Find all occurrences of a pattern."""
        return self.search_engine.find_all(self.buffer, pattern, options)
    
    def find_next(self) -> Optional[Match]:
        """Find the next occurrence of the last search pattern."""
        match = self.search_engine.find_next(self.buffer, self.cursor.get_position())
        if match:
            self.cursor.move_to_position(match.position, self.buffer)
        return match
    
    def find_previous(self) -> Optional[Match]:
        """Find the previous occurrence of the last search pattern."""
        match = self.search_engine.find_previous(self.buffer, self.cursor.get_position())
        if match:
            self.cursor.move_to_position(match.position, self.buffer)
        return match
    
    def replace_all(self, pattern: str, replacement: str, 
                   options: Optional[SearchOptions] = None) -> int:
        """Replace all occurrences of a pattern."""
        return self.search_engine.replace_all(self.buffer, pattern, replacement, options)
    
    def replace_next(self, replacement: str) -> bool:
        """Replace the next occurrence of the last search pattern."""
        return self.search_engine.replace_next(self.buffer, replacement, self.cursor.get_position())
    
    def load_file(self, path: str) -> bool:
        """Load a file into the editor."""
        success = self.file_manager.load_file(path, self.buffer)
        if success:
            # Reset cursor and history
            self.cursor.move_to_position(Position(line=0, column=0), self.buffer)
            self.history.clear()
            self.selection = None
        return success
    
    def save_file(self, path: Optional[str] = None) -> bool:
        """Save the current buffer to a file."""
        return self.file_manager.save_file(self.buffer, path)
    
    def save_as_file(self, path: str) -> bool:
        """Save the current buffer to a new file."""
        return self.file_manager.save_as_file(self.buffer, path)
    
    def new_file(self) -> None:
        """Create a new file."""
        self.file_manager.new_file(self.buffer)
        self.cursor.move_to_position(Position(line=0, column=0), self.buffer)
        self.history.clear()
        self.selection = None
    
    def is_modified(self) -> bool:
        """Check if the buffer has been modified."""
        return self.buffer.modified
    
    def get_file_name(self) -> str:
        """Get the name of the current file."""
        return self.file_manager.get_file_name()
    
    def get_file_path(self) -> Optional[str]:
        """Get the path of the current file."""
        return self.file_manager.current_file.path
    
    def get_word_count(self) -> int:
        """Get the word count of the buffer."""
        return self.buffer.get_word_count()
    
    def get_char_count(self) -> int:
        """Get the character count of the buffer."""
        return self.buffer.get_char_count()
    
    def get_line_count(self) -> int:
        """Get the line count of the buffer."""
        return self.buffer.get_line_count()
    
    def get_editor_state(self) -> EditorState:
        """Get the current state of the editor."""
        return EditorState(
            cursor_position=self.cursor.get_position(),
            selection=self.selection,
            file_info=self.file_manager.get_file_info(),
            modified=self.is_modified()
        )
    
    def goto_line(self, line_number: int) -> None:
        """Go to a specific line number (1-indexed)."""
        line_index = max(0, line_number - 1)
        self.cursor.move_to_line(line_index, self.buffer)
    
    def get_line_at_cursor(self) -> str:
        """Get the content of the line at the cursor position."""
        pos = self.cursor.get_position()
        return self.buffer.get_line(pos.line)
    
    def insert_line_above(self) -> None:
        """Insert a new line above the current line."""
        pos = self.cursor.get_position()
        line_start = Position(line=pos.line, column=0)
        self.insert_text("\n", line_start)
        # Move cursor to the new line
        self.cursor.move_to_position(line_start, self.buffer)
    
    def insert_line_below(self) -> None:
        """Insert a new line below the current line."""
        pos = self.cursor.get_position()
        line = self.buffer.get_line(pos.line)
        line_end = Position(line=pos.line, column=len(line))
        self.insert_text("\n", line_end)
    
    def delete_line(self) -> None:
        """Delete the current line."""
        pos = self.cursor.get_position()
        line_start = Position(line=pos.line, column=0)
        
        if pos.line < self.buffer.get_line_count() - 1:
            # Not the last line - include the newline
            line_end = Position(line=pos.line + 1, column=0)
        else:
            # Last line - just delete the line content
            line = self.buffer.get_line(pos.line)
            line_end = Position(line=pos.line, column=len(line))
        
        self.delete_text(line_start, line_end)
    
    def duplicate_line(self) -> None:
        """Duplicate the current line."""
        pos = self.cursor.get_position()
        line = self.buffer.get_line(pos.line)
        line_end = Position(line=pos.line, column=len(line))
        self.insert_text("\n" + line, line_end)