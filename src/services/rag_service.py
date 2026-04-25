"""RAG service: retrieves context and generates a grounded answer via LLM."""

import logging
from pathlib import Path

import yaml
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from src.llms import LLMFactory
from src.retrievers.retriever import RAGRetriever
from src.schemas.pydantic.rag_schemas import QueryRequest, SourceDocument

from pprint import pprint

logger = logging.getLogger(__name__)

_PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
_DEFAULT_CONFIG_PATH: Path = _PROJECT_ROOT / "config" / "rag.yaml"
_DEFAULT_PROMPT_PATH: Path = _PROJECT_ROOT / "config" / "prompt.yaml"

_NO_CONTEXT_ANSWER = (
    "I do not have sufficient information in my knowledge base to answer this question."
)
_DISCLAIMER = (
    "DISCLAIMER: This information is for general awareness only. "
    "Always consult a qualified healthcare professional for medical advice, "
    "diagnosis, or treatment."
)


class RAGService:
    """Orchestrates retrieval and LLM augmentation for the health QA pipeline.

    Composes RAGRetriever and LLMFactory. Formats a grounded prompt with
    numbered context chunks, invokes the LLM, and returns a structured
    response dict with answer text, source citations, and disclaimer.

    Args:
        config_path: Path to rag.yaml. Defaults to config/rag.yaml.
        prompt_path: Path to prompt.yaml. Defaults to config/prompt.yaml.
    """

    def __init__(
        self,
        config_path: str | Path | None = None,
        prompt_path: str | Path | None = None,
    ) -> None:
        self._retriever = RAGRetriever(config_path)
        llm = LLMFactory(config_path).build()
        self._prompt = self._load_prompt(
            Path(prompt_path) if prompt_path else _DEFAULT_PROMPT_PATH
        )
        self._chain = self._prompt | llm

    def _load_prompt(self, prompt_path: Path) -> ChatPromptTemplate:
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt config not found: {prompt_path}")
        with prompt_path.open("r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
        tmpl = raw["rag_qa"]
        return ChatPromptTemplate.from_messages([
            ("system", tmpl["system"]),
            ("human", tmpl["human"]),
        ])

    def _format_context(self, docs: list[Document]) -> str:
        sections = []
        for i, doc in enumerate(docs, start=1):
            source = doc.metadata.get("source_file", "unknown")
            page = doc.metadata.get("page", "unknown")
            sections.append(f"[{i}] Source: {source}, Page {page}\n{doc.page_content}")
        return "\n\n".join(sections)

    def _extract_sources(self, docs: list[Document]) -> list[SourceDocument]:
        return [
            SourceDocument(
                source_file=doc.metadata.get("source_file", "unknown"),
                disease_topic=doc.metadata.get("disease_topic", "unknown"),
                page=doc.metadata.get("page", "unknown"),
            )
            for doc in docs
        ]

    def answer(self, request: QueryRequest) -> dict:
        """Answer a health question using retrieved WHO context.

        Args:
            request: Validated QueryRequest with query, language, and k.

        Returns:
            dict with keys:
                answer (str): LLM response grounded in retrieved context.
                sources (list[dict]): Citation metadata for retrieved chunks.
                disclaimer (str): Fixed medical safety disclaimer.
        """
        docs = self._retriever.retrieve(request.query, k=request.k)
        print('============= Docs =============')

        pprint(docs)
        
        print('============= Docs =============')

        if not docs:
            logger.warning("RAGService: no documents retrieved for query: %r", request.query)
            return {
                "answer": _NO_CONTEXT_ANSWER,
                "sources": [],
                "disclaimer": _DISCLAIMER,
            }

        context = self._format_context(docs)
        ai_message = self._chain.invoke({
            "context": context,
            "question": request.query,
            "language": request.language,
        })

        logger.info("RAGService: answered query=%r language=%s", request.query[:80], request.language)
        return {
            "answer": ai_message.content,
            "sources": [src.model_dump() for src in self._extract_sources(docs)],
            "disclaimer": _DISCLAIMER,
        }
