"""Dependency injection utilities — singleton factories for shared services."""

from functools import lru_cache

from src.services.chat_service import ChatService
from src.services.rag_service import RAGService
from src.vectorstores.vector_db_service import VectorDBService


@lru_cache(maxsize=1)
def get_rag_service() -> RAGService:
    return RAGService()


@lru_cache(maxsize=1)
def get_chat_service() -> ChatService:
    return ChatService(get_rag_service())


@lru_cache(maxsize=1)
def get_vector_db_service() -> VectorDBService:
    return VectorDBService()
