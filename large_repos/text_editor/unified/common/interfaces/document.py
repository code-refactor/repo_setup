from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime

from ..core.models import FileInfo


class DocumentInterface(ABC):
    """Abstract interface for document management functionality."""
    
    @abstractmethod
    def save(self, path: Optional[str] = None) -> bool:
        """Save the document to a file."""
        pass
    
    @abstractmethod
    def save_as(self, path: str) -> bool:
        """Save the document to a new file."""
        pass
    
    @abstractmethod
    def load(self, path: str) -> bool:
        """Load a document from a file."""
        pass
    
    @abstractmethod
    def new_document(self) -> None:
        """Create a new document."""
        pass
    
    @abstractmethod
    def get_file_info(self) -> FileInfo:
        """Get information about the current file."""
        pass
    
    @abstractmethod
    def get_file_name(self) -> str:
        """Get the name of the current file."""
        pass
    
    @abstractmethod
    def get_file_path(self) -> Optional[str]:
        """Get the path of the current file."""
        pass
    
    @abstractmethod
    def has_file(self) -> bool:
        """Check if there is a current file."""
        pass
    
    @abstractmethod
    def is_modified(self) -> bool:
        """Check if the document has been modified."""
        pass
    
    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Get document metadata."""
        pass
    
    @abstractmethod
    def set_metadata(self, metadata: Dict[str, Any]) -> None:
        """Set document metadata."""
        pass
    
    @abstractmethod
    def get_word_count(self) -> int:
        """Get the total word count of the document."""
        pass
    
    @abstractmethod
    def get_char_count(self) -> int:
        """Get the total character count of the document."""
        pass
    
    @abstractmethod
    def get_creation_time(self) -> Optional[datetime]:
        """Get the document creation time."""
        pass
    
    @abstractmethod
    def get_modification_time(self) -> Optional[datetime]:
        """Get the last modification time."""
        pass


class VersionedDocumentInterface(DocumentInterface):
    """Extended document interface with version control functionality."""
    
    @abstractmethod
    def create_version(self, description: str = "") -> str:
        """Create a new version of the document."""
        pass
    
    @abstractmethod
    def list_versions(self) -> List[Dict[str, Any]]:
        """List all available versions."""
        pass
    
    @abstractmethod
    def restore_version(self, version_id: str) -> bool:
        """Restore a specific version of the document."""
        pass
    
    @abstractmethod
    def compare_versions(self, version1: str, version2: str) -> Dict[str, Any]:
        """Compare two versions of the document."""
        pass
    
    @abstractmethod
    def delete_version(self, version_id: str) -> bool:
        """Delete a specific version."""
        pass
    
    @abstractmethod
    def get_current_version_id(self) -> Optional[str]:
        """Get the ID of the current version."""
        pass


class CollaborativeDocumentInterface(DocumentInterface):
    """Extended document interface with collaboration features."""
    
    @abstractmethod
    def add_comment(self, position: int, text: str, author: str) -> str:
        """Add a comment at a specific position."""
        pass
    
    @abstractmethod
    def get_comments(self) -> List[Dict[str, Any]]:
        """Get all comments in the document."""
        pass
    
    @abstractmethod
    def resolve_comment(self, comment_id: str) -> bool:
        """Mark a comment as resolved."""
        pass
    
    @abstractmethod
    def delete_comment(self, comment_id: str) -> bool:
        """Delete a comment."""
        pass
    
    @abstractmethod
    def add_suggestion(self, start_pos: int, end_pos: int, 
                      suggested_text: str, author: str) -> str:
        """Add a text suggestion."""
        pass
    
    @abstractmethod
    def accept_suggestion(self, suggestion_id: str) -> bool:
        """Accept a text suggestion."""
        pass
    
    @abstractmethod
    def reject_suggestion(self, suggestion_id: str) -> bool:
        """Reject a text suggestion."""
        pass
    
    @abstractmethod
    def get_suggestions(self) -> List[Dict[str, Any]]:
        """Get all suggestions in the document."""
        pass
    
    @abstractmethod
    def set_document_permissions(self, permissions: Dict[str, str]) -> None:
        """Set document access permissions."""
        pass
    
    @abstractmethod
    def get_document_permissions(self) -> Dict[str, str]:
        """Get document access permissions."""
        pass


class StructuredDocumentInterface(DocumentInterface):
    """Extended document interface for structured documents."""
    
    @abstractmethod
    def get_outline(self) -> List[Dict[str, Any]]:
        """Get the document outline/structure."""
        pass
    
    @abstractmethod
    def add_section(self, title: str, level: int, position: Optional[int] = None) -> str:
        """Add a new section to the document."""
        pass
    
    @abstractmethod
    def remove_section(self, section_id: str) -> bool:
        """Remove a section from the document."""
        pass
    
    @abstractmethod
    def move_section(self, section_id: str, new_position: int) -> bool:
        """Move a section to a new position."""
        pass
    
    @abstractmethod
    def get_section_content(self, section_id: str) -> str:
        """Get the content of a specific section."""
        pass
    
    @abstractmethod
    def set_section_content(self, section_id: str, content: str) -> bool:
        """Set the content of a specific section."""
        pass
    
    @abstractmethod
    def add_table_of_contents(self, position: Optional[int] = None) -> bool:
        """Add a table of contents to the document."""
        pass
    
    @abstractmethod
    def update_table_of_contents(self) -> bool:
        """Update the existing table of contents."""
        pass
    
    @abstractmethod
    def add_footnote(self, text: str, reference_position: int) -> str:
        """Add a footnote to the document."""
        pass
    
    @abstractmethod
    def add_citation(self, citation_data: Dict[str, Any], position: int) -> str:
        """Add a citation to the document."""
        pass
    
    @abstractmethod
    def get_bibliography(self) -> List[Dict[str, Any]]:
        """Get the bibliography/references."""
        pass
    
    @abstractmethod
    def update_bibliography(self) -> bool:
        """Update the bibliography based on citations."""
        pass


class ExportableDocumentInterface(DocumentInterface):
    """Extended document interface with export functionality."""
    
    @abstractmethod
    def export_to_format(self, format: str, options: Optional[Dict[str, Any]] = None) -> bytes:
        """Export document to a specific format."""
        pass
    
    @abstractmethod
    def get_supported_export_formats(self) -> List[str]:
        """Get list of supported export formats."""
        pass
    
    @abstractmethod
    def export_to_pdf(self, options: Optional[Dict[str, Any]] = None) -> bytes:
        """Export document to PDF format."""
        pass
    
    @abstractmethod
    def export_to_html(self, options: Optional[Dict[str, Any]] = None) -> str:
        """Export document to HTML format."""
        pass
    
    @abstractmethod
    def export_to_markdown(self, options: Optional[Dict[str, Any]] = None) -> str:
        """Export document to Markdown format."""
        pass
    
    @abstractmethod
    def export_to_docx(self, options: Optional[Dict[str, Any]] = None) -> bytes:
        """Export document to DOCX format."""
        pass
    
    @abstractmethod
    def import_from_format(self, data: bytes, format: str, 
                          options: Optional[Dict[str, Any]] = None) -> bool:
        """Import document from a specific format."""
        pass
    
    @abstractmethod
    def get_supported_import_formats(self) -> List[str]:
        """Get list of supported import formats."""
        pass