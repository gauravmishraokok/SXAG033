"""Storage module components.

Provides PostgreSQL, vector, and graph storage implementations.

Imports are lazy to avoid requiring optional heavy dependencies (sentence-transformers,
neo4j client) just by importing the storage package. Use explicit imports in app wiring.
"""

# Only expose the DB model base and ORM aliases at package level (no heavy deps)
from .postgres.models import (
    Base,
    MemCubeORM,
    EpisodeORM,
    ContradictionORM,
    QuarantineLogORM,
)

__all__ = [
    "Base",
    "MemCubeORM",
    "EpisodeORM",
    "ContradictionORM",
    "QuarantineLogORM",
]