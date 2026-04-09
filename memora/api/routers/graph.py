"""Knowledge graph visualization endpoints."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from memora.api.dependencies import get_db, get_kg_repo
from memora.core.interfaces import IKGRepo

router = APIRouter(prefix="/graph", tags=["graph"])


def _extra_dict(extra: Any) -> dict:
    if isinstance(extra, dict):
        return extra
    return {}


def _short_label(content: str, extra: dict) -> str:
    title = (extra.get("label") or extra.get("title") or "").strip()
    if title:
        return title[:72] + ("…" if len(title) > 72 else "")
    c = (content or "").strip()
    first = c.split("\n")[0].strip()
    if len(first) > 72:
        return first[:69] + "…"
    return first or "·"


@router.get("/nodes")
async def get_nodes(kg_repo: IKGRepo = Depends(get_kg_repo), db=Depends(get_db)):
    """Return normalized graph nodes for D3 rendering."""
    try:
        raw_nodes = await kg_repo.get_all_nodes()
    except Exception:
        raw_nodes = []

    if not raw_nodes:
        from memora.storage.mongo.collections import MEM_CUBES
        cursor = db[MEM_CUBES].find({}, sort=[("provenance.created_at", -1)], limit=100)
        docs = await cursor.to_list(100)
        out = []
        for d in docs:
            ex = _extra_dict(d.get("extra"))
            content = d.get("content", "") or ""
            out.append(
                {
                    "id": d.get("_id", ""),
                    "label": _short_label(content, ex),
                    "type": d.get("memory_type", "episodic"),
                    "tier": d.get("tier", "warm"),
                    "content": content,
                    "tags": d.get("tags", []),
                    "access_count": d.get("access_count", 0),
                    "extra": ex,
                }
            )
        return {"nodes": out}
    out = []
    for n in raw_nodes:
        ex = _extra_dict(n.get("extra"))
        content = (n.get("content") or "") or ""
        if not content and n.get("label"):
            content = str(n.get("label"))
        short = (str(n["label"]).strip()[:72] if n.get("label") else _short_label(content, ex))
        out.append(
            {
                "id": n["id"],
                "label": short,
                "type": n.get("memory_type", n.get("type", "kg_node")),
                "tier": n.get("tier", "warm"),
                "content": content,
                "tags": n.get("tags", []),
                "access_count": n.get("access_count", 0),
                "extra": ex,
            }
        )
    return {"nodes": out}


@router.get("/edges")
async def get_edges(kg_repo: IKGRepo = Depends(get_kg_repo)):
    """Return normalized graph edges for frontend rendering."""
    try:
        raw_edges = await kg_repo.get_all_edges()
    except Exception:
        raw_edges = []
    return {
        "edges": [
            {
                "id": e.get("id", ""),
                "source": e.get("from", e.get("source", "")),
                "target": e.get("to", e.get("target", "")),
                "label": e.get("label", ""),
                "active": e.get("active", True),
            }
            for e in raw_edges
        ]
    }


@router.get("/neighbors/{cube_id}")
async def get_neighbors(cube_id: str, depth: int = 1, kg_repo: IKGRepo = Depends(get_kg_repo)):
    """Return neighbor cubes for a target graph node."""
    try:
        neighbors = await kg_repo.get_neighbors(cube_id, depth)
    except Exception:
        neighbors = []
    return {
        "neighbors": [
            {
                "id": c.id,
                "label": c.content[:30],
                "type": c.memory_type.value,
                "tier": c.tier.value,
                "content": c.content,
                "tags": c.tags,
                "access_count": c.access_count,
            }
            for c in neighbors
        ]
    }
