"""Pydantic models for the FastAPI request/response layer."""

from typing import Optional

from pydantic import BaseModel, Field


class DocumentInfo(BaseModel):
    filename: str
    on_disk: bool
    in_chroma: bool


class IngestionResult(BaseModel):
    chunks_stored: int
    files_processed: int


class DeleteResult(BaseModel):
    filename: str
    chunks_deleted: int
    file_removed: bool


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, description="The user's health question.")
    language: str = Field(default="English", description="Preferred response language.")
    k: int = Field(default=3, ge=1, le=10, description="Number of chunks to retrieve.")
    session_id: Optional[str] = Field(
        default=None,
        description="Session ID for chat history. Auto-generated if omitted.",
    )


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: list[dict]
    disclaimer: str
    history: list[ChatMessage]
