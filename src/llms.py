"""LLM factory: builds ChatGoogleGenerativeAI (primary) with ChatOpenRouter as fallback."""

import logging
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel

logger = logging.getLogger(__name__)

_PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
_DEFAULT_CONFIG_PATH: Path = _PROJECT_ROOT / "config" / "rag.yaml"

load_dotenv(_PROJECT_ROOT / ".env")


class LLMFactory:
    """Reads config/rag.yaml [llm] section and builds a LangChain chat model.

    Returns ChatGoogleGenerativeAI (Gemini 2.5 Flash) as the primary model with
    ChatOpenRouter as an automatic fallback via LangChain's .with_fallbacks().
    If the Google API call fails, the chain transparently retries with OpenRouter.

    Args:
        config_path: Path to rag.yaml. Defaults to config/rag.yaml.

    Raises:
        FileNotFoundError: If the config file does not exist.
        KeyError: If the 'llm' section is absent from the config.
    """

    def __init__(self, config_path: str | Path | None = None) -> None:
        resolved = Path(config_path) if config_path else _DEFAULT_CONFIG_PATH
        self._cfg = self._load_config(resolved)

    def _load_config(self, config_path: Path) -> dict:
        if not config_path.exists():
            raise FileNotFoundError(f"RAG config not found: {config_path}")
        with config_path.open("r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
        if "llm" not in raw:
            raise KeyError("'llm' section missing from config/rag.yaml")
        return raw["llm"]

    def _build_google(self) -> BaseChatModel:
        from langchain_google_genai import ChatGoogleGenerativeAI  # noqa: PLC0415

        return ChatGoogleGenerativeAI(
            model=self._cfg.get("google_model", "gemini-2.5-flash-preview-04-17"),
            google_api_key=os.environ["GOOGLE_API_KEY"],
            temperature=self._cfg.get("temperature", 0.1),
            max_output_tokens=self._cfg.get("max_tokens", 1024),
            max_retries=self._cfg.get("max_retries", 2),
        )

    def _build_openrouter(self) -> BaseChatModel:
        from langchain_openrouter import ChatOpenRouter  # noqa: PLC0415

        return ChatOpenRouter(
            model=self._cfg.get("openrouter_model", "meta-llama/llama-3.2-3b-instruct:free"),
            temperature=self._cfg.get("temperature", 0.1),
            max_tokens=self._cfg.get("max_tokens", 1024),
            max_retries=self._cfg.get("max_retries", 2),
        )

    def build(self) -> BaseChatModel:
        """Build and return Gemini 2.5 Flash with ChatOpenRouter as automatic fallback.

        Returns:
            RunnableWithFallbacks: Google Gemini primary, OpenRouter fallback.
        """
        primary = self._build_google()
        fallback = self._build_openrouter()
        logger.info(
            "LLMFactory: primary=%s, fallback=%s",
            self._cfg.get("google_model"),
            self._cfg.get("openrouter_model"),
        )
        return primary.with_fallbacks([fallback])
