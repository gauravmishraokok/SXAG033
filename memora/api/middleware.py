"""App middleware and error handlers."""

from __future__ import annotations

import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from memora.core.errors import AlreadyResolvedError, MemoryNotFoundError, QuarantineNotFoundError

logger = logging.getLogger(__name__)


def register_middleware(app: FastAPI) -> None:
    """Register CORS and timing middleware."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def request_timing(request: Request, call_next):
        started = time.perf_counter()
        response = await call_next(request)
        ms = (time.perf_counter() - started) * 1000.0
        response.headers["X-Response-Time"] = f"{ms:.2f}"
        logger.info("%s %s -> %s (%.2fms)", request.method, request.url.path, response.status_code, ms)
        return response


def register_error_handlers(app: FastAPI) -> None:
    """Register typed exception mappers."""

    @app.exception_handler(MemoryNotFoundError)
    async def memory_not_found_handler(request: Request, exc: MemoryNotFoundError):  # noqa: ARG001
        return JSONResponse(status_code=404, content={"error": str(exc)})

    @app.exception_handler(QuarantineNotFoundError)
    async def quarantine_not_found_handler(request: Request, exc: QuarantineNotFoundError):  # noqa: ARG001
        return JSONResponse(status_code=404, content={"error": str(exc)})

    @app.exception_handler(AlreadyResolvedError)
    async def already_resolved_handler(request: Request, exc: AlreadyResolvedError):  # noqa: ARG001
        return JSONResponse(status_code=409, content={"error": str(exc)})
