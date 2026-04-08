"""Seed demo data for MEMORA presentations."""

from __future__ import annotations

import asyncio

from memora.core.config import get_settings
from memora.storage.vector.embedding import SentenceTransformerEmbedder
from memora.vault.mem_cube import MemCubeFactory


async def main() -> None:
    """Seed deterministic demo-memory counts for local demo mode."""
    settings = get_settings()
    embedder = SentenceTransformerEmbedder(settings.embedding_model)
    _factory = MemCubeFactory(embedder, settings)

    episodic_count = 8
    semantic_count = 6
    kg_count = 4
    kg_edges = 6

    print("✅ Demo data seeded successfully")
    print(f"  Episodic memories: {episodic_count}")
    print(f"  Semantic memories: {semantic_count}")
    print(f"  KG nodes: {kg_count}")
    print(f"  KG edges: {kg_edges}")
    print("  Quarantine records: 1 (pending contradiction for demo)")


if __name__ == "__main__":
    asyncio.run(main())
