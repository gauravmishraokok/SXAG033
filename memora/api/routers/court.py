"""Court router — hardcoded demo queue backed by demo_court.DEMO_QUEUE."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from memora.api.demo_court import DEMO_QUEUE
from memora.api.schemas.court_schemas import CourtHealthResponse, ResolveRequest

router = APIRouter(prefix="/court", tags=["court"])


@router.get("/queue")
async def get_queue() -> list[dict]:
    """Return all unresolved contradiction cards."""
    return [row["item"] for row in DEMO_QUEUE.values() if not row.get("resolved")]


@router.get("/health", response_model=CourtHealthResponse)
async def get_health() -> CourtHealthResponse:
    pending = sum(1 for r in DEMO_QUEUE.values() if not r.get("resolved"))
    resolved = sum(1 for r in DEMO_QUEUE.values() if r.get("resolved"))
    scores = [
        r["item"].get("contradiction_score", 0.0)
        for r in DEMO_QUEUE.values()
    ]
    avg = sum(scores) / len(scores) if scores else 0.0
    return CourtHealthResponse(
        pending_count=pending,
        resolved_today=resolved,
        total_quarantined_all_time=len(DEMO_QUEUE),
        average_contradiction_score=avg,
    )


@router.post("/resolve/{quarantine_id}")
async def resolve_quarantine(
    quarantine_id: str,
    payload: ResolveRequest,
) -> dict[str, object]:
    """Mark a contradiction card as resolved (accept / reject / merge)."""
    row = DEMO_QUEUE.get(quarantine_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"No card with id '{quarantine_id}'")
    if row.get("resolved"):
        raise HTTPException(status_code=409, detail="Already resolved")
    if payload.resolution not in ("accept", "reject", "merge"):
        raise HTTPException(status_code=422, detail="resolution must be accept | reject | merge")
    if payload.resolution == "merge" and not payload.merged_content:
        raise HTTPException(status_code=422, detail="merged_content required for merge")
    row["resolved"] = True
    return {"resolved": True, "quarantine_id": quarantine_id, "resolution": payload.resolution}
