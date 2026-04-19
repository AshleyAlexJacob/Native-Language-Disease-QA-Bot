"""End-to-end smoke test: load malaria.pdf, chunk, embed, store in ChromaDB, then query."""

import logging
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from src.core.document_parser import DocumentParser
from src.vectorstores.vector_db_service import VectorDBService

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("smoke_test_embeddings")

_TEST_PDF = _PROJECT_ROOT / "docs" / "who_guides_doc" / "malaria.pdf"

_QUERIES = [
    "What are the symptoms of malaria?",
    "How is malaria transmitted?",
    "What treatments are recommended for malaria?",
]


def main() -> None:
    logger.info("=== Smoke Test: Embeddings + ChromaDB ===")

    # 1. Parse malaria.pdf only
    parser = DocumentParser()
    docs = parser.parse_document(_TEST_PDF)
    logger.info("Parsed %d page(s) from %s", len(docs), _TEST_PDF.name)

    # 2. Reset store, then ingest (chunk + embed + store)
    service = VectorDBService()
    service.reset()
    ids = service.ingest_documents(docs)
    logger.info("Stored %d chunk(s) in ChromaDB.", len(ids))

    # 3. Run test queries and print results
    for query in _QUERIES:
        print(f"\n{'=' * 60}")
        print(f"QUERY: {query}")
        print("=" * 60)
        results = service.search(query, k=3)
        if not results:
            print("  [no results returned]")
            continue
        for rank, (doc, score) in enumerate(results, start=1):
            print(f"\n  Result #{rank}  |  score={score:.4f}")
            print(f"  Source : {doc.metadata.get('source_file', 'unknown')}")
            print(f"  Topic  : {doc.metadata.get('disease_topic', 'unknown')}")
            print(f"  Page   : {doc.metadata.get('page', 'unknown')}")
            snippet = doc.page_content[:300].replace("\n", " ")
            print(f"  Chunk  : {snippet}...")

    logger.info("=== Smoke test complete ===")


if __name__ == "__main__":
    main()
