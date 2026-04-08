from typing import Callable, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import json
from memora.core.types import MemCube, MemoryType

class SymbolicRetriever:
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self.session_factory = session_factory

    async def search_by_tags(self, tags: list[str], top_k: int = 10) -> list[MemCube]:
        sql = text("""
            SELECT id, content, memory_type, tier, tags, embedding, provenance, access_count, ttl_seconds, extra
            FROM mem_cubes
            WHERE tags @> :tags::jsonb
            ORDER BY access_count DESC, provenance->>'updated_at' DESC
            LIMIT :limit
        """)
        async with self.session_factory() as session:
            result = await session.execute(sql, {"tags": json.dumps(tags), "limit": top_k})
            rows = result.fetchall()
            cubes = []
            for row in rows:
                cubes.append(self._row_to_cube(row))
            return cubes

    async def search_by_type(self, memory_type: MemoryType, session_id: Optional[str] = None, limit: int = 20) -> list[MemCube]:
        if session_id:
            sql = text("""
                SELECT id, content, memory_type, tier, tags, embedding, provenance, access_count, ttl_seconds, extra
                FROM mem_cubes
                WHERE memory_type = :memory_type AND provenance->>'session_id' = :session_id
                ORDER BY access_count DESC, provenance->>'updated_at' DESC
                LIMIT :limit
            """)
            params = {"memory_type": memory_type.value, "session_id": session_id, "limit": limit}
        else:
            sql = text("""
                SELECT id, content, memory_type, tier, tags, embedding, provenance, access_count, ttl_seconds, extra
                FROM mem_cubes
                WHERE memory_type = :memory_type
                ORDER BY access_count DESC, provenance->>'updated_at' DESC
                LIMIT :limit
            """)
            params = {"memory_type": memory_type.value, "limit": limit}
            
        async with self.session_factory() as session:
            result = await session.execute(sql, params)
            rows = result.fetchall()
            cubes = []
            for row in rows:
                cubes.append(self._row_to_cube(row))
            return cubes

    def _row_to_cube(self, row) -> MemCube:
        d = dict(row._mapping)
        # SQLAlchemy returns dict or lists based on column type, for JSON types tags, provenance, extra
        return MemCube.from_dict(d)
