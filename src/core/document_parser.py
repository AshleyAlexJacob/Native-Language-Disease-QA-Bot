"""Document parser for loading WHO medical PDF files into LangChain Documents."""

import logging
from pathlib import Path

import yaml
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

logger = logging.getLogger(__name__)

_PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
_DEFAULT_CONFIG_PATH: Path = _PROJECT_ROOT / "config" / "rag.yaml"


class DocumentParserError(Exception):
    """Raised when a PDF file cannot be parsed."""


class DocumentParser:
    """Discovers and parses PDF documents into LangChain Documents.

    Reads configuration from a YAML file to locate the documents directory.
    Each PDF is loaded page-by-page; metadata fields ``disease_topic``,
    ``source_file``, and ``page_count`` are injected per page for downstream
    retrieval filtering.

    Args:
        config_path: Path to the RAG YAML config file.  Defaults to
            ``config/rag.yaml`` relative to the project root.

    Raises:
        FileNotFoundError: If the config file or docs directory does not exist.
        KeyError: If the ``document_parser`` section is absent from the config.
    """

    def __init__(self, config_path: str | Path | None = None) -> None:
        resolved = Path(config_path) if config_path else _DEFAULT_CONFIG_PATH
        self._config = self._load_config(resolved)
        self._docs_dir = self._resolve_docs_dir()

    def _load_config(self, config_path: Path) -> dict:
        if not config_path.exists():
            raise FileNotFoundError(f"RAG config not found: {config_path}")
        with config_path.open("r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
        if "document_parser" not in raw:
            raise KeyError("'document_parser' section missing from config")
        cfg = raw["document_parser"]
        logger.debug("Loaded document_parser config: %s", cfg)
        return cfg

    def _resolve_docs_dir(self) -> Path:
        raw_path = Path(self._config["docs_dir"])
        docs_dir = raw_path if raw_path.is_absolute() else _PROJECT_ROOT / raw_path
        if not docs_dir.exists():
            raise FileNotFoundError(f"Documents directory not found: {docs_dir}")
        return docs_dir

    @property
    def docs_dir(self) -> Path:
        """Resolved absolute path to the documents directory."""
        return self._docs_dir

    @property
    def pdf_paths(self) -> list[Path]:
        """All PDF files under docs_dir, sorted for deterministic ordering."""
        recursive: bool = self._config.get("recursive", False)
        pattern = "**/*.pdf" if recursive else "*.pdf"
        return sorted(self._docs_dir.glob(pattern))

    def parse_document(self, path: str | Path) -> list[Document]:
        """Parse a single PDF file into a list of LangChain Documents.

        One Document is produced per page.  Extra metadata keys
        ``disease_topic``, ``source_file``, and ``page_count`` are added to
        every page document.

        Args:
            path: Path to a PDF file.

        Returns:
            A list of Documents, one per page.

        Raises:
            FileNotFoundError: If the path does not point to an existing file.
            DocumentParserError: If the PDF cannot be parsed.
        """
        pdf_path = Path(path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        try:
            docs = PyPDFLoader(str(pdf_path)).load()
        except Exception as exc:
            raise DocumentParserError(
                f"Failed to parse '{pdf_path.name}': {exc}"
            ) from exc

        disease_topic = pdf_path.stem
        source_file = pdf_path.name
        page_count = len(docs)
        for doc in docs:
            doc.metadata["disease_topic"] = disease_topic
            doc.metadata["source_file"] = source_file
            doc.metadata["page_count"] = page_count

        logger.debug("Parsed '%s': %d page(s)", source_file, page_count)
        return docs

    def parse_all_documents(self) -> list[Document]:
        """Parse every PDF in docs_dir and return a flat list of Documents.

        Files that fail to parse are skipped with an ERROR log entry; the
        remaining documents are still returned.

        Returns:
            A flat list of Documents across all discovered PDF files.
        """
        paths = self.pdf_paths
        all_docs: list[Document] = []
        for pdf_path in paths:
            try:
                all_docs.extend(self.parse_document(pdf_path))
            except (DocumentParserError, FileNotFoundError) as exc:
                logger.error("Skipping '%s' due to error: %s", pdf_path.name, exc)

        logger.info(
            "Ingested %d document(s) from %d file(s) in '%s'",
            len(all_docs),
            len(paths),
            self._docs_dir,
        )
        return all_docs
