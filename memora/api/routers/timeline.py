"""Timeline endpoints."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, Query

from memora.api.dependencies import get_db

router = APIRouter(prefix="/timeline", tags=["timeline"])


@router.get("")
async def get_timeline(
    session_id: str | None = None,
    limit: int = Query(default=50, le=200),
    before: str | None = None,
    db=Depends(get_db),
) -> dict[str, object]:
    """Return timeline events for a session."""
    from memora.storage.mongo.collections import TIMELINE_EVENTS

    query = {}
    if session_id:
        query["session_id"] = session_id
    if before:
        query["created_at"] = {"$lt": datetime.fromisoformat(before)}

    collection = db[TIMELINE_EVENTS]
    cursor = collection.find(query, sort=[("created_at", -1)], limit=limit)
    events = await cursor.to_list(limit)
    total = await collection.count_documents(query)

    return {
        "events": [
            {
                "id": e["_id"],
                "cube_id": e.get("cube_id"),
                "event_type": e.get("event_type"),
                "description": e.get("description"),
                "session_id": e.get("session_id"),
                "metadata": e.get("metadata", {}),
                "created_at": e["created_at"].isoformat() if hasattr(e.get("created_at"), "isoformat") else str(e.get("created_at", "")),
            }
            for e in reversed(events)
        ],
        "total": total,
    }
