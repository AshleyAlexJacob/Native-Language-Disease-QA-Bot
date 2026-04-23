"""Unit tests for src.pipelines.ingestion_pipeline.IngestionPipeline."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml
from langchain_core.documents import Document

from src.pipelines.ingestion_pipeline import IngestionPipeline


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_pdf(path: Path, num_pages: int = 2) -> Path:
    from pypdf import PdfWriter

    writer = PdfWriter()
    for _ in range(num_pages):
        writer.add_blank_page(width=200, height=200)
    with path.open("wb") as fh:
        writer.write(fh)
    return path


@pytest.fixture()
def docs_dir(tmp_path: Path) -> Path:
    _make_pdf(tmp_path / "cancer.pdf", num_pages=2)
    _make_pdf(tmp_path / "influenza.pdf", num_pages=3)
    return tmp_path


@pytest.fixture()
def valid_config(tmp_path: Path, docs_dir: Path) -> Path:
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


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestIngestionPipeline:
    def test_run_returns_documents(self, valid_config: Path) -> None:
        pipeline = IngestionPipeline(config_path=valid_config)
        docs = pipeline.run()
        assert isinstance(docs, list)
        assert len(docs) > 0
        assert all(isinstance(d, Document) for d in docs)

    def test_run_returns_empty_on_empty_dir(self, tmp_path: Path) -> None:
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
        pipeline = IngestionPipeline(config_path=config_path)
        assert pipeline.run() == []

    def test_run_delegates_to_parser(self, valid_config: Path) -> None:
        fake_doc = Document(
            page_content="test",
            metadata={"source_file": "test.pdf", "page_count": 1},
        )
        with patch("src.pipelines.ingestion_pipeline.DocumentParser") as MockParser:
            instance = MockParser.return_value
            instance.pdf_paths = [Path("test.pdf")]
            instance.docs_dir = Path("/fake/dir")
            instance.parse_document.return_value = [fake_doc]

            pipeline = IngestionPipeline(config_path=valid_config)
            docs = pipeline.run()

        instance.parse_document.assert_called_once()
        assert docs == [fake_doc]

    def test_run_total_page_count(self, valid_config: Path) -> None:
        pipeline = IngestionPipeline(config_path=valid_config)
        docs = pipeline.run()
        # cancer.pdf = 2 pages, influenza.pdf = 3 pages → 5 total
        assert len(docs) == 5

    def test_run_logs_summary(
        self, valid_config: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        import logging

        with caplog.at_level(logging.INFO, logger="src.pipelines.ingestion_pipeline"):
            pipeline = IngestionPipeline(config_path=valid_config)
            pipeline.run()

        messages = " ".join(caplog.messages)
        assert "Ingestion complete" in messages
