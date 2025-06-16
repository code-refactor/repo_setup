# Core text editor functionality
# Now using the unified common library for core functionality

from .editor import Editor

# Re-export common components for backward compatibility
from common.core import (
    TextBuffer, Cursor, History, FileManager,
    Position, Direction, ChangeType
)

__all__ = [
    'Editor', 'TextBuffer', 'Cursor', 'History', 'FileManager',
    'Position', 'Direction', 'ChangeType'
]