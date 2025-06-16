"""Focus mode system for the writer text editor."""

from __future__ import annotations
import time
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union, Any
from pydantic import BaseModel, Field

from writer_text_editor.document import Document, Section, TextSegment
# Import common models for enhanced positioning
from common.core.models import Position, Selection


class FocusLevel(str, Enum):
    """The level of focus."""
    
    PARAGRAPH = "paragraph"
    SENTENCE = "sentence"
    SECTION = "section"


class FocusContext(BaseModel):
    """Context information about the focused element."""
    
    document: Document
    section: Section
    segment: TextSegment
    level: FocusLevel
    start_time: float = Field(default_factory=time.time)
    # Enhanced positioning using common models
    focus_position: Optional[Position] = None  # Current cursor position within focus
    focus_selection: Optional[Selection] = None  # Selected text within focus
    
    class Config:
        arbitrary_types_allowed = True
    
    def get_focus_area(self) -> Optional[Selection]:
        """Get the selection representing the focused area."""
        if self.segment.start_position and self.segment.end_position:
            return Selection(
                start=self.segment.start_position,
                end=self.segment.end_position
            )
        return None
    
    def set_cursor_position(self, position: Position) -> bool:
        """Set the cursor position within the focused segment."""
        focus_area = self.get_focus_area()
        if focus_area and focus_area.start <= position <= focus_area.end:
            self.focus_position = position
            return True
        return False
    
    def set_selection(self, selection: Selection) -> bool:
        """Set a selection within the focused segment."""
        focus_area = self.get_focus_area()
        if focus_area and focus_area.start <= selection.start and selection.end <= focus_area.end:
            self.focus_selection = selection
            return True
        return False


class FocusMode:
    """The focus mode system."""
    
    def __init__(self, document: Document):
        """Initialize the focus mode system with the given document."""
        self.document = document
        self.active_focus: Optional[FocusContext] = None
        self.focus_history: List[FocusContext] = []
    
    def is_active(self) -> bool:
        """Check if focus mode is currently active."""
        return self.active_focus is not None
    
    def get_focus_context(self) -> Optional[FocusContext]:
        """Get the current focus context if focus mode is active."""
        return self.active_focus
    
    def enter_focus(
        self, 
        section_index: int, 
        segment_index: int, 
        level: FocusLevel = FocusLevel.PARAGRAPH
    ) -> Optional[FocusContext]:
        """Enter focus mode for the specified section and segment."""
        section = self.document.get_section(section_index)
        if not section:
            return None
        
        segment = section.get_segment(segment_index)
        if not segment:
            return None
        
        self.active_focus = FocusContext(
            document=self.document,
            section=section,
            segment=segment,
            level=level
        )
        self.focus_history.append(self.active_focus)
        return self.active_focus
    
    def exit_focus(self) -> bool:
        """Exit focus mode."""
        if self.active_focus:
            self.active_focus = None
            return True
        return False
    
    def move_focus(self, direction: int = 1) -> Optional[FocusContext]:
        """Move the focus to the next or previous segment."""
        if not self.active_focus:
            return None
        
        current_segment = self.active_focus.segment
        current_section = self.active_focus.section
        
        # Find the next segment within the current section
        next_position = current_segment.position + direction
        next_segment = current_section.get_segment(next_position)
        
        if next_segment:
            # Move focus within the same section
            self.active_focus = FocusContext(
                document=self.document,
                section=current_section,
                segment=next_segment,
                level=self.active_focus.level
            )
            self.focus_history.append(self.active_focus)
            return self.active_focus
        
        # Try to move to a different section
        current_section_idx = self.document.current_revision.sections.index(current_section)
        next_section_idx = current_section_idx + direction
        
        if 0 <= next_section_idx < len(self.document.current_revision.sections):
            next_section = self.document.current_revision.sections[next_section_idx]
            
            # Get the first or last segment of the next section depending on direction
            target_position = 0 if direction > 0 else len(next_section.segments) - 1
            if 0 <= target_position < len(next_section.segments):
                next_segment = next_section.segments[target_position]
                
                self.active_focus = FocusContext(
                    document=self.document,
                    section=next_section,
                    segment=next_segment,
                    level=self.active_focus.level
                )
                self.focus_history.append(self.active_focus)
                return self.active_focus
        
        return None
    
    def change_focus_level(self, level: FocusLevel) -> Optional[FocusContext]:
        """Change the level of focus."""
        if not self.active_focus:
            return None
        
        self.active_focus.level = level
        self.focus_history.append(self.active_focus)
        return self.active_focus
    
    def edit_focused_content(self, new_content: str) -> Optional[TextSegment]:
        """Edit the content of the focused segment."""
        if not self.active_focus:
            return None
        
        self.active_focus.segment.content = new_content
        self.document.updated_at = time.time()
        return self.active_focus.segment
    
    def get_focus_time(self) -> float:
        """Get the time spent in the current focus session in seconds."""
        if not self.active_focus:
            return 0.0
        
        return time.time() - self.active_focus.start_time
    
    def get_surrounding_context(self, context_size: int = 2) -> List[TextSegment]:
        """Get the surrounding segments around the focused segment."""
        if not self.active_focus:
            return []
        
        section = self.active_focus.section
        position = self.active_focus.segment.position
        
        start = max(0, position - context_size)
        end = min(len(section.segments), position + context_size + 1)
        
        return section.segments[start:end]
    
    def move_cursor_in_focus(self, direction: str, amount: int = 1) -> bool:
        """Move the cursor within the focused segment."""
        if not self.active_focus or not self.active_focus.focus_position:
            return False
        
        current_pos = self.active_focus.focus_position
        focus_area = self.active_focus.get_focus_area()
        
        if not focus_area:
            return False
        
        # Calculate new position based on direction
        new_pos = None
        if direction == "left":
            new_col = max(focus_area.start.column, current_pos.column - amount)
            new_pos = Position(line=current_pos.line, column=new_col)
        elif direction == "right":
            new_col = min(focus_area.end.column, current_pos.column + amount)
            new_pos = Position(line=current_pos.line, column=new_col)
        elif direction == "up" and current_pos.line > focus_area.start.line:
            new_pos = Position(line=current_pos.line - amount, column=current_pos.column)
        elif direction == "down" and current_pos.line < focus_area.end.line:
            new_pos = Position(line=current_pos.line + amount, column=current_pos.column)
        
        if new_pos:
            return self.active_focus.set_cursor_position(new_pos)
        
        return False
    
    def select_in_focus(self, start_pos: Position, end_pos: Position) -> bool:
        """Create a selection within the focused segment."""
        if not self.active_focus:
            return False
        
        selection = Selection(start=start_pos, end=end_pos)
        return self.active_focus.set_selection(selection)
    
    def get_focus_cursor_position(self) -> Optional[Position]:
        """Get the current cursor position within the focus."""
        if self.active_focus:
            return self.active_focus.focus_position
        return None
    
    def get_focus_selection(self) -> Optional[Selection]:
        """Get the current selection within the focus."""
        if self.active_focus:
            return self.active_focus.focus_selection
        return None