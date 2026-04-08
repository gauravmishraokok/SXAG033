"""Domain exceptions for MEMORA.

All domain exceptions. Using typed exceptions (not generic `ValueError` or `RuntimeError`)
makes error handling explicit, testable, and readable.
"""


class MemoraError(Exception):
    """Base class for all MEMORA exceptions."""


# Memory operations
class MemoryNotFoundError(MemoraError):
    """Raised when a MemCube ID does not exist in any repository."""
    def __init__(self, cube_id: str):
        super().__init__(f"Memory not found: {cube_id}")
        self.cube_id = cube_id


class MemoryValidationError(MemoraError):
    """Raised when a MemCube fails validation (empty content, bad embedding dim, etc.)."""
    pass


class DuplicateMemoryError(MemoraError):
    """Raised on attempt to insert a MemCube with an ID that already exists."""
    def __init__(self, cube_id: str):
        super().__init__(f"Memory already exists: {cube_id}")
        self.cube_id = cube_id


# Quarantine operations
class QuarantineNotFoundError(MemoraError):
    """Raised when a quarantine_id does not exist."""
    def __init__(self, quarantine_id: str):
        super().__init__(f"Quarantine record not found: {quarantine_id}")
        self.quarantine_id = quarantine_id


class AlreadyResolvedError(MemoraError):
    """Raised on attempt to resolve an already-resolved quarantine record."""
    pass


# LLM errors
class LLMResponseError(MemoraError):
    """Raised when LLM returns unparseable or invalid response."""
    def __init__(self, message: str, raw_response: str = ""):
        super().__init__(message)
        self.raw_response = raw_response


class LLMRateLimitError(MemoraError):
    """Raised on 429 from LLM provider. Caller should retry with backoff."""
    pass


# Storage errors
class StorageConnectionError(MemoraError):
    """Raised when DB connection cannot be established."""
    pass


class EmbeddingDimensionError(MemoraError):
    """Raised when embedding vector has wrong dimension."""
    def __init__(self, expected: int, got: int):
        super().__init__(f"Embedding dimension mismatch: expected {expected}, got {got}")
        self.expected = expected
        self.got = got


# Court errors
class ContradictionDetectionError(MemoraError):
    """Raised when contradiction detection pipeline fails (not the same as finding a contradiction)."""
    pass