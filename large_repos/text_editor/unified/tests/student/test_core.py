"""
Tests for the core text editor functionality.
"""
import pytest
import time

from common.core import TextBuffer, Cursor, History, FileManager, Editor, Position
from text_editor.core import Editor as StudentEditor


class TestTextBuffer:
    def test_initialization(self):
        """Test that the buffer is initialized correctly."""
        buffer = TextBuffer()
        assert buffer.lines == [""]
        
        buffer = TextBuffer()
        buffer.set_content("Hello\nWorld")
        assert buffer.lines == ["Hello", "World"]
    
    def test_get_content(self):
        """Test getting the entire content of the buffer."""
        buffer = TextBuffer()
        buffer.set_content("Hello\nWorld")
        assert buffer.get_content() == "Hello\nWorld"
        
        buffer = TextBuffer()
        assert buffer.get_content() == ""
    
    def test_get_line(self):
        """Test getting a specific line from the buffer."""
        buffer = TextBuffer()
        buffer.set_content("Hello\nWorld")
        assert buffer.get_line(0) == "Hello"
        assert buffer.get_line(1) == "World"
        
        # get_line returns empty string for invalid lines, not IndexError
        assert buffer.get_line(2) == ""
    
    def test_get_line_count(self):
        """Test getting the number of lines in the buffer."""
        buffer = TextBuffer()
        buffer.set_content("Hello\nWorld")
        assert buffer.get_line_count() == 2
        
        buffer = TextBuffer()
        assert buffer.get_line_count() == 1
    
    def test_insert_text_single_line(self):
        """Test inserting text within a single line."""
        buffer = TextBuffer()
        buffer.set_content("Hello World")
        buffer.insert_text(Position(line=0, column=5), " Beautiful")
        assert buffer.get_content() == "Hello Beautiful World"
    
    def test_insert_text_multiline(self):
        """Test inserting text with multiple lines."""
        buffer = TextBuffer()
        buffer.set_content("Hello World")
        buffer.insert_text(Position(line=0, column=5), " Beautiful\nAmazing")
        assert buffer.get_content() == "Hello Beautiful\nAmazing World"
    
    def test_insert_text_at_end(self):
        """Test inserting text at the end of a line."""
        buffer = TextBuffer()
        buffer.set_content("Hello")
        buffer.insert_text(Position(line=0, column=5), " World")
        assert buffer.get_content() == "Hello World"
    
    def test_delete_text_single_line(self):
        """Test deleting text within a single line."""
        buffer = TextBuffer()
        buffer.set_content("Hello Beautiful World")
        change = buffer.delete_text(Position(line=0, column=5), Position(line=0, column=15))
        assert change.content == " Beautiful"
        assert buffer.get_content() == "Hello World"
    
    def test_delete_text_multiline(self):
        """Test deleting text across multiple lines."""
        buffer = TextBuffer()
        buffer.set_content("Hello\nBeautiful\nWorld")
        change = buffer.delete_text(Position(line=0, column=5), Position(line=2, column=0))
        assert change.content == "\nBeautiful\n"
        assert buffer.get_content() == "HelloWorld"
    
    def test_replace_text(self):
        """Test replacing text in the buffer."""
        buffer = TextBuffer()
        buffer.set_content("Hello World")
        change = buffer.replace_text(Position(line=0, column=0), Position(line=0, column=5), "Hi")
        assert change.metadata["original_content"] == "Hello"
        assert buffer.get_content() == "Hi World"
    
    def test_clear(self):
        """Test clearing the buffer."""
        buffer = TextBuffer()
        buffer.set_content("Hello World")
        buffer.clear()
        assert buffer.get_content() == ""
        assert buffer.get_line_count() == 1


class TestCursor:
    def test_initialization(self):
        """Test that the cursor is initialized correctly."""
        buffer = TextBuffer()
        buffer.set_content("Hello World")
        cursor = Cursor()
        assert cursor.position.line == 0
        assert cursor.position.column == 0
    
    def test_move_to(self):
        """Test moving the cursor to a specific position."""
        buffer = TextBuffer()
        buffer.set_content("Hello\nWorld")
        cursor = Cursor()
        
        cursor.move_to_position(Position(line=1, column=3), buffer)
        assert cursor.position.line == 1
        assert cursor.position.column == 3
        
        # Common library normalizes positions instead of raising errors
        cursor.move_to_position(Position(line=2, column=0), buffer)
        assert cursor.position.line == 1  # Normalized to last line
        
        cursor.move_to_position(Position(line=1, column=10), buffer)
        assert cursor.position.column == 5  # Normalized to line end
    
    def test_get_position(self):
        """Test getting the cursor position."""
        buffer = TextBuffer()
        buffer.set_content("Hello\nWorld")
        cursor = Cursor()
        
        cursor.move_to_position(Position(line=1, column=3), buffer)
        pos = cursor.get_position()
        assert pos.line == 1
        assert pos.column == 3
    
    def test_move_up(self):
        """Test moving the cursor up."""
        buffer = TextBuffer()
        buffer.set_content("Hello\nWorld")
        cursor = Cursor()
        
        cursor.move_to_position(Position(line=1, column=3), buffer)
        from common.core.models import Direction
        cursor.move(Direction.UP, buffer)
        pos = cursor.get_position()
        assert pos.line == 0
        assert pos.column == 3
        
        cursor.move(Direction.UP, buffer)  # Already at the top, should stay at line 0
        pos = cursor.get_position()
        assert pos.line == 0
        assert pos.column == 3
    
    def test_move_down(self):
        """Test moving the cursor down."""
        buffer = TextBuffer()
        buffer.set_content("Hello\nWorld")
        cursor = Cursor()
        from common.core.models import Direction
        
        cursor.move(Direction.DOWN, buffer)
        pos = cursor.get_position()
        assert pos.line == 1
        assert pos.column == 0
        
        cursor.move(Direction.DOWN, buffer)  # Already at the bottom, should stay at line 1
        pos = cursor.get_position()
        assert pos.line == 1
        assert pos.column == 0
    
    def test_move_left(self):
        """Test moving the cursor left."""
        buffer = TextBuffer()
        buffer.set_content("Hello\nWorld")
        cursor = Cursor()
        from common.core.models import Direction
        
        cursor.move_to_position(Position(line=0, column=3), buffer)
        cursor.move(Direction.LEFT, buffer)
        pos = cursor.get_position()
        assert pos.line == 0
        assert pos.column == 2
        
        cursor.move_to_position(Position(line=1, column=0), buffer)
        cursor.move(Direction.LEFT, buffer)  # Should move to the end of the previous line
        pos = cursor.get_position()
        assert pos.line == 0
        assert pos.column == 5
    
    def test_move_right(self):
        """Test moving the cursor right."""
        buffer = TextBuffer()
        buffer.set_content("Hello\nWorld")
        cursor = Cursor()
        from common.core.models import Direction
        
        cursor.move(Direction.RIGHT, buffer)
        pos = cursor.get_position()
        assert pos.line == 0
        assert pos.column == 1
        
        cursor.move_to_position(Position(line=0, column=5), buffer)
        cursor.move(Direction.RIGHT, buffer)  # Should move to the beginning of the next line
        pos = cursor.get_position()
        assert pos.line == 1
        assert pos.column == 0
    
    def test_move_to_line_start(self):
        """Test moving the cursor to the start of the line."""
        buffer = TextBuffer()
        buffer.set_content("Hello\nWorld")
        cursor = Cursor()
        from common.core.models import Direction
        
        cursor.move_to_position(Position(line=0, column=3), buffer)
        cursor.move(Direction.HOME, buffer)
        pos = cursor.get_position()
        assert pos.line == 0
        assert pos.column == 0
    
    def test_move_to_line_end(self):
        """Test moving the cursor to the end of the line."""
        buffer = TextBuffer()
        buffer.set_content("Hello\nWorld")
        cursor = Cursor()
        from common.core.models import Direction
        
        cursor.move(Direction.END, buffer)
        pos = cursor.get_position()
        assert pos.line == 0
        assert pos.column == 5
    
    def test_move_to_buffer_start(self):
        """Test moving the cursor to the start of the buffer."""
        buffer = TextBuffer()
        buffer.set_content("Hello\nWorld")
        cursor = Cursor()
        
        cursor.move_to_position(Position(line=1, column=3), buffer)
        cursor.move_to_position(Position(line=0, column=0), buffer)
        pos = cursor.get_position()
        assert pos.line == 0
        assert pos.column == 0
    
    def test_move_to_buffer_end(self):
        """Test moving the cursor to the end of the buffer."""
        buffer = TextBuffer()
        buffer.set_content("Hello\nWorld")
        cursor = Cursor()
        
        cursor.move_to_position(Position(line=1, column=5), buffer)
        pos = cursor.get_position()
        assert pos.line == 1
        assert pos.column == 5


class TestHistory:
    def test_record_operations(self):
        """Test recording different types of operations."""
        from common.core.models import Change, ChangeType
        history = History()
        
        # Record an insert
        change = Change(type=ChangeType.INSERT, position=Position(line=0, column=0), content="Hello")
        history.record_change(change)
        assert len(history.changes) == 1
        assert history.changes[0].type == ChangeType.INSERT
        
        # Record a delete
        change = Change(type=ChangeType.DELETE, position=Position(line=0, column=0), content="Hello")
        history.record_change(change)
        assert len(history.changes) == 2
        assert history.changes[1].type == ChangeType.DELETE
        
        # Record a replace
        change = Change(type=ChangeType.REPLACE, position=Position(line=0, column=0), content="Hi", metadata={"original_content": "Hello"})
        history.record_change(change)
        assert len(history.changes) == 3
        assert history.changes[2].type == ChangeType.REPLACE
    
    def test_undo_redo(self):
        """Test the undo and redo functionality."""
        from common.core.models import Change, ChangeType
        history = History()
        buffer = TextBuffer()
        
        # Initial state: nothing to undo or redo
        assert not history.can_undo()
        assert not history.can_redo()
        
        # Record an operation
        change = Change(type=ChangeType.INSERT, position=Position(line=0, column=0), content="Hello")
        history.record_change(change)
        assert history.can_undo()
        assert not history.can_redo()
        
        # Undo the operation
        operation = history.undo(buffer)
        assert operation.type == ChangeType.INSERT
        assert not history.can_undo()
        assert history.can_redo()
        
        # Redo the operation
        operation = history.redo(buffer)
        assert operation.type == ChangeType.INSERT
        assert history.can_undo()
        assert not history.can_redo()
    
    def test_clear_history(self):
        """Test clearing the history."""
        from common.core.models import Change, ChangeType
        history = History()
        
        change = Change(type=ChangeType.INSERT, position=Position(line=0, column=0), content="Hello")
        history.record_change(change)
        history.clear()
        
        assert not history.can_undo()
        assert not history.can_redo()


class TestEditor:
    def test_initialization(self):
        """Test that the editor is initialized correctly."""
        editor = StudentEditor("Hello World")
        assert editor.get_content() == "Hello World"
        assert editor.get_cursor_position() == (0, 0)
    
    def test_insert_text(self):
        """Test inserting text at the cursor position."""
        editor = StudentEditor("Hello")
        editor.set_cursor_position(0, 5)
        editor.insert_text(" World")
        assert editor.get_content() == "Hello World"
        assert editor.get_cursor_position() == (0, 11)
    
    def test_delete_char_before_cursor(self):
        """Test deleting the character before the cursor."""
        editor = StudentEditor("Hello World")
        editor.set_cursor_position(0, 11)
        editor.delete_char_before_cursor()
        assert editor.get_content() == "Hello Worl"
        assert editor.get_cursor_position() == (0, 10)
    
    def test_delete_char_after_cursor(self):
        """Test deleting the character after the cursor."""
        editor = StudentEditor("Hello World")
        editor.set_cursor_position(0, 5)
        editor.delete_char_after_cursor()
        assert editor.get_content() == "HelloWorld"
        assert editor.get_cursor_position() == (0, 5)
    
    def test_new_line(self):
        """Test inserting a new line at the cursor position."""
        editor = StudentEditor("Hello World")
        editor.set_cursor_position(0, 5)
        editor.new_line()
        assert editor.get_content() == "Hello\n World"
        assert editor.get_cursor_position() == (1, 0)
    
    def test_move_cursor(self):
        """Test moving the cursor in different directions."""
        editor = StudentEditor("Hello\nWorld")
        
        editor.move_cursor("right", 2)
        assert editor.get_cursor_position() == (0, 2)
        
        editor.move_cursor("down")
        assert editor.get_cursor_position() == (1, 2)
        
        editor.move_cursor("left")
        assert editor.get_cursor_position() == (1, 1)
        
        editor.move_cursor("up")
        assert editor.get_cursor_position() == (0, 1)
        
        editor.move_cursor("line_end")
        assert editor.get_cursor_position() == (0, 5)
        
        editor.move_cursor("line_start")
        assert editor.get_cursor_position() == (0, 0)
        
        editor.move_cursor("buffer_end")
        assert editor.get_cursor_position() == (1, 5)
        
        editor.move_cursor("buffer_start")
        assert editor.get_cursor_position() == (0, 0)
    
    def test_replace_text(self):
        """Test replacing text between specified positions."""
        editor = StudentEditor("Hello World")
        editor.replace_text(0, 0, 0, 5, "Hi")
        assert editor.get_content() == "Hi World"
    
    def test_undo_redo(self):
        """Test undoing and redoing operations."""
        editor = StudentEditor()
        
        # Insert some text
        editor.insert_text("Hello")
        assert editor.get_content() == "Hello"
        
        # Undo the insertion
        assert editor.undo()
        assert editor.get_content() == ""
        
        # Redo the insertion
        assert editor.redo()
        assert editor.get_content() == "Hello"
        
        # Delete some text
        editor.set_cursor_position(0, 5)
        editor.delete_char_before_cursor()
        assert editor.get_content() == "Hell"
        
        # Undo the deletion
        assert editor.undo()
        assert editor.get_content() == "Hello"
        
        # Redo the deletion
        assert editor.redo()
        assert editor.get_content() == "Hell"
    
    def test_clear(self):
        """Test clearing the editor."""
        editor = StudentEditor("Hello World")
        editor.clear()
        assert editor.get_content() == ""
        assert editor.get_cursor_position() == (0, 0)


class TestFileManager:
    def test_file_operations(self, tmp_path):
        """Test file operations using a temporary file."""
        file_path = tmp_path / "test.txt"
        file_manager = FileManager()
        buffer = TextBuffer()
        buffer.set_content("Hello World")
        
        # Test saving a file
        file_manager.save_as_file(buffer, str(file_path))
        assert file_path.read_text() == "Hello World"
        
        # Test loading a file
        buffer2 = TextBuffer()
        success = file_manager.load_file(str(file_path), buffer2)
        assert success
        assert buffer2.get_content() == "Hello World"
        
        # Test file manager has file
        assert file_manager.has_file()