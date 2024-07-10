import uuid

from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Dict
from pydantic.v1 import BaseModel, Field

if TYPE_CHECKING:
    from langchain_core.documents import Document as LangChainDocument


class BaseDocument(BaseModel):
    """Base Document Object.

    Generic abstract interface for retrievable documents.

    """
    doc_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), 
        description="Unique ID of the document.")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="A flat dictionary of metadata fields.")
    
    @abstractmethod
    def get_content(self) -> str:
        """Get document content."""

    @abstractmethod
    def get_metadata(self) -> str:
        """Get metadata."""

class Document(BaseDocument):
    text: str = Field(default="")

    @classmethod
    def class_name(cls) -> str:
        return "Document"

    def get_content(self) -> str:
        """Get the text content of the document."""
        return self.text
    
    def get_metadata(self) -> dict:
        """Get the metadata of the document."""
        return self.metadata
    
    @classmethod
    def from_langchain_format(cls, doc: "LangChainDocument") -> "Document":
        """
        Convert a document from LangChain format.

        Args:
            doc (LangChainDocument): Document in LangChain format.
        """
        return cls(text=doc.page_content, metadata=doc.metadata)
