"""Ingestion pipeline that orchestrates PDF loading, chunking, embedding, and vector DB upsert."""

import logging
from pathlib import Path

from langchain_core.documents import Document

from src.core.document_parser import DocumentParser
from src.vectorstores.vector_db_service import VectorDBService

logger = logging.getLogger(__name__)


class IngestionPipeline:
    """Orchestrates the full document ingestion job for the RAG pipeline.

    Runs four stages in sequence: parse PDFs → chunk → embed → upsert to
    ChromaDB.  Call :meth:`run` to execute the full job.

    Args:
        config_path: Path to the RAG YAML config file.  Passed through to all
            sub-components; defaults to ``config/rag.yaml`` relative to the
            project root.
        reset: If ``True``, the ChromaDB collection is cleared before
            ingestion so every run starts from a clean state.  Defaults to
            ``False`` (append / upsert behaviour).
    """

    def __init__(
        self,
        config_path: str | Path | None = None,
        reset: bool = False,
    ) -> None:
        self._parser = DocumentParser(config_path)
        self._vector_db = VectorDBService(config_path)
        self._reset = reset

    def _log_document_summary(self, filename: str, docs: list[Document]) -> None:
        """Log filename, page count, and top 5 lines of the first page."""
        page_count = docs[0].metadata.get("page_count", len(docs)) if docs else 0
        top_lines = []
        if docs:
            top_lines = [
                line for line in docs[0].page_content.splitlines() if line.strip()
            ][:5]

        logger.info("  File     : %s", filename)
        logger.info("  Pages    : %d", page_count)
        logger.info("  Preview  :")
        for line in top_lines:
            logger.info("    %s", line)

    def run(self) -> list[str]:
        """Execute the full ingestion pipeline.

        Steps:
            1. Optionally reset the ChromaDB collection (if ``reset=True``).
            2. Parse every PDF listed in the RAG YAML config.
            3. Chunk, embed, and upsert all parsed pages via
               :class:`~src.vectorstores.vector_db_service.VectorDBService`.

        Returns:
            List of ChromaDB document IDs assigned to the stored chunks.
        """
        logger.info("Starting ingestion pipeline from '%s'", self._parser.docs_dir)

        if self._reset:
            logger.warning("Reset requested — clearing existing ChromaDB collection.")
            self._vector_db.reset()

        all_documents: list[Document] = []
        for pdf_path in self._parser.pdf_paths:
            try:
                docs = self._parser.parse_document(pdf_path)
                self._log_document_summary(pdf_path.name, docs)
                all_documents.extend(docs)
            except Exception as exc:
                logger.error("Skipping '%s' due to error: %s", pdf_path.name, exc)

        logger.info(
            "Parsing complete: %d page(s) loaded from %d PDF file(s).",
            len(all_documents),
            len(self._parser.pdf_paths),
        )

        if not all_documents:
            logger.warning("No documents parsed — skipping embedding and vector DB upsert.")
            return []

        logger.info("Starting chunking, embedding, and vector DB upsert …")
        ids = self._vector_db.ingest_documents(all_documents)
        logger.info(
            "Ingestion complete: %d chunk(s) stored in ChromaDB.", len(ids)
        )
        return ids