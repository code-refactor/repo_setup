"""Document models for the legal discovery interpreter.

This module extends the common Document model with legal-specific functionality
while maintaining backward compatibility with existing interfaces.
"""

from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field

from common.core import Document as CommonDocument


class DocumentMetadata(BaseModel):
    """Metadata for a legal document.
    
    This class maintains the existing legal discovery metadata structure
    while being compatible with the common Document model.
    """
    
    document_id: str = Field(..., description="Unique identifier for the document")
    title: str = Field(..., description="Document title")
    document_type: str = Field(..., description="Type of document (e.g., contract, email, memo)")
    date_created: datetime = Field(..., description="Date and time the document was created")
    date_modified: Optional[datetime] = Field(None, description="Date and time the document was last modified")
    author: Optional[str] = Field(None, description="Author of the document")
    custodian: Optional[str] = Field(None, description="Custodian of the document")
    source: Optional[str] = Field(None, description="Source of the document")
    file_path: Optional[str] = Field(None, description="File path where the document is stored")
    file_type: Optional[str] = Field(None, description="File type of the document")
    file_size: Optional[int] = Field(None, description="Size of the document in bytes")
    
    # Additional metadata fields specific to legal discovery
    confidentiality: Optional[str] = Field(None, description="Confidentiality level of the document")
    privilege_status: Optional[str] = Field(None, description="Privilege status of the document")
    litigation_hold: Optional[bool] = Field(None, description="Whether the document is on litigation hold")
    production_number: Optional[str] = Field(None, description="Production number for the document")
    redaction_status: Optional[str] = Field(None, description="Redaction status of the document")
    
    class Config:
        """Pydantic model configuration."""
        
        extra = "allow"  # Allow extra fields for flexibility
    
    def to_common_metadata(self) -> Dict[str, Any]:
        """Convert to common document metadata format.
        
        Returns:
            Dictionary compatible with common Document metadata
        """
        return {
            "title": self.title,
            "document_type": self.document_type,
            "author": self.author,
            "custodian": self.custodian,
            "source": self.source,
            "file_path": self.file_path,
            "file_type": self.file_type,
            "file_size": self.file_size,
            # Legal-specific fields
            "confidentiality": self.confidentiality,
            "privilege_status": self.privilege_status,
            "litigation_hold": self.litigation_hold,
            "production_number": self.production_number,
            "redaction_status": self.redaction_status,
        }


class Document(BaseModel):
    """Legal document model that maintains compatibility with existing code.
    
    This class bridges the legal-specific document structure with the common
    Document model while preserving all existing functionality.
    """
    
    metadata: DocumentMetadata = Field(..., description="Document metadata")
    content: str = Field(..., description="Full text content of the document")
    
    # Search and analysis related fields
    relevance_score: Optional[float] = Field(None, description="Relevance score for the document")
    privilege_score: Optional[float] = Field(None, description="Privilege score for the document")
    extracted_entities: Optional[Dict[str, List[str]]] = Field(None, 
                                                            description="Extracted entities from the document")
    tags: Optional[List[str]] = Field(None, description="Tags assigned to the document")
    
    def get_content_preview(self, max_length: int = 200) -> str:
        """Get a preview of the document content.
        
        Args:
            max_length: Maximum length of the preview
            
        Returns:
            A preview of the document content
        """
        if len(self.content) <= max_length:
            return self.content
        
        return f"{self.content[:max_length]}..."
    
    def to_common_document(self) -> CommonDocument:
        """Convert to common Document format.
        
        Returns:
            CommonDocument instance with equivalent data
        """
        # Prepare legal metadata
        legal_metadata = {
            "privilege_score": self.privilege_score,
            "extracted_entities": self.extracted_entities,
            "relevance_score": self.relevance_score,
        }
        
        return CommonDocument(
            document_id=self.metadata.document_id,
            content=self.content,
            metadata=self.metadata.to_common_metadata(),
            created_at=self.metadata.date_created,
            modified_at=self.metadata.date_modified,
            source=self.metadata.source,
            source_type=self.metadata.document_type,
            content_type=self.metadata.file_type,
            size_bytes=self.metadata.file_size,
            legal_metadata=legal_metadata,
            tags=set(self.tags or []),
            classification=self.metadata.confidentiality,
            sensitivity_level=self.metadata.privilege_status,
        )
    
    @classmethod
    def from_common_document(cls, common_doc: CommonDocument) -> "Document":
        """Create legal Document from common Document.
        
        Args:
            common_doc: CommonDocument instance
            
        Returns:
            Legal Document instance
        """
        # Extract legal-specific metadata
        legal_meta = common_doc.legal_metadata or {}
        
        # Create DocumentMetadata
        metadata = DocumentMetadata(
            document_id=common_doc.document_id,
            title=common_doc.metadata.get("title", ""),
            document_type=common_doc.source_type or "unknown",
            date_created=common_doc.created_at or datetime.now(),
            date_modified=common_doc.modified_at,
            author=common_doc.metadata.get("author"),
            custodian=common_doc.metadata.get("custodian"),
            source=common_doc.source,
            file_path=common_doc.metadata.get("file_path"),
            file_type=common_doc.content_type,
            file_size=common_doc.size_bytes,
            confidentiality=common_doc.classification,
            privilege_status=common_doc.sensitivity_level,
            litigation_hold=common_doc.metadata.get("litigation_hold"),
            production_number=common_doc.metadata.get("production_number"),
            redaction_status=common_doc.metadata.get("redaction_status"),
        )
        
        return cls(
            metadata=metadata,
            content=common_doc.content,
            relevance_score=legal_meta.get("relevance_score"),
            privilege_score=legal_meta.get("privilege_score"),
            extracted_entities=legal_meta.get("extracted_entities"),
            tags=list(common_doc.tags) if common_doc.tags else None,
        )


class EmailDocument(Document):
    """Model for an email document."""
    
    sender: str = Field(..., description="Email sender")
    recipients: List[str] = Field(..., description="Email recipients")
    cc: Optional[List[str]] = Field(None, description="CC recipients")
    bcc: Optional[List[str]] = Field(None, description="BCC recipients")
    subject: str = Field(..., description="Email subject")
    sent_date: datetime = Field(..., description="Date and time the email was sent")
    thread_id: Optional[str] = Field(None, description="ID of the email thread")
    in_reply_to: Optional[str] = Field(None, description="ID of the email this is in reply to")
    attachments: Optional[List[str]] = Field(None, description="List of attachment document IDs")


class LegalAgreement(Document):
    """Model for a legal agreement document."""
    
    parties: List[str] = Field(..., description="Parties to the agreement")
    effective_date: datetime = Field(..., description="Effective date of the agreement")
    termination_date: Optional[datetime] = Field(None, description="Termination date of the agreement")
    governing_law: Optional[str] = Field(None, description="Governing law of the agreement")
    agreement_type: str = Field(..., description="Type of agreement")


class DocumentCollection(BaseModel):
    """A collection of documents for a legal discovery case."""
    
    collection_id: str = Field(..., description="Unique identifier for the collection")
    name: str = Field(..., description="Name of the collection")
    description: Optional[str] = Field(None, description="Description of the collection")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    documents: Dict[str, Union[Document, EmailDocument, LegalAgreement]] = Field(
        default_factory=dict, description="Documents in the collection, indexed by document ID"
    )
    
    def add_document(self, document: Union[Document, EmailDocument, LegalAgreement]) -> None:
        """Add a document to the collection.
        
        Args:
            document: Document to add
        """
        self.documents[document.metadata.document_id] = document
        self.updated_at = datetime.now()
    
    def remove_document(self, document_id: str) -> None:
        """Remove a document from the collection.
        
        Args:
            document_id: ID of the document to remove
        """
        if document_id in self.documents:
            del self.documents[document_id]
            self.updated_at = datetime.now()
    
    def get_document(self, document_id: str) -> Optional[Union[Document, EmailDocument, LegalAgreement]]:
        """Get a document from the collection.
        
        Args:
            document_id: ID of the document to get
            
        Returns:
            The document, or None if not found
        """
        return self.documents.get(document_id)
    
    def count(self) -> int:
        """Count the number of documents in the collection.
        
        Returns:
            Number of documents in the collection
        """
        return len(self.documents)
    
    def to_common_collection(self) -> Dict[str, CommonDocument]:
        """Convert collection to common document format.
        
        Returns:
            Dictionary of CommonDocument instances
        """
        common_docs = {}
        for doc_id, doc in self.documents.items():
            if hasattr(doc, 'to_common_document'):
                common_docs[doc_id] = doc.to_common_document()
            else:
                # For documents that don't have the conversion method,
                # create a basic CommonDocument
                common_docs[doc_id] = CommonDocument(
                    document_id=doc_id,
                    content=getattr(doc, 'content', ''),
                    metadata=getattr(doc, 'metadata', {}).__dict__ if hasattr(getattr(doc, 'metadata', {}), '__dict__') else getattr(doc, 'metadata', {})
                )
        return common_docs