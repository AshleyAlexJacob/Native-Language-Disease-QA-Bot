"""Document chunking for the RAG ingestion pipeline."""

import logging
from pathlib import Path

import yaml
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

_PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
_DEFAULT_CONFIG_PATH: Path = _PROJECT_ROOT / "config" / "rag.yaml"


class DocumentChunker:
    """Splits LangChain Documents into fixed-size overlapping chunks.

    Reads chunk_size and chunk_overlap from the ``chunking`` section of
    the RAG YAML config. All original metadata is preserved on every
    child chunk.

    Args:
        config_path: Path to the RAG YAML config file. Defaults to
            ``config/rag.yaml`` relative to the project root.

    Raises:
        FileNotFoundError: If the config file does not exist.
        KeyError: If the ``chunking`` section is absent from the config.
    """

    def __init__(self, config_path: str | Path | None = None) -> None:
        resolved = Path(config_path) if config_path else _DEFAULT_CONFIG_PATH
        cfg = self._load_config(resolved)
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=cfg["chunk_size"],
            chunk_overlap=cfg["chunk_overlap"],
        )

    def _load_config(self, config_path: Path) -> dict:
        if not config_path.exists():
            raise FileNotFoundError(f"RAG config not found: {config_path}")
        with config_path.open("r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
        if "chunking" not in raw:
            raise KeyError("'chunking' section missing from config")
        cfg = raw["chunking"]
        logger.debug("Loaded chunking config: %s", cfg)
        return cfg

    def split(self, documents: list[Document]) -> list[Document]:
        """Split documents into chunks, preserving all metadata.

        Args:
            documents: Raw page-level Documents from the ingestion pipeline.

        Returns:
            A flat list of chunk-level Documents.
        """
        chunks = self._splitter.split_documents(documents)
        logger.info("Split %d document(s) into %d chunk(s).", len(documents), len(chunks))
        return chunks
