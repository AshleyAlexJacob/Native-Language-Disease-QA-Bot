"""Chat service: wraps RAGService with in-memory per-session chat history."""

import uuid

from src.schemas.pydantic.api_schemas import ChatMessage
from src.schemas.pydantic.rag_schemas import QueryRequest
from src.services.rag_service import RAGService

_sessions: dict[str, list[ChatMessage]] = {}


class ChatService:
    """Maintains per-session chat history and delegates Q&A to RAGService.

    Args:
        rag_service: An initialised RAGService instance.
    """

    def __init__(self, rag_service: RAGService) -> None:
        self._rag = rag_service

    def chat(
        self,
        query: str,
        language: str,
        k: int,
        session_id: str | None,
    ) -> dict:
        """Answer a query and append both turns to the session history.

        Args:
            query: The user's health question.
            language: Preferred response language.
            k: Number of chunks to retrieve.
            session_id: Existing session ID, or None to start a new session.

        Returns:
            dict with session_id, answer, sources, disclaimer, and history.
        """
        sid = session_id or str(uuid.uuid4())
        history = _sessions.setdefault(sid, [])

        result = self._rag.answer(QueryRequest(query=query, language=language, k=k))

        history.append(ChatMessage(role="human", content=query))
        history.append(ChatMessage(role="assistant", content=result["answer"]))

        return {
            "session_id": sid,
            "answer": result["answer"],
            "sources": result["sources"],
            "disclaimer": result["disclaimer"],
            "history": [m.model_dump() for m in history],
        }
