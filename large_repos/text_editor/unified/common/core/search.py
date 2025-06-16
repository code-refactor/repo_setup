import re
from typing import List, Optional, Iterator
from pydantic import BaseModel, Field

from .models import Position, Match
from .buffer import TextBuffer


class SearchOptions(BaseModel):
    """Options for text search operations."""
    case_sensitive: bool = False
    whole_word: bool = False
    regex: bool = False
    wrap_around: bool = True
    backward: bool = False


class SearchEngine(BaseModel):
    """Handles text search operations within the buffer."""
    
    options: SearchOptions = Field(default_factory=SearchOptions)
    last_pattern: str = ""
    last_matches: List[Match] = Field(default_factory=list)
    current_match_index: int = -1
    
    def find_all(self, buffer: TextBuffer, pattern: str, options: Optional[SearchOptions] = None) -> List[Match]:
        """Find all occurrences of the pattern in the buffer."""
        if options:
            self.options = options
        
        self.last_pattern = pattern
        self.last_matches = []
        self.current_match_index = -1
        
        if not pattern:
            return self.last_matches
        
        content = buffer.get_content()
        search_pattern = self._prepare_pattern(pattern)
        
        if not search_pattern:
            return self.last_matches
        
        try:
            for match in re.finditer(search_pattern, content, self._get_flags()):
                position = self._offset_to_position(buffer, match.start())
                groups = list(match.groups()) if match.groups() else []
                
                self.last_matches.append(Match(
                    position=position,
                    length=match.end() - match.start(),
                    content=match.group(0),
                    groups=groups
                ))
        except re.error:
            # Invalid regex pattern
            pass
        
        return self.last_matches
    
    def find_next(self, buffer: TextBuffer, start_pos: Optional[Position] = None) -> Optional[Match]:
        """Find the next occurrence of the last searched pattern."""
        if not self.last_matches:
            return None
        
        if start_pos is None:
            # Continue from current match
            if self.current_match_index >= 0:
                self.current_match_index = (self.current_match_index + 1) % len(self.last_matches)
            else:
                self.current_match_index = 0
        else:
            # Find next match after start_pos
            self.current_match_index = self._find_next_match_index(start_pos)
            if self.current_match_index == -1:
                if self.options.wrap_around:
                    self.current_match_index = 0
                else:
                    return None
        
        if 0 <= self.current_match_index < len(self.last_matches):
            return self.last_matches[self.current_match_index]
        
        return None
    
    def find_previous(self, buffer: TextBuffer, start_pos: Optional[Position] = None) -> Optional[Match]:
        """Find the previous occurrence of the last searched pattern."""
        if not self.last_matches:
            return None
        
        if start_pos is None:
            # Continue from current match
            if self.current_match_index >= 0:
                self.current_match_index = (self.current_match_index - 1) % len(self.last_matches)
            else:
                self.current_match_index = len(self.last_matches) - 1
        else:
            # Find previous match before start_pos
            self.current_match_index = self._find_previous_match_index(start_pos)
            if self.current_match_index == -1:
                if self.options.wrap_around:
                    self.current_match_index = len(self.last_matches) - 1
                else:
                    return None
        
        if 0 <= self.current_match_index < len(self.last_matches):
            return self.last_matches[self.current_match_index]
        
        return None
    
    def replace_all(self, buffer: TextBuffer, pattern: str, replacement: str, 
                   options: Optional[SearchOptions] = None) -> int:
        """Replace all occurrences of the pattern with the replacement text."""
        matches = self.find_all(buffer, pattern, options)
        if not matches:
            return 0
        
        # Sort matches in reverse order to avoid position shifts
        matches.sort(key=lambda m: (m.position.line, m.position.column), reverse=True)
        
        for match in matches:
            end_pos = Position(
                line=match.position.line,
                column=match.position.column + match.length
            )
            buffer.replace_text(match.position, end_pos, replacement)
        
        # Clear cached matches since positions have changed
        self.last_matches = []
        self.current_match_index = -1
        
        return len(matches)
    
    def replace_next(self, buffer: TextBuffer, replacement: str, 
                    start_pos: Optional[Position] = None) -> bool:
        """Replace the next occurrence of the pattern."""
        match = self.find_next(buffer, start_pos)
        if not match:
            return False
        
        end_pos = Position(
            line=match.position.line,
            column=match.position.column + match.length
        )
        buffer.replace_text(match.position, end_pos, replacement)
        
        # Update cached matches
        self._update_matches_after_replacement(match, replacement)
        
        return True
    
    def get_current_match(self) -> Optional[Match]:
        """Get the current match."""
        if 0 <= self.current_match_index < len(self.last_matches):
            return self.last_matches[self.current_match_index]
        return None
    
    def get_match_info(self) -> dict:
        """Get information about the current search state."""
        return {
            "pattern": self.last_pattern,
            "total_matches": len(self.last_matches),
            "current_index": self.current_match_index + 1 if self.current_match_index >= 0 else 0,
            "has_matches": len(self.last_matches) > 0,
            "current_match": self.get_current_match()
        }
    
    def _prepare_pattern(self, pattern: str) -> str:
        """Prepare the search pattern based on options."""
        if not self.options.regex:
            # Escape special regex characters
            pattern = re.escape(pattern)
        
        if self.options.whole_word:
            pattern = r'\b' + pattern + r'\b'
        
        return pattern
    
    def _get_flags(self) -> int:
        """Get regex flags based on options."""
        flags = 0
        if not self.options.case_sensitive:
            flags |= re.IGNORECASE
        return flags
    
    def _offset_to_position(self, buffer: TextBuffer, offset: int) -> Position:
        """Convert a character offset to a Position."""
        content = buffer.get_content()
        line = 0
        column = 0
        
        for i, char in enumerate(content):
            if i == offset:
                break
            if char == '\n':
                line += 1
                column = 0
            else:
                column += 1
        
        return Position(line=line, column=column)
    
    def _position_to_offset(self, buffer: TextBuffer, position: Position) -> int:
        """Convert a Position to a character offset."""
        offset = 0
        for line_num in range(min(position.line, buffer.get_line_count())):
            line = buffer.get_line(line_num)
            offset += len(line) + 1  # +1 for newline
        
        # Add column offset for the target line
        if position.line < buffer.get_line_count():
            line = buffer.get_line(position.line)
            offset += min(position.column, len(line))
        
        return offset
    
    def _find_next_match_index(self, start_pos: Position) -> int:
        """Find the index of the next match after the given position."""
        for i, match in enumerate(self.last_matches):
            if match.position > start_pos:
                return i
        return -1
    
    def _find_previous_match_index(self, start_pos: Position) -> int:
        """Find the index of the previous match before the given position."""
        for i in range(len(self.last_matches) - 1, -1, -1):
            match = self.last_matches[i]
            if match.position < start_pos:
                return i
        return -1
    
    def _update_matches_after_replacement(self, replaced_match: Match, replacement: str) -> None:
        """Update cached matches after a replacement operation."""
        # Calculate the position shift
        original_length = replaced_match.length
        new_length = len(replacement)
        shift = new_length - original_length
        
        # Remove the replaced match
        if self.current_match_index < len(self.last_matches):
            del self.last_matches[self.current_match_index]
        
        # Adjust positions of matches that come after the replacement
        for i in range(self.current_match_index, len(self.last_matches)):
            match = self.last_matches[i]
            if match.position.line == replaced_match.position.line:
                # Same line - adjust column
                if match.position.column > replaced_match.position.column:
                    match.position.column += shift
            # No need to adjust matches on different lines for single-line replacements
        
        # Adjust current match index
        if self.current_match_index >= len(self.last_matches):
            self.current_match_index = -1
    
    def clear_search(self) -> None:
        """Clear the current search state."""
        self.last_pattern = ""
        self.last_matches = []
        self.current_match_index = -1