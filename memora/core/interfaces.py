"""Abstract base classes (ports) for every repository and service.

Modules depend on these interfaces, never on concrete implementations.
This is foundation of the dependency inversion that allows mocking in tests.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, Awaitable
from datetime import datetime

from .types import MemCube, MemoryType, QuarantineStatus, ContradictionVerdict


class IEpisodicRepo(ABC):
    @abstractmethod
    async def save(self, cube: MemCube) -> str:
        """Persist an episodic MemCube. Returns the cube.id."""

    @abstractmethod
    async def get(self, cube_id: str) -> Optional[MemCube]:
        """Fetch by ID. Returns None if not found."""

    @abstractmethod
    async def delete(self, cube_id: str) -> None:
        """Hard delete. Raises MemoryNotFoundError if not found."""

    @abstractmethod
    async def list_recent(self, session_id: str, limit: int = 20) -> list[MemCube]:
        """Return most recent N episodic memories for a session, newest first."""

    @abstractmethod
    async def update_access(self, cube_id: str) -> None:
        """Increment access_count and update provenance.updated_at."""


class ISemanticRepo(ABC):
    @abstractmethod
    async def save(self, cube: MemCube) -> str:
        """Persist a semantic MemCube. Returns the cube.id."""

    @abstractmethod
    async def get(self, cube_id: str) -> Optional[MemCube]:
        """Fetch by ID. Returns None if not found."""

    @abstractmethod
    async def delete(self, cube_id: str) -> None:
        """Hard delete. Raises MemoryNotFoundError if not found."""

    @abstractmethod
    async def upsert_by_key(self, key: str, cube: MemCube) -> str:
        """Upsert: if a semantic memory with this key exists, update it. Otherwise insert."""


class IKGRepo(ABC):
    @abstractmethod
    async def upsert_node(self, cube: MemCube) -> str:
        """Insert or update a KG node. Returns node ID."""

    @abstractmethod
    async def add_edge(self, from_id: str, to_id: str, label: str,
                       metadata: dict | None = None) -> str:
        """Add a directed edge. Returns edge ID. Old edges are archived, not deleted."""

    @abstractmethod
    async def deprecate_edge(self, edge_id: str, reason: str) -> None:
        """Mark edge as deprecated with a reason and deprecated_at timestamp."""

    @abstractmethod
    async def get_neighbors(self, cube_id: str, depth: int = 1) -> list[MemCube]:
        """Return all nodes reachable within `depth` hops. Active edges only."""

    @abstractmethod
    async def get_all_nodes(self) -> list[dict]:
        """For graph visualization. Returns list of {id, label, type, tier}."""

    @abstractmethod
    async def get_all_edges(self) -> list[dict]:
        """For graph visualization. Returns list of {id, from, to, label, active, deprecated_at}."""


class IQuarantineRepo(ABC):
    @abstractmethod
    async def save_pending(self, cube: MemCube,
                           verdict: ContradictionVerdict) -> str:
        """Store a quarantined memory. Returns quarantine_id."""

    @abstractmethod
    async def list_pending(self) -> list[dict]:
        """Return all PENDING quarantine records with their verdicts."""

    @abstractmethod
    async def get(self, quarantine_id: str) -> Optional[dict]:
        """Fetch a specific quarantine record."""

    @abstractmethod
    async def resolve(self, quarantine_id: str, status: QuarantineStatus,
                      merged_content: str = "") -> None:
        """Mark as resolved. Raises QuarantineNotFoundError if not found."""


class IVectorSearch(ABC):
    @abstractmethod
    async def similarity_search(self, query_embedding: list[float],
                                top_k: int = 5,
                                memory_types: list[MemoryType] | None = None) -> list[tuple[MemCube, float]]:
        """
        Return top_k MemCubes most similar to query_embedding.
        Each result is (MemCube, cosine_similarity_score).
        Optional filter by memory_types.
        """


class IFailureLog(ABC):
    @abstractmethod
    async def log(self, action: str, memory_ids: list[str], feedback: str,
                  session_id: str) -> str:
        """Record a failure. Returns failure_log_id."""

    @abstractmethod
    async def get_patterns(self) -> list[dict]:
        """
        Return list of failure patterns:
        [{memory_cluster_ids: [...], failure_count: int, last_failure_at: datetime}]
        """


class IEmbeddingModel(ABC):
    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        """Return 384-dim embedding for text."""

    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Return batch of embeddings. More efficient than calling embed() in a loop."""


class ILLM(ABC):
    @abstractmethod
    async def complete(self, system: str, user: str,
                       max_tokens: int = 1000) -> str:
        """Single-turn completion. Returns assistant message text."""

    @abstractmethod
    async def complete_json(self, system: str, user: str,
                            schema: dict, max_tokens: int = 1000) -> dict:
        """
        Completion that MUST return valid JSON matching schema.
        Raises LLMResponseError if response cannot be parsed as valid JSON.
        """
