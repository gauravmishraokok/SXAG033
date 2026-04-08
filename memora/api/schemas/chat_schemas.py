"""Chat request/response API schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Incoming chat payload."""

    message: str = Field(..., min_length=1, max_length=10000)
    session_id: str | None = None
    feedback: str | None = None


class ChatResponse(BaseModel):
    """Outgoing chat response payload."""

    text: str
    session_id: str
    turn_number: int
    memories_used: list[str]
    memory_count: int
