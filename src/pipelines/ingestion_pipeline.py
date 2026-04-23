"""Ingestion pipeline that orchestrates PDF document loading for the RAG system."""

import logging
from pathlib import Path

from langchain_core.documents import Document

from src.core.document_parser import DocumentParser

logger = logging.getLogger(__name__)


class IngestionPipeline:
    """Orchestrates the document ingestion job for the RAG pipeline.

    Coordinates the parsing stage (and future stages such as chunking,
    embedding, and vector store upsert).  Call :meth:`run` to execute
    the full ingestion job.

    Args:
        config_path: Path to the RAG YAML config file.  Passed through to
            :class:`~src.core.document_parser.DocumentParser`; defaults to
            ``config/rag.yaml`` relative to the project root.
    """

    def __init__(self, config_path: str | Path | None = None) -> None:
        self._parser = DocumentParser(config_path)

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

    def run(self) -> list[Document]:
        """Execute the ingestion pipeline and return parsed Documents.

        Parses all PDF files configured in the RAG YAML, logs a per-file
        summary (name, page count, top 5 lines), and returns a flat list of
        LangChain Documents ready for downstream processing.

        Returns:
            A flat list of Documents across all ingested PDF files.
        """
        logger.info("Starting ingestion pipeline from '%s'", self._parser.docs_dir)

        all_documents: list[Document] = []
        for pdf_path in self._parser.pdf_paths:
            try:
                docs = self._parser.parse_document(pdf_path)
                self._log_document_summary(pdf_path.name, docs)
                all_documents.extend(docs)
            except Exception as exc:
                logger.error("Skipping '%s' due to error: %s", pdf_path.name, exc)

        logger.info(
            "Ingestion complete: %d page(s) loaded from %d PDF file(s).",
            len(all_documents),
            len(self._parser.pdf_paths),
        )

        return all_documents