"""Smoke test: end-to-end RAG query through RAGService."""

import logging
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from src.services.rag_service import RAGService
from src.schemas.pydantic.rag_schemas import QueryRequest

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")


if __name__ == "__main__":
    svc = RAGService()
    result = svc.answer(QueryRequest(query="ملیریا کی علامات کیا ہیں؟", language="Urdu"))
    # result = svc.answer(QueryRequest(query="What are the symptoms of Malaria?", language="Urdu"))
    
    print("\n=== Answer ===")
    print(result["answer"])
    print("\n=== Sources ===")
    for src in result["sources"]:
        print(f"  - {src['source_file']} (Page {src['page']})")
    print("\n=== Disclaimer ===")
    print(result["disclaimer"])
