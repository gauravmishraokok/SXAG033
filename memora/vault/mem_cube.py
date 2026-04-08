"""
vault/mem_cube.py — MemCube factory + serialization helpers.

Responsibilities:
- Create MemCube instances with proper provenance
- Serialize/deserialize to/from DB row format
- Validate content before storage

Does NOT: write to DB (that's episodic_repo / semantic_repo / kg_repo)
Does NOT: decide which tier (that's tier_router)
"""
from memora.core.types import MemCube, MemoryType, MemoryTier, Provenance
from memora.storage.vector.embedding import EmbeddingModel
from typing import Optional
import uuid
from datetime import datetime


class MemCubeFactory:
    def __init__(self, embedding_model: EmbeddingModel):
        self.embedder = embedding_model

    async def create(
        self,
        content: str,
        memory_type: MemoryType,
        session_id: str,
        origin: str = "agent_inference",
        tags: list[str] | None = None,
        extra: dict | None = None,
    ) -> MemCube:
        """Create a new MemCube with embedding and provenance."""
        ...

    def to_db_row(self, cube: MemCube) -> dict:
        """Serialize MemCube to flat dict for PostgreSQL storage."""
        ...

    def from_db_row(self, row: dict) -> MemCube:
        """Deserialize from PostgreSQL row to MemCube."""
        ...
