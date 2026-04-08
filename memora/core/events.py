"""
core/events.py — Event bus + all typed event dataclasses.

This is the ONLY way modules communicate with each other.
No module should import another module's classes directly for side effects.

Pattern: publish(event) → subscribers are called synchronously (simple hackathon version)
         Upgrade path: swap to asyncio.Queue or Redis pub/sub for production.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Type
from datetime import datetime
from .types import MemCube, ContradictionVerdict, QuarantineStatus


# ─── Event base ────────────────────────────────────────────────────────────────

@dataclass
class BaseEvent:
    timestamp: datetime = field(default_factory=datetime.utcnow)
    session_id: str = ""


# ─── Conversation events ────────────────────────────────────────────────────────

@dataclass
class ConversationTurnEvent(BaseEvent):
    """Agent received a user message. Triggers: scheduler/ingestion_pipeline."""
    user_message: str = ""
    agent_response: str = ""
    turn_number: int = 0


# ─── Scheduler → Court ─────────────────────────────────────────────────────────

@dataclass
class MemoryWriteRequested(BaseEvent):
    """Scheduler produced a new memory candidate. Court must evaluate it first."""
    cube: MemCube = field(default_factory=MemCube)


# ─── Court → Vault ─────────────────────────────────────────────────────────────

@dataclass
class MemoryApproved(BaseEvent):
    """Court cleared the memory. Vault should persist it."""
    cube: MemCube = field(default_factory=MemCube)


@dataclass
class MemoryQuarantined(BaseEvent):
    """Court flagged a contradiction. UI should show resolution card."""
    verdict: ContradictionVerdict = field(default_factory=ContradictionVerdict)
    incoming_cube: MemCube = field(default_factory=MemCube)


# ─── UI → Court → Vault ────────────────────────────────────────────────────────

@dataclass
class ResolutionApplied(BaseEvent):
    """User resolved a quarantine. Vault should finalize storage."""
    quarantine_id: str = ""
    resolution: QuarantineStatus = QuarantineStatus.RESOLVED_ACCEPT
    merged_content: str = ""   # Only populated for RESOLVED_MERGE


# ─── Experience events ─────────────────────────────────────────────────────────

@dataclass
class NegativeOutcomeRecorded(BaseEvent):
    """Agent action got negative feedback. Experience module should log the failure."""
    action_description: str = ""
    memory_cluster_ids: list[str] = field(default_factory=list)
    feedback: str = ""


# ─── Simple synchronous event bus ──────────────────────────────────────────────

class EventBus:
    def __init__(self):
        self._handlers: dict[Type[BaseEvent], list[Callable]] = {}

    def subscribe(self, event_type: Type[BaseEvent], handler: Callable) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def publish(self, event: BaseEvent) -> None:
        for handler in self._handlers.get(type(event), []):
            handler(event)


# Singleton bus — import this everywhere
bus = EventBus()
