#!/usr/bin/env python3
"""
Test script to verify that the text_editor refactoring is working correctly.
This script tests that the student persona can still access all its functionality
while using the common library for core components.
"""

def test_basic_editor():
    """Test basic editor functionality."""
    from text_editor import Editor
    
    editor = Editor('Hello World')
    assert editor.get_content() == 'Hello World'
    assert editor.get_cursor_position() == (0, 0)
    
    editor.insert_text(' - Test')
    assert ' - Test' in editor.get_content()
    
    print("✓ Basic editor functionality works")

def test_common_library_integration():
    """Test that common library components are properly accessible."""
    from text_editor import Editor, CommonEditor, Position, Direction
    
    # Test that we can create common editor directly
    common_editor = CommonEditor()
    assert hasattr(common_editor, 'get_content')
    
    # Test that we can use common models
    pos = Position(line=0, column=5)
    assert pos.line == 0 and pos.column == 5
    
    # Test that student editor wraps common editor properly
    editor = Editor('Test')
    assert hasattr(editor, 'common_editor')
    assert hasattr(editor, 'buffer')
    assert hasattr(editor, 'cursor')
    
    print("✓ Common library integration works")

def test_student_specific_features():
    """Test that all student-specific features are accessible."""
    from text_editor import (
        CustomizationManager, 
        FeatureManager, 
        LearningManager, 
        StudyManager,
        InterviewManager
    )
    
    # Test customization manager
    customization = CustomizationManager()
    components = customization.get_all_components()
    assert len(components) > 0
    
    # Test feature manager
    features = FeatureManager()
    available_features = features.get_available_features()
    assert len(available_features) > 0
    
    # Test learning manager
    learning = LearningManager()
    concepts = learning.get_all_concepts()
    assert len(concepts) > 0
    
    # Test study manager
    study = StudyManager()
    assert hasattr(study, 'topics')
    assert hasattr(study, 'progress_tracker')  # Should use common analytics
    
    # Test interview manager
    interview = InterviewManager()
    assert hasattr(interview, 'stats')
    
    print("✓ All student-specific features work")

def test_analytics_integration():
    """Test that common analytics library is properly integrated."""
    from text_editor import StudyManager
    from common.analytics import ProgressTracker, MetricsCollector
    
    study = StudyManager()
    
    # Verify that study manager uses common analytics
    assert isinstance(study.progress_tracker, ProgressTracker)
    assert isinstance(study.metrics_collector, MetricsCollector)
    
    print("✓ Analytics integration works")

def test_educational_features():
    """Test educational features specific to student persona."""
    from text_editor import LearningManager
    
    learning = LearningManager()
    
    # Test concept browsing
    concepts = learning.get_all_concepts()
    basic_concepts = learning.get_concepts_by_difficulty(
        learning.get_all_concepts()[0].difficulty
    )
    assert len(basic_concepts) > 0
    
    # Test projects
    projects = learning.get_all_extension_projects()
    assert len(projects) > 0
    
    print("✓ Educational features work")

if __name__ == '__main__':
    print("Testing text_editor refactoring...")
    
    test_basic_editor()
    test_common_library_integration()
    test_student_specific_features()
    test_analytics_integration()
    test_educational_features()
    
    print("\n🎉 All tests passed! Refactoring successful.")
    print("\nSummary:")
    print("- ✅ Core editor functionality now uses common library")
    print("- ✅ Student-specific features preserved")
    print("- ✅ Analytics integration working")
    print("- ✅ Educational features intact")
    print("- ✅ Backward compatibility maintained")