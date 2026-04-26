"""Main application entry point (FastAPI factory)."""

import logging

from fastapi import FastAPI

from src.routers import chat, documents

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(name)s: %(message)s",
)

app = FastAPI(
    title="Native Language Disease QA Bot",
    description="WHO-grounded health QA with multilingual support.",
    version="0.1.0",
)

app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
