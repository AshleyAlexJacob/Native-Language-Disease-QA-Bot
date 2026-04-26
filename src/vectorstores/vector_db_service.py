"""High-level service composing chunking, embedding, and vector storage."""

import logging
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever

from src.embeddings.chunker import DocumentChunker
from src.embeddings.embedder import DocumentEmbedder
from src.vectorstores.chroma_store import ChromaVectorStore

logger = logging.getLogger(__name__)


class VectorDBService:
    """Orchestrates document ingestion into and retrieval from ChromaDB.

    Composes DocumentChunker, DocumentEmbedder, and ChromaVectorStore.
    This is the single public entry point for all vector DB operations
    in the RAG pipeline.

    Args:
        config_path: Path to the RAG YAML config file. Passed through to
            all composed components; defaults to ``config/rag.yaml``.
    """

    def __init__(self, config_path: str | Path | None = None) -> None:
        self._chunker = DocumentChunker(config_path)
        embedder = DocumentEmbedder(config_path)
        self._store = ChromaVectorStore(embedder.embeddings, config_path)

    def ingest_documents(self, docs: list[Document]) -> list[str]:
        """Chunk, embed, and persist a list of Documents.

        Args:
            docs: Page-level Documents from the ingestion pipeline.

        Returns:
            List of ChromaDB document IDs assigned to the stored chunks.
        """
        chunks = self._chunker.split(docs)
        ids = self._store.add_documents(chunks)
        logger.info(
            "Ingested %d page(s) → %d chunk(s) → %d ID(s) stored.",
            len(docs),
            len(chunks),
            len(ids),
        )
        return ids

    def search(self, query: str, k: int = 3) -> list[tuple[Document, float]]:
        """Search the vector store and return top-k chunks with scores.

        Args:
            query: Natural-language query string.
            k: Maximum number of results.

        Returns:
            List of (Document, relevance_score) tuples.
        """
        return self._store.similarity_search(query, k=k)

    def as_retriever(self, **kwargs) -> VectorStoreRetriever:
        """Expose the underlying store as a LangChain retriever.

        Args:
            **kwargs: Forwarded to ChromaVectorStore.as_retriever().

        Returns:
            A VectorStoreRetriever for use in LCEL chains.
        """
        return self._store.as_retriever(**kwargs)

    def list_sources(self) -> list[str]:
        """Return sorted unique source_file values from all stored chunks."""
        return self._store.list_sources()

    def delete_by_source(self, source_file: str) -> int:
        """Delete all chunks matching source_file. Returns count deleted."""
        return self._store.delete_by_source(source_file)

    def reset(self) -> None:
        """Delete all documents from the ChromaDB collection.

        Useful for re-ingestion and testing. The collection is recreated
        lazily on the next ingest_documents call.
        """
        self._store.clear()
        logger.warning("VectorDBService: vector store has been reset.")
