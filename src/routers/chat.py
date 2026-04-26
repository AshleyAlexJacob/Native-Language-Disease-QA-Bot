"""Chat inference endpoint with in-session history."""

from fastapi import APIRouter, Depends

from src.dependencies import get_chat_service
from src.schemas.pydantic.api_schemas import ChatRequest, ChatResponse
from src.services.chat_service import ChatService

router = APIRouter()


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    svc: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    """Answer a health question using WHO-grounded RAG, maintaining session history.

    Supply the same ``session_id`` across multiple requests to build a
    multi-turn conversation. Omit it (or pass ``null``) to start a new session.
    """
    result = svc.chat(
        query=request.query,
        language=request.language,
        k=request.k,
        session_id=request.session_id,
    )
    return ChatResponse(**result)
