"""RAG retriever: wraps VectorDBService to return top-k Documents for a query."""

import logging
from pathlib import Path

from langchain_core.documents import Document

from src.vectorstores.vector_db_service import VectorDBService

logger = logging.getLogger(__name__)


class RAGRetriever:
    """Retrieves semantically relevant document chunks for a user query.

    Delegates to VectorDBService.search() so that embedding generation,
    ChromaDB connection, and similarity scoring are not duplicated here.

    Args:
        config_path: Path to rag.yaml. Defaults to config/rag.yaml.
    """

    def __init__(self, config_path: str | Path | None = None) -> None:
        self._service = VectorDBService(config_path)

    def retrieve(self, query: str, k: int = 5) -> list[Document]:
        """Return the top-k most relevant Document chunks for a query.

        Args:
            query: The user's natural-language question.
            k: Number of chunks to return.

        Returns:
            List of Document objects ranked by relevance (scores stripped).
        """
        results = self._service.search(query, k=k)
        print(results)
        docs = [doc for doc, _score in results]
        logger.debug("RAGRetriever: retrieved %d chunk(s) for query: %r", len(docs), query)
        return docs
