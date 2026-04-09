"""Health and observability endpoints."""

from __future__ import annotations

import time

from fastapi import APIRouter, Depends

from memora.api.dependencies import get_db, get_quarantine_manager

router = APIRouter(prefix="", tags=["health"])
_start_time = time.time()
_latency_samples: list[float] = []


@router.get("/health")
async def get_health(
    db=Depends(get_db),
    quarantine_mgr=Depends(get_quarantine_manager),
) -> dict[str, object]:
    """Return app health with memory and latency metrics."""
    from memora.storage.mongo.collections import MEM_CUBES

    try:
        await db.command("ping")
        db_ok = True
    except Exception:
        db_ok = False

    collection = db[MEM_CUBES]
    total = await collection.count_documents({})

    hot = await collection.count_documents({"tier": "hot"})
    warm = await collection.count_documents({"tier": "warm"})
    cold = await collection.count_documents({"tier": "cold"})

    episodic = await collection.count_documents({"memory_type": "episodic"})
    semantic = await collection.count_documents({"memory_type": "semantic"})
    kg_node = await collection.count_documents({"memory_type": "kg_node"})

    try:
        health_data = await quarantine_mgr.get_health()
        pending = health_data.get("pending_count", 0)
    except Exception:
        pending = 0

    ordered = sorted(_latency_samples)
    p50 = ordered[len(ordered) // 2] if ordered else 0.0
    p99_idx = int(len(ordered) * 0.99)
    p99 = ordered[p99_idx] if ordered else 0.0

    return {
        "status": "ok" if db_ok else "degraded",
        "total_memories": total,
        "memories_by_tier": {"hot": hot, "warm": warm, "cold": cold},
        "memories_by_type": {"episodic": episodic, "semantic": semantic, "kg_node": kg_node},
        "retrieval_latency_p50_ms": round(p50, 1),
        "retrieval_latency_p99_ms": round(p99, 1),
        "quarantine_pending": pending,
        "db_connected": db_ok,
        "uptime_seconds": round(time.time() - _start_time, 1),
    }
