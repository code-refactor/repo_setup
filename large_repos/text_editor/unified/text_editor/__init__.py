# Student text editor package - uses common library for core functionality

# Import core editor functionality from common library
from common.core import Editor as CommonEditor, Position, Direction

# Import student-specific modules
from .core.editor import Editor
from .customization.manager import CustomizationManager
from .features.manager import FeatureManager
from .learning.manager import LearningManager
from .study.manager import StudyManager
from .interview.manager import InterviewManager

__all__ = [
    # Core functionality (now using common library)
    'CommonEditor', 'Position', 'Direction',
    
    # Student-specific functionality
    'Editor',
    'CustomizationManager',
    'FeatureManager', 
    'LearningManager',
    'StudyManager',
    'InterviewManager'
]