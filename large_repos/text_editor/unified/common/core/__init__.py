# Core functionality that can be used by all packages

from .models import (
    Position, Selection, Direction, ChangeType, Change, 
    NavigationHistory, Match, FileInfo, EditorState
)
from .buffer import TextBuffer
from .cursor import Cursor
from .history import History
from .file_manager import FileManager
from .search import SearchEngine, SearchOptions
from .editor import Editor

__all__ = [
    # Models
    'Position', 'Selection', 'Direction', 'ChangeType', 'Change',
    'NavigationHistory', 'Match', 'FileInfo', 'EditorState',
    # Core classes
    'TextBuffer', 'Cursor', 'History', 'FileManager', 
    'SearchEngine', 'SearchOptions', 'Editor'
]
