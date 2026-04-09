"""Court and quarantine API schemas."""

from __future__ import annotations

from pydantic import BaseModel


class QuarantineItemResponse(BaseModel):
    """Single quarantine queue item."""

    quarantine_id: str
    incoming_content: str
    incoming_cube_id: str
    conflicting_cube_id: str
    contradiction_score: float
    reasoning: str
    suggested_resolution: str | None
    created_at: str


class ResolveRequest(BaseModel):
    """Resolution payload for court actions."""

    resolution: str
    merged_content: str = ""


class CourtHealthResponse(BaseModel):
    """Court health and queue metrics."""

    pending_count: int
    resolved_today: int
    total_quarantined_all_time: int
    average_contradiction_score: float
