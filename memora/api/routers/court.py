"""Court router endpoints."""

from __future__ import annotations

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException

from memora.api.dependencies import get_db, get_quarantine_manager, get_resolution_handler
from memora.storage.mongo.collections import MEM_CUBES
from memora.api.schemas.court_schemas import ResolveRequest
from memora.core.errors import AlreadyResolvedError, QuarantineNotFoundError
from memora.core.types import QuarantineStatus

router = APIRouter(prefix="/court", tags=["court"])


def quarantine_to_response(doc: dict, conflicting_content: str = "") -> dict:
    incoming_doc = doc.get("incoming_cube_doc") or {}
    created_at = doc.get("created_at", "")
    if hasattr(created_at, "isoformat"):
        created_at = created_at.isoformat()
    return {
        "quarantine_id": doc["_id"],
        "incoming_content": incoming_doc.get("content", ""),
        "incoming_cube_id": doc.get("incoming_cube_id", ""),
        "conflicting_cube_id": doc.get("conflicting_id", ""),
        "conflicting_content": conflicting_content,
        "contradiction_score": doc.get("contradiction_score", 0.0),
        "reasoning": doc.get("reasoning", ""),
        "suggested_resolution": doc.get("suggested_resolution"),
        "created_at": created_at,
    }


@router.get("/queue")
async def get_queue(mgr=Depends(get_quarantine_manager), db=Depends(get_db)):
    items = await mgr.repo.list_pending()
    out = []
    for item in items:
        conflict_text = ""
        cid = item.get("conflicting_id")
        if cid:
            cdoc = await db[MEM_CUBES].find_one({"_id": cid})
            if cdoc:
                conflict_text = cdoc.get("content", "") or ""
        out.append(quarantine_to_response(item, conflicting_content=conflict_text))
    return out


@router.get("/health")
async def get_health(mgr=Depends(get_quarantine_manager)):
    # Prefer manager-level health if available and compatible.
    try:
        return await mgr.get_health()
    except Exception:
        # Fallback to repo-backed aggregation to stay resilient.
        records = mgr.repo.collection
        now = datetime.utcnow()
        start_of_day = datetime(now.year, now.month, now.day)

        pending_count = await records.count_documents({"status": QuarantineStatus.PENDING.value})
        resolved_today = await records.count_documents({
            "status": {"$ne": QuarantineStatus.PENDING.value},
            "resolved_at": {"$gte": start_of_day, "$lt": start_of_day + timedelta(days=1)},
        })
        total = await records.count_documents({})
        pipeline = [
            {"$group": {"_id": None, "avg_score": {"$avg": "$contradiction_score"}}}
        ]
        agg = await records.aggregate(pipeline).to_list(length=1)
        avg_score = float(agg[0]["avg_score"]) if agg and agg[0].get("avg_score") is not None else 0.0
        return {
            "pending_count": pending_count,
            "resolved_today": resolved_today,
            "total_quarantined_all_time": total,
            "average_contradiction_score": avg_score,
        }


@router.post("/resolve/{quarantine_id}")
async def resolve_quarantine(
    quarantine_id: str,
    payload: ResolveRequest,
    handler=Depends(get_resolution_handler),
):
    resolution_map = {
        "accept": QuarantineStatus.RESOLVED_ACCEPT,
        "reject": QuarantineStatus.RESOLVED_REJECT,
        "merge": QuarantineStatus.RESOLVED_MERGE,
    }
    if payload.resolution not in resolution_map:
        raise HTTPException(status_code=422, detail="resolution must be accept|reject|merge")
    try:
        await handler.resolve(
            quarantine_id=quarantine_id,
            resolution=resolution_map[payload.resolution],
            merged_content=payload.merged_content or "",
        )
        return {"resolved": True, "quarantine_id": quarantine_id}
    except QuarantineNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"Quarantine not found: {quarantine_id}") from exc
    except AlreadyResolvedError as exc:
        raise HTTPException(status_code=409, detail="Already resolved") from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
