"""
core/interfaces.py — Abstract ports (interfaces) for every repository.

Vault, Retrieval, Experience all implement these.
Agent and Scheduler only know these interfaces — not the concrete classes.
Enables: mock in tests, swap implementations without touching callers.
"""
from abc import ABC, abstractmethod
from .types import MemCube, Episode, ContradictionVerdict, QuarantineStatus
from typing import Optional


class IEpisodicRepo(ABC):
    @abstractmethod
    async def save(self, cube: MemCube) -> str: ...
    @abstractmethod
    async def get(self, cube_id: str) -> Optional[MemCube]: ...
    @abstractmethod
    async def delete(self, cube_id: str) -> None: ...


class IKGRepo(ABC):
    @abstractmethod
    async def upsert_node(self, cube: MemCube) -> str: ...
    @abstractmethod
    async def add_edge(self, from_id: str, to_id: str, label: str) -> None: ...
    @abstractmethod
    async def get_neighbors(self, cube_id: str, depth: int = 1) -> list[MemCube]: ...
    @abstractmethod
    async def get_all_nodes(self) -> list[dict]: ...
    @abstractmethod
    async def get_all_edges(self) -> list[dict]: ...


class IQuarantineRepo(ABC):
    @abstractmethod
    async def save_pending(self, cube: MemCube, verdict: ContradictionVerdict) -> str: ...
    @abstractmethod
    async def list_pending(self) -> list[dict]: ...
    @abstractmethod
    async def resolve(self, quarantine_id: str, status: QuarantineStatus) -> None: ...


class IRetriever(ABC):
    @abstractmethod
    async def search(self, query: str, top_k: int = 5) -> list[MemCube]: ...


class IFailureLog(ABC):
    @abstractmethod
    async def log_failure(self, action: str, memory_ids: list[str], feedback: str) -> None: ...
    @abstractmethod
    async def get_failure_patterns(self) -> list[dict]: ...
