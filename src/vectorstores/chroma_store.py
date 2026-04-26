"""ChromaDB-backed vector store for the RAG pipeline."""

import logging
from pathlib import Path

import yaml
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStoreRetriever

logger = logging.getLogger(__name__)

_PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
_DEFAULT_CONFIG_PATH: Path = _PROJECT_ROOT / "config" / "rag.yaml"


class ChromaVectorStore:
    """Thin wrapper around langchain_chroma.Chroma for the RAG pipeline.

    Manages a persistent ChromaDB collection. The persist_directory is
    resolved relative to the project root when a relative path is given,
    matching the convention used by DocumentParser for docs_dir.

    Args:
        embeddings: An instantiated LangChain Embeddings object.
        config_path: Path to the RAG YAML config file. Defaults to
            ``config/rag.yaml`` relative to the project root.

    Raises:
        FileNotFoundError: If the config file does not exist.
        KeyError: If the ``vectorstore`` section is absent from the config.
    """

    def __init__(
        self,
        embeddings: Embeddings,
        config_path: str | Path | None = None,
    ) -> None:
        resolved = Path(config_path) if config_path else _DEFAULT_CONFIG_PATH
        cfg = self._load_config(resolved)
        persist_dir = self._resolve_persist_dir(cfg["persist_directory"])
        self._store = Chroma(
            collection_name=cfg["collection_name"],
            embedding_function=embeddings,
            persist_directory=str(persist_dir),
        )
        logger.debug(
            "ChromaVectorStore initialised: collection=%s persist_dir=%s",
            cfg["collection_name"],
            persist_dir,
        )

    def _load_config(self, config_path: Path) -> dict:
        if not config_path.exists():
            raise FileNotFoundError(f"RAG config not found: {config_path}")
        with config_path.open("r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
        if "vectorstore" not in raw:
            raise KeyError("'vectorstore' section missing from config")
        cfg = raw["vectorstore"]
        logger.debug("Loaded vectorstore config: %s", cfg)
        return cfg

    def _resolve_persist_dir(self, raw_path: str) -> Path:
        path = Path(raw_path)
        resolved = path if path.is_absolute() else _PROJECT_ROOT / path
        resolved.mkdir(parents=True, exist_ok=True)
        return resolved

    def add_documents(self, documents: list[Document]) -> list[str]:
        """Embed and persist documents to the ChromaDB collection.

        Args:
            documents: Chunk-level Documents to store.

        Returns:
            List of assigned document IDs.
        """
        ids = self._store.add_documents(documents)
        logger.info("Added %d document chunk(s) to ChromaDB.", len(documents))
        return ids

    def similarity_search(
        self,
        query: str,
        k: int = 3,
    ) -> list[tuple[Document, float]]:
        """Return the top-k most similar documents with relevance scores.

        Args:
            query: The natural-language search query.
            k: Number of results to return.

        Returns:
            List of (Document, score) tuples, highest similarity first.
        """
        results = self._store.similarity_search_with_relevance_scores(query, k=k)
        logger.debug("similarity_search returned %d result(s) for query: %r", len(results), query)
        return results

    def as_retriever(self, **kwargs) -> VectorStoreRetriever:
        """Return a LangChain VectorStoreRetriever for use in LCEL chains.

        Args:
            **kwargs: Forwarded to Chroma.as_retriever().

        Returns:
            A configured VectorStoreRetriever.
        """
        return self._store.as_retriever(**kwargs)

    def list_sources(self) -> list[str]:
        """Return sorted unique source_file values from all stored chunks."""
        result = self._store.get(include=["metadatas"])
        seen: set[str] = set()
        for meta in (result.get("metadatas") or []):
            if meta and "source_file" in meta:
                seen.add(meta["source_file"])
        return sorted(seen)

    def delete_by_source(self, source_file: str) -> int:
        """Delete all chunks whose source_file metadata matches.

        Args:
            source_file: The filename to match against stored chunk metadata.

        Returns:
            Number of chunks deleted.
        """
        result = self._store.get(
            where={"source_file": source_file}, include=["metadatas"]
        )
        ids: list[str] = result.get("ids") or []
        if ids:
            self._store.delete(ids=ids)
            logger.info("Deleted %d chunk(s) for source_file=%r", len(ids), source_file)
        return len(ids)

    def clear(self) -> None:
        """Delete and reinitialize the collection.

        Uses reset_collection() so the internal Chroma state remains valid
        and add_documents can be called immediately after.
        """
        self._store.reset_collection()
        logger.warning("ChromaDB collection cleared.")
