"""SQLAlchemy ORM models for PostgreSQL.

Exactly 4 tables as per spec: mem_cubes, quarantine_records, failure_log, timeline_events.
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Float, DateTime, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

# pgvector is only available when the Postgres extension is installed.
# In test environments without a real DB, fall back to JSON for the column type.
try:
    from pgvector.sqlalchemy import Vector as VECTOR
    _VECTOR_COLUMN = VECTOR(384)
except ImportError:
    VECTOR = JSON  # type: ignore[assignment,misc]
    _VECTOR_COLUMN = JSON  # type: ignore[assignment,misc]

Base = declarative_base()


class MemCubeRow(Base):
    """ORM model for mem_cubes table."""
    __tablename__ = "mem_cubes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    memory_type = Column(String(20), nullable=False)  # MemoryType enum value
    tier = Column(String(10), nullable=False)         # MemoryTier enum value
    tags = Column(JSON, nullable=False, default=list)  # list[str]
    embedding = Column(_VECTOR_COLUMN)                    # pgvector column
    provenance = Column(JSON, nullable=False)          # Serialized Provenance
    access_count = Column(Integer, nullable=False, default=0)
    ttl_seconds = Column(Integer)                      # None or int
    extra = Column(JSON, nullable=False, default=dict)  # dict[str, Any]
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class QuarantineRow(Base):
    """ORM model for quarantine_records table."""
    __tablename__ = "quarantine_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incoming_cube_id = Column(UUID(as_uuid=True), nullable=False)
    conflicting_id = Column(UUID(as_uuid=True), nullable=False)
    contradiction_score = Column(Float, nullable=False)
    reasoning = Column(Text, nullable=False)
    suggested_resolution = Column(Text)  # None or string
    status = Column(String(30), nullable=False, default='pending')  # QuarantineStatus enum value
    merged_content = Column(Text)  # Only for RESOLVED_MERGE
    incoming_cube_json = Column(JSON, nullable=False)  # Full MemCube serialized
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    resolved_at = Column(DateTime)  # None until resolved


class FailureLogRow(Base):
    """ORM model for failure_log table."""
    __tablename__ = "failure_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), nullable=False)
    action_description = Column(Text, nullable=False)
    memory_cluster_ids = Column(JSON, nullable=False)  # list of cube IDs
    feedback = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class TimelineEventRow(Base):
    """ORM model for timeline_events table."""
    __tablename__ = "timeline_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cube_id = Column(UUID(as_uuid=True))  # Can be None for system events
    event_type = Column(String(30), nullable=False)  # "created"|"updated"|"quarantined"|"resolved"|"evicted"
    description = Column(Text)  # Optional description
    session_id = Column(UUID(as_uuid=True))  # Optional session context
    event_metadata = Column(JSON, nullable=False, default=dict)  # Event-specific metadata (renamed from 'metadata' — reserved by SQLAlchemy)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


# ── Aliases used by vault repos and storage/__init__.py ─────────────────────
MemCubeORM = MemCubeRow
QuarantineORM = QuarantineRow
FailureLogORM = FailureLogRow
TimelineEventORM = TimelineEventRow
# EpisodeORM: MemCubes filtered by memory_type == EPISODIC (alias at ORM level)
EpisodeORM = MemCubeRow
# Legacy aliases for storage/__init__.py compatibility
ContradictionORM = QuarantineRow
QuarantineLogORM = QuarantineRow
Contradict = QuarantineRow