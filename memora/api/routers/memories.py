"""Memory router endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from memora.api.dependencies import get_db, get_episodic_repo, get_retriever
from memora.core.errors import MemoryNotFoundError

router = APIRouter(prefix="/memories", tags=["memories"])


def cube_to_response(cube) -> dict:
    return {
        "id": cube.id,
        "content": cube.content,
        "memory_type": cube.memory_type.value,
        "tier": cube.tier.value,
        "tags": cube.tags,
        "access_count": cube.access_count,
        "created_at": cube.provenance.created_at.isoformat() if cube.provenance else "",
        "updated_at": cube.provenance.updated_at.isoformat() if cube.provenance else "",
        "provenance": {
            "origin": cube.provenance.origin,
            "session_id": cube.provenance.session_id,
            "version": cube.provenance.version,
            "parent_id": cube.provenance.parent_id,
        } if cube.provenance else None,
        "extra": cube.extra or {},
    }


@router.get("")
async def list_memories(
    session_id: str | None = None,
    limit: int = Query(default=20, le=100),
    episodic_repo=Depends(get_episodic_repo),
    db=Depends(get_db),
):
    _ = episodic_repo  # repository is part of contract; db is used for query flexibility
    from memora.storage.mongo.collections import MEM_CUBES
    from memora.storage.vector.mongo_vector_client import _doc_to_cube

    query = {}
    if session_id:
        query["provenance.session_id"] = session_id

    collection = db[MEM_CUBES]
    cursor = collection.find(query, sort=[("provenance.created_at", -1)], limit=limit)
    docs = await cursor.to_list(limit)
    total = await collection.count_documents(query)

    return {
        "memories": [cube_to_response(_doc_to_cube(doc)) for doc in docs],
        "total": total,
    }


@router.get("/search")
async def search_memories(
    q: str = Query(..., min_length=1),
    top_k: int = Query(default=5, ge=1, le=20),
    retriever=Depends(get_retriever),
):
    results = await retriever.search(q, top_k=top_k)
    return {
        "memories": [cube_to_response(c) for c in results],
        "total": len(results),
    }


@router.get("/{cube_id}")
async def get_memory(cube_id: str, db=Depends(get_db)):
    from memora.storage.mongo.collections import MEM_CUBES
    from memora.storage.vector.mongo_vector_client import _doc_to_cube

    doc = await db[MEM_CUBES].find_one({"_id": cube_id})
    if not doc:
        raise HTTPException(status_code=404, detail=f"Memory not found: {cube_id}")
    return cube_to_response(_doc_to_cube(doc))


@router.delete("/{cube_id}")
async def delete_memory(cube_id: str, episodic_repo=Depends(get_episodic_repo)):
    try:
        await episodic_repo.delete(cube_id)
        return {"deleted": True}
    except MemoryNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"Memory not found: {cube_id}") from exc
