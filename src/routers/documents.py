"""Document management endpoints: list, upload, ingest, delete."""

import logging
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile

import src.dependencies as _deps
from src.dependencies import get_vector_db_service
from src.pipelines.ingestion_pipeline import IngestionPipeline
from src.schemas.pydantic.api_schemas import DeleteResult, DocumentInfo, IngestionResult
from src.vectorstores.vector_db_service import VectorDBService

logger = logging.getLogger(__name__)

router = APIRouter()

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_DOCS_DIR = _PROJECT_ROOT / "docs" / "who_guides_doc"


@router.get("", response_model=list[DocumentInfo])
def list_documents(
    vdb: VectorDBService = Depends(get_vector_db_service),
) -> list[DocumentInfo]:
    """List all PDF documents on disk and their ChromaDB ingestion status."""
    disk_files = {p.name for p in _DOCS_DIR.glob("*.pdf")}
    chroma_files = set(vdb.list_sources())
    all_files = sorted(disk_files | chroma_files)
    return [
        DocumentInfo(
            filename=f,
            on_disk=f in disk_files,
            in_chroma=f in chroma_files,
        )
        for f in all_files
    ]


@router.post("", response_model=list[str], status_code=201)
async def add_documents(files: list[UploadFile]) -> list[str]:
    """Upload one or more PDF files to the document store directory."""
    if not files:
        raise HTTPException(status_code=400, detail="No files provided.")

    saved: list[str] = []
    for upload in files:
        if not (upload.filename or "").lower().endswith(".pdf"):
            raise HTTPException(
                status_code=422,
                detail=f"Only PDF files are accepted. Got: {upload.filename!r}",
            )
        dest = _DOCS_DIR / upload.filename  # type: ignore[arg-type]
        with dest.open("wb") as fh:
            shutil.copyfileobj(upload.file, fh)
        saved.append(upload.filename)  # type: ignore[arg-type]
        logger.info("Saved uploaded file: %s", dest)

    return saved


@router.post("/ingest", response_model=IngestionResult)
def trigger_ingestion(
    reset: bool = Query(default=False, description="Clear ChromaDB before ingesting."),
) -> IngestionResult:
    """Run the full ingestion pipeline (parse → chunk → embed → upsert)."""
    pipeline = IngestionPipeline(reset=reset)
    ids = pipeline.run()
    if reset:
        # IngestionPipeline creates its own Chroma instance; resetting deletes the
        # collection and recreates it with a new UUID.  The cached VectorDBService
        # singleton now holds a stale reference to the old UUID, so we evict it so
        # the next request gets a fresh connection to the new collection.
        _deps.get_vector_db_service.cache_clear()
    files_processed = len(list(_DOCS_DIR.glob("*.pdf")))
    return IngestionResult(chunks_stored=len(ids), files_processed=files_processed)


@router.delete("/{filename}", response_model=DeleteResult)
def delete_document(
    filename: str,
    delete_file: bool = Query(
        default=False,
        description="Also remove the PDF from disk.",
    ),
    vdb: VectorDBService = Depends(get_vector_db_service),
) -> DeleteResult:
    """Delete a document's chunks from ChromaDB, and optionally its PDF from disk."""
    chunks_deleted = vdb.delete_by_source(filename)

    file_removed = False
    if delete_file:
        pdf_path = _DOCS_DIR / filename
        if pdf_path.exists():
            pdf_path.unlink()
            file_removed = True
            logger.info("Deleted file from disk: %s", pdf_path)

    return DeleteResult(
        filename=filename,
        chunks_deleted=chunks_deleted,
        file_removed=file_removed,
    )
