"""
core/types.py — Domain primitives. No external dependencies.
Every other module imports FROM here. Nothing imports INTO here.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
from datetime import datetime, timezone
import uuid
from .errors import MemoraError, EmbeddingDimensionError


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
    origin: str                        # "user_input" | "agent_inference" | "system" | "resolution"
    session_id: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    version: int = 1
    parent_id: Optional[str] = None    # For versioned updates

    @classmethod
    def new(cls, origin: str, session_id: str) -> "Provenance":
        """Create a new provenance record."""
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        return cls(origin=origin, session_id=session_id, created_at=now, updated_at=now, version=1, parent_id=None)


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

    def __post_init__(self) -> None:
        """Validate MemCube fields."""
        if not self.content:
            raise MemoraError("MemCube content cannot be empty")
        
        if self.embedding is not None and len(self.embedding) != 384:
            raise EmbeddingDimensionError(384, len(self.embedding))
        
        if self.access_count < 0:
            raise MemoraError("access_count must be >= 0")

    def bump_access(self) -> "MemCube":
        """Return new MemCube with access_count incremented and updated_at refreshed."""
        # Create new provenance with updated timestamp
        new_provenance = None
        if self.provenance:
            # Ensure timestamp difference by using microseconds from provenance
            import time
            base_time = datetime.now(timezone.utc).replace(tzinfo=None)
            # Add small increment to ensure different timestamp
            new_time = base_time.replace(microsecond=(base_time.microsecond + 1) % 1000000)
            
            new_provenance = Provenance(
                origin=self.provenance.origin,
                session_id=self.provenance.session_id,
                created_at=self.provenance.created_at,
                updated_at=new_time,
                version=self.provenance.version,
                parent_id=self.provenance.parent_id
            )
        
        updated_cube = MemCube(
            id=self.id,
            content=self.content,
            memory_type=self.memory_type,
            tier=self.tier,
            tags=self.tags.copy(),
            embedding=self.embedding.copy() if self.embedding else None,
            provenance=new_provenance,
            access_count=self.access_count + 1,
            ttl_seconds=self.ttl_seconds,
            extra=self.extra.copy()
        )
        
        return updated_cube

    def with_embedding(self, embedding: list[float]) -> "MemCube":
        """Return new MemCube with embedding set. Validates length == 384."""
        if len(embedding) != 384:
            raise EmbeddingDimensionError(384, len(embedding))
        
        return MemCube(
            id=self.id,
            content=self.content,
            memory_type=self.memory_type,
            tier=self.tier,
            tags=self.tags.copy(),
            embedding=embedding.copy(),
            provenance=self.provenance,
            access_count=self.access_count,
            ttl_seconds=self.ttl_seconds,
            extra=self.extra.copy()
        )
    
    def with_extra(self, extra: dict[str, Any]) -> "MemCube":
        """Return new MemCube with extra field set."""
        return MemCube(
            id=self.id,
            content=self.content,
            memory_type=self.memory_type,
            tier=self.tier,
            tags=self.tags.copy(),
            embedding=self.embedding.copy() if self.embedding else None,
            provenance=self.provenance,
            access_count=self.access_count,
            ttl_seconds=self.ttl_seconds,
            extra=extra.copy()
        )

    def to_dict(self) -> dict:
        """Serialize to plain dict (for JSON serialization). Converts enums to .value."""
        from dataclasses import asdict
        result = {
            "id": self.id,
            "content": self.content,
            "memory_type": self.memory_type.value,
            "tier": self.tier.value,
            "tags": self.tags,
            "embedding": self.embedding,
            "provenance": asdict(self.provenance) if self.provenance else None,
            "access_count": self.access_count,
            "ttl_seconds": self.ttl_seconds,
            "extra": self.extra
        }
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "MemCube":
        """Deserialize from plain dict. Converts string values back to enums."""
        # Convert enum strings back to enums
        memory_type = MemoryType(data["memory_type"])
        tier = MemoryTier(data["tier"])
        
        # Reconstruct provenance if present
        provenance = None
        if data["provenance"]:
            prov_data = data["provenance"]
            provenance = Provenance(
                origin=prov_data["origin"],
                session_id=prov_data["session_id"],
                created_at=datetime.fromisoformat(prov_data["created_at"]),
                updated_at=datetime.fromisoformat(prov_data["updated_at"]),
                version=prov_data["version"],
                parent_id=prov_data["parent_id"]
            )
        
        return cls(
            id=data["id"],
            content=data["content"],
            memory_type=memory_type,
            tier=tier,
            tags=data["tags"],
            embedding=data["embedding"],
            provenance=provenance,
            access_count=data["access_count"],
            ttl_seconds=data["ttl_seconds"],
            extra=data["extra"]
        )


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

    def __post_init__(self) -> None:
        """Validate episode fields."""
        if not self.content:
            raise MemoraError("Episode content cannot be empty")
        
        if self.end_turn < self.start_turn:
            raise MemoraError("end_turn must be >= start_turn")
        
        if not (0.0 <= self.boundary_score <= 1.0):
            raise MemoraError("boundary_score must be in [0.0, 1.0]")


@dataclass
class ContradictionVerdict:
    """Output of the Memory Court Judge Agent."""
    incoming_id: str
    conflicting_id: str
    score: float               # 0.0 = no contradiction, 1.0 = direct conflict
    reasoning: str
    is_quarantined: bool
    suggested_resolution: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate verdict fields."""
        if not (0.0 <= self.score <= 1.0):
            raise MemoraError("score must be in [0.0, 1.0]")
        
        if not self.reasoning:
            raise MemoraError("reasoning cannot be empty")
        
        if self.suggested_resolution is not None:
            if self.suggested_resolution not in {"accept", "reject", "merge"} and not self.suggested_resolution.startswith("merge:"):
                raise MemoraError("suggested_resolution must be 'accept', 'reject', or 'merge:<content>'")


# Validation helpers

def validate_mem_cube(cube: MemCube) -> None:
    """Raise ValueError with descriptive message for any invalid MemCube field."""
    try:
        # Re-use of post_init validation logic
        cube.__post_init__()
    except ValueError as e:
        raise ValueError(f"Invalid MemCube: {e}")


def validate_episode(episode: Episode) -> None:
    """Raise ValueError for any invalid Episode field."""
    try:
        # Re-use of post_init validation logic
        episode.__post_init__()
    except ValueError as e:
        raise ValueError(f"Invalid Episode: {e}")
