from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, Any
from uuid import UUID

from .models import (
    CitationBlock,
    CodeBlock,
    Document,
    EquationBlock,
    ImageBlock,
    JournalFormat,
    Section,
    TableBlock,
    TextBlock,
)


class ExportStorageInterface(ABC):
    """Abstract interface for export storage implementations."""

    @abstractmethod
    def create_document(self, document: Document) -> Document:
        """
        Create a new document.

        Args:
            document: The document to create

        Returns:
            Document: The created document
        """
        pass

    @abstractmethod
    def get_document(self, document_id: UUID) -> Optional[Document]:
        """
        Retrieve a document by ID.

        Args:
            document_id: The ID of the document to retrieve

        Returns:
            Optional[Document]: The document if found, None otherwise
        """
        pass

    @abstractmethod
    def update_document(self, document: Document) -> Document:
        """
        Update an existing document.

        Args:
            document: The document with updated fields

        Returns:
            Document: The updated document
        """
        pass

    @abstractmethod
    def delete_document(self, document_id: UUID) -> bool:
        """
        Delete a document by ID.

        Args:
            document_id: The ID of the document to delete

        Returns:
            bool: True if deletion successful, False otherwise
        """
        pass

    @abstractmethod
    def list_documents(self) -> List[Document]:
        """
        List all documents.

        Returns:
            List[Document]: List of all documents
        """
        pass


class InMemoryExportStorage(ExportStorageInterface):
    """In-memory implementation of export storage."""

    def __init__(self):
        self._documents: Dict[UUID, Document] = {}

    def create_document(self, document: Document) -> Document:
        self._documents[document.id] = document
        return document

    def get_document(self, document_id: UUID) -> Optional[Document]:
        return self._documents.get(document_id)

    def update_document(self, document: Document) -> Document:
        if document.id not in self._documents:
            return None
        self._documents[document.id] = document
        return document

    def delete_document(self, document_id: UUID) -> bool:
        if document_id not in self._documents:
            return False
        del self._documents[document_id]
        return True

    def list_documents(self) -> List[Document]:
        return list(self._documents.values())