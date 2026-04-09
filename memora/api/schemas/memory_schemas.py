"""Memory API schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class MemoryCubeResponse(BaseModel):
    """Serialized memory cube for API consumers."""

    id: str
    content: str
    memory_type: str
    tier: str
    tags: list[str]
    access_count: int
    created_at: str
    updated_at: str
    provenance: dict | None = None
    extra: dict = Field(default_factory=dict)


class MemoryListResponse(BaseModel):
    """List response for memory endpoints."""

    memories: list[MemoryCubeResponse]
    total: int


class MemorySearchRequest(BaseModel):
    """Search request contract."""

    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)
    memory_types: list[str] | None = None
