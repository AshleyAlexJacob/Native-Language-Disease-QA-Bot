"""Pydantic models for RAG pipeline request and response validation."""

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Validated input for a health QA query.

    Attributes:
        query: The user's natural-language health question.
        language: The user's preferred response language (e.g. "Urdu", "English").
        k: Number of document chunks to retrieve (1–10).
    """

    query: str = Field(..., min_length=1, description="The user's health question.")
    language: str = Field(default="English", description="Language for the response.")
    k: int = Field(default=3, ge=1, le=10, description="Number of chunks to retrieve.")


class SourceDocument(BaseModel):
    """Citation metadata for a single retrieved document chunk.

    Attributes:
        source_file: Filename of the WHO document (e.g. 'malaria.pdf').
        disease_topic: Disease category inferred from the document name.
        page: Page number within the source document.
    """

    source_file: str
    disease_topic: str
    page: int | str


class RAGResponse(BaseModel):
    """Structured LLM output for a grounded health QA response.

    Used with LangChain's .with_structured_output() to enforce schema
    on the LLM reply.

    Attributes:
        answer: The grounded answer text in the user's language.
        citations: List of inline source references extracted from the answer.
        disclaimer: Medical safety disclaimer in the user's language.
    """

    answer: str = Field(description="Grounded answer text in the user's language.")
    citations: list[str] = Field(
        description="Source references, e.g. ['[Source: malaria.pdf, Page 3]']."
    )
    disclaimer: str = Field(description="Medical safety disclaimer.")
