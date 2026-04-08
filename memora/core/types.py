"""
core/types.py — Domain primitives. No external dependencies.
Every other module imports FROM here. Nothing imports INTO here.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
from datetime import datetime
import uuid


class MemoryType(str, Enum):
    EPISODIC = "episodic"       # Narrative memories with temporal context
    SEMANTIC = "semantic"       # Distilled facts / KV-style knowledge
    KG_NODE = "kg_node"         # Knowledge graph entity
    KG_EDGE = "kg_edge"         # Knowledge graph relationship


class MemoryTier(str, Enum):
    HOT = "hot"           # KV-cache / in-memory; high access frequency
    WARM = "warm"         # Active pgvector store; regular access
    COLD = "cold"         # Archived; rarely accessed


class QuarantineStatus(str, Enum):
    PENDING = "pending"
    RESOLVED_ACCEPT = "resolved_accept"
    RESOLVED_REJECT = "resolved_reject"
    RESOLVED_MERGE = "resolved_merge"


@dataclass
class Provenance:
    """Tracks origin + version chain of every memory. Inspired by MemOS provenance tagging."""
    origin: str                        # "user_input" | "agent_inference" | "system"
    session_id: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    version: int = 1
    parent_id: Optional[str] = None    # For versioned updates


@dataclass
class MemCube:
    """
    Central memory unit. Inspired by MemOS MemCube.
    Wraps any memory type with metadata for tier routing, TTL, and provenance.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    memory_type: MemoryType = MemoryType.EPISODIC
    tier: MemoryTier = MemoryTier.WARM
    tags: list[str] = field(default_factory=list)
    embedding: Optional[list[float]] = None
    provenance: Optional[Provenance] = None
    access_count: int = 0
    ttl_seconds: Optional[int] = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class Episode:
    """
    A coherent narrative chunk from a conversation.
    Output of Nemori-style episode segmenter.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    start_turn: int = 0
    end_turn: int = 0
    session_id: str = ""
    boundary_score: float = 0.0    # Confidence of the segmentation boundary


@dataclass
class ContradictionVerdict:
    """Output of the Memory Court Judge Agent."""
    incoming_id: str
    conflicting_id: str
    score: float               # 0.0 = no contradiction, 1.0 = direct conflict
    reasoning: str
    is_quarantined: bool
    suggested_resolution: Optional[str] = None
