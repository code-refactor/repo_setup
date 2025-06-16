from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Union, Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class JournalFormat(str, Enum):
    """Supported academic journal formats."""

    NATURE = "nature"
    SCIENCE = "science"
    PLOS = "plos"
    FRONTIERS = "frontiers"
    CELL = "cell"
    IEEE = "ieee"
    ACM = "acm"
    JMLR = "jmlr"  # Journal of Machine Learning Research
    PNAS = "pnas"  # Proceedings of the National Academy of Sciences
    ROYAL_SOCIETY = "royal_society"
    DEFAULT = "default"


class TextBlock(BaseModel):
    """A block of text content."""

    id: UUID = Field(default_factory=uuid4)
    content: str
    type: str = "text"


class ImageBlock(BaseModel):
    """A block containing an image."""

    id: UUID = Field(default_factory=uuid4)
    path: str  # Path to the image file
    caption: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    type: str = "image"


class TableBlock(BaseModel):
    """A block containing a table."""

    id: UUID = Field(default_factory=uuid4)
    headers: List[str]
    data: List[List[str]]
    caption: Optional[str] = None
    type: str = "table"


class CodeBlock(BaseModel):
    """A block containing code."""

    id: UUID = Field(default_factory=uuid4)
    code: str
    language: str = "python"
    type: str = "code"


class EquationBlock(BaseModel):
    """A block containing a mathematical equation."""

    id: UUID = Field(default_factory=uuid4)
    equation: str  # LaTeX format equation
    type: str = "equation"


class CitationBlock(BaseModel):
    """A block for a citation reference."""

    id: UUID = Field(default_factory=uuid4)
    reference_ids: List[str]  # IDs of references to cite
    context: Optional[str] = None
    type: str = "citation"


class Section(BaseModel):
    """A section in a document."""

    id: UUID = Field(default_factory=uuid4)
    title: str
    content_blocks: List[Any] = Field(default_factory=list)


class Document(BaseModel):
    """A complete academic document."""

    id: UUID = Field(default_factory=uuid4)
    title: str
    authors: List[str] = Field(default_factory=list)
    affiliations: List[str] = Field(default_factory=list)
    corresponding_email: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    format: JournalFormat = JournalFormat.DEFAULT
    sections: List[Section] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def add_run(self, parameters: List[Any]) -> Any:
        """Add a new run to this experiment."""
        # This is a stub for the test, it will be implemented in the formatter
        pass