"""FastAPI application entrypoint for MEMORA."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from memora.api.middleware import register_error_handlers, register_middleware
from memora.api.routers import chat, court, graph, health, memories, timeline
from memora.core.config import get_settings
from memora.core.events import bus


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and tear down app-scoped services."""
    settings = get_settings()
    app.state.agent = None
    app.state.retriever = None
    app.state.quarantine_mgr = None
    app.state.resolution_handler = None
    app.state.episodic_repo = None
    app.state.kg_repo = None
    app.state.settings = settings
    try:
        yield
    finally:
        bus.clear()


def create_app() -> FastAPI:
    """Create configured FastAPI app."""
    app = FastAPI(
        title="MEMORA",
        description="Persistent Memory for Long-Running Agents",
        version="0.1.0",
        lifespan=lifespan,
    )
    register_middleware(app)
    register_error_handlers(app)
    app.include_router(chat.router)
    app.include_router(memories.router)
    app.include_router(court.router)
    app.include_router(graph.router)
    app.include_router(timeline.router)
    app.include_router(health.router)
    return app


app = create_app()
