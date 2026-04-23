"""Unit tests for src.core.document_parser.DocumentParser."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml
from langchain_core.documents import Document

from src.core.document_parser import DocumentParser, DocumentParserError


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_pdf(path: Path, num_pages: int = 2) -> Path:
    """Write a minimal valid PDF with blank pages using pypdf."""
    from pypdf import PdfWriter

    writer = PdfWriter()
    for _ in range(num_pages):
        writer.add_blank_page(width=200, height=200)
    with path.open("wb") as fh:
        writer.write(fh)
    return path


@pytest.fixture()
def docs_dir(tmp_path: Path) -> Path:
    """A temporary directory containing two minimal PDFs."""
    _make_pdf(tmp_path / "malaria.pdf", num_pages=3)
    _make_pdf(tmp_path / "dengue.pdf", num_pages=2)
    return tmp_path


@pytest.fixture()
def valid_config(tmp_path: Path, docs_dir: Path) -> Path:
    """A rag.yaml pointing at docs_dir."""
    cfg = {
        "document_parser": {
            "docs_dir": str(docs_dir),
            "file_extension": ".pdf",
            "recursive": False,
        }
    }
    config_path = tmp_path / "rag.yaml"
    config_path.write_text(yaml.dump(cfg))
    return config_path


@pytest.fixture()
def parser(valid_config: Path) -> DocumentParser:
    return DocumentParser(config_path=valid_config)


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------


class TestLoadConfig:
    def test_valid_config_instantiates(self, valid_config: Path) -> None:
        parser = DocumentParser(config_path=valid_config)
        assert parser is not None

    def test_missing_config_raises_file_not_found(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError, match="RAG config not found"):
            DocumentParser(config_path=tmp_path / "nonexistent.yaml")

    def test_missing_section_raises_key_error(self, tmp_path: Path) -> None:
        bad_config = tmp_path / "bad.yaml"
        bad_config.write_text(yaml.dump({"other_section": {}}))
        with pytest.raises(KeyError, match="document_parser"):
            DocumentParser(config_path=bad_config)

    def test_custom_config_path_respected(self, valid_config: Path) -> None:
        parser = DocumentParser(config_path=str(valid_config))
        assert parser.docs_dir.exists()


# ---------------------------------------------------------------------------
# Directory resolution
# ---------------------------------------------------------------------------


class TestDocsDir:
    def test_docs_dir_returns_path(self, parser: DocumentParser) -> None:
        assert isinstance(parser.docs_dir, Path)

    def test_docs_dir_exists(self, parser: DocumentParser) -> None:
        assert parser.docs_dir.exists()

    def test_missing_docs_dir_raises(self, tmp_path: Path) -> None:
        cfg = {
            "document_parser": {
                "docs_dir": str(tmp_path / "nonexistent"),
                "file_extension": ".pdf",
                "recursive": False,
            }
        }
        config_path = tmp_path / "rag.yaml"
        config_path.write_text(yaml.dump(cfg))
        with pytest.raises(FileNotFoundError, match="Documents directory not found"):
            DocumentParser(config_path=config_path)

    def test_absolute_docs_dir_in_config(self, tmp_path: Path, docs_dir: Path) -> None:
        cfg = {
            "document_parser": {
                "docs_dir": str(docs_dir),  # absolute
                "file_extension": ".pdf",
                "recursive": False,
            }
        }
        config_path = tmp_path / "rag.yaml"
        config_path.write_text(yaml.dump(cfg))
        parser = DocumentParser(config_path=config_path)
        assert parser.docs_dir == docs_dir


# ---------------------------------------------------------------------------
# pdf_paths property
# ---------------------------------------------------------------------------


class TestPdfPaths:
    def test_returns_only_pdfs(self, docs_dir: Path, parser: DocumentParser) -> None:
        (docs_dir / "readme.txt").write_text("hello")
        assert all(p.suffix == ".pdf" for p in parser.pdf_paths)

    def test_empty_dir_returns_empty_list(self, tmp_path: Path) -> None:
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        cfg = {
            "document_parser": {
                "docs_dir": str(empty_dir),
                "file_extension": ".pdf",
                "recursive": False,
            }
        }
        config_path = tmp_path / "rag.yaml"
        config_path.write_text(yaml.dump(cfg))
        parser = DocumentParser(config_path=config_path)
        assert parser.pdf_paths == []

    def test_paths_are_sorted(self, parser: DocumentParser) -> None:
        paths = parser.pdf_paths
        assert paths == sorted(paths)

    def test_non_recursive_excludes_subdirectory(
        self, tmp_path: Path, docs_dir: Path
    ) -> None:
        subdir = docs_dir / "subdir"
        subdir.mkdir()
        _make_pdf(subdir / "typhoid.pdf")
        cfg = {
            "document_parser": {
                "docs_dir": str(docs_dir),
                "file_extension": ".pdf",
                "recursive": False,
            }
        }
        config_path = tmp_path / "rag.yaml"
        config_path.write_text(yaml.dump(cfg))
        parser = DocumentParser(config_path=config_path)
        names = [p.name for p in parser.pdf_paths]
        assert "typhoid.pdf" not in names

    def test_recursive_includes_subdirectory(
        self, tmp_path: Path, docs_dir: Path
    ) -> None:
        subdir = docs_dir / "subdir"
        subdir.mkdir()
        _make_pdf(subdir / "typhoid.pdf")
        cfg = {
            "document_parser": {
                "docs_dir": str(docs_dir),
                "file_extension": ".pdf",
                "recursive": True,
            }
        }
        config_path = tmp_path / "rag.yaml"
        config_path.write_text(yaml.dump(cfg))
        parser = DocumentParser(config_path=config_path)
        names = [p.name for p in parser.pdf_paths]
        assert "typhoid.pdf" in names


# ---------------------------------------------------------------------------
# parse_document
# ---------------------------------------------------------------------------


class TestParseDocument:
    def test_returns_list_of_documents(
        self, parser: DocumentParser, docs_dir: Path
    ) -> None:
        pdf = docs_dir / "malaria.pdf"
        docs = parser.parse_document(pdf)
        assert isinstance(docs, list)
        assert len(docs) > 0
        assert all(isinstance(d, Document) for d in docs)

    def test_metadata_injected(self, parser: DocumentParser, docs_dir: Path) -> None:
        pdf = docs_dir / "malaria.pdf"
        docs = parser.parse_document(pdf)
        for doc in docs:
            assert doc.metadata["disease_topic"] == "malaria"
            assert doc.metadata["source_file"] == "malaria.pdf"
            assert doc.metadata["page_count"] == len(docs)

    def test_file_not_found_raises(self, parser: DocumentParser) -> None:
        with pytest.raises(FileNotFoundError):
            parser.parse_document(Path("/nonexistent/path/file.pdf"))

    def test_bad_pdf_raises_document_parser_error(
        self, parser: DocumentParser, docs_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def boom(_self: object) -> list:
            raise RuntimeError("corrupt")

        monkeypatch.setattr(
            "langchain_community.document_loaders.PyPDFLoader.load", boom
        )
        with pytest.raises(DocumentParserError, match="Failed to parse"):
            parser.parse_document(docs_dir / "malaria.pdf")


# ---------------------------------------------------------------------------
# parse_all_documents
# ---------------------------------------------------------------------------


class TestParseAllDocuments:
    def test_returns_flat_list(self, parser: DocumentParser) -> None:
        docs = parser.parse_all_documents()
        assert isinstance(docs, list)
        assert all(isinstance(d, Document) for d in docs)

    def test_empty_dir_returns_empty(self, tmp_path: Path) -> None:
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        cfg = {
            "document_parser": {
                "docs_dir": str(empty_dir),
                "file_extension": ".pdf",
                "recursive": False,
            }
        }
        config_path = tmp_path / "rag.yaml"
        config_path.write_text(yaml.dump(cfg))
        parser = DocumentParser(config_path=config_path)
        assert parser.parse_all_documents() == []

    def test_continues_on_single_file_error(
        self, parser: DocumentParser, docs_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        original_parse = parser.parse_document

        def failing_once(path: Path) -> list[Document]:
            if path.name == "dengue.pdf":
                raise DocumentParserError("simulated failure")
            return original_parse(path)

        monkeypatch.setattr(parser, "parse_document", failing_once)
        docs = parser.parse_all_documents()
        assert len(docs) > 0

    def test_total_page_count(self, parser: DocumentParser, docs_dir: Path) -> None:
        docs = parser.parse_all_documents()
        # malaria.pdf = 3 pages, dengue.pdf = 2 pages → 5 total
        assert len(docs) == 5
