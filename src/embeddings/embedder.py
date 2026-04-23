"""Embedding model wrapper for the RAG ingestion pipeline."""

import logging
from pathlib import Path

import yaml
from langchain_ollama import OllamaEmbeddings

logger = logging.getLogger(__name__)

_PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
_DEFAULT_CONFIG_PATH: Path = _PROJECT_ROOT / "config" / "rag.yaml"


class DocumentEmbedder:
    """Wraps OllamaEmbeddings for use in the RAG pipeline.

    Reads provider, model, and base_url from the ``embeddings`` section
    of the RAG YAML config. Currently supports ``provider: ollama`` only.

    Args:
        config_path: Path to the RAG YAML config file. Defaults to
            ``config/rag.yaml`` relative to the project root.

    Raises:
        FileNotFoundError: If the config file does not exist.
        KeyError: If the ``embeddings`` section is absent from the config.
        ValueError: If an unsupported provider is specified.
    """

    def __init__(self, config_path: str | Path | None = None) -> None:
        resolved = Path(config_path) if config_path else _DEFAULT_CONFIG_PATH
        cfg = self._load_config(resolved)
        self.embeddings = self._build_embeddings(cfg)

    def _load_config(self, config_path: Path) -> dict:
        if not config_path.exists():
            raise FileNotFoundError(f"RAG config not found: {config_path}")
        with config_path.open("r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
        if "embeddings" not in raw:
            raise KeyError("'embeddings' section missing from config")
        cfg = raw["embeddings"]
        logger.debug("Loaded embeddings config: %s", cfg)
        return cfg

    def _build_embeddings(self, cfg: dict) -> OllamaEmbeddings:
        provider = cfg.get("provider", "ollama")
        if provider != "ollama":
            raise ValueError(f"Unsupported embeddings provider: '{provider}'")
        return OllamaEmbeddings(
            model=cfg["model"],
            base_url=cfg.get("base_url", "http://localhost:11434"),
        )
