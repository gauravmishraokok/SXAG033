import uuid
from datetime import datetime, timezone
from dataclasses import dataclass

@dataclass
class SessionState:
    session_id: str
    turn_count: int
    created_at: datetime
    last_active_at: datetime
    context_token_count: int

class SessionManager:
    def __init__(self):
        self._sessions: dict[str, SessionState] = {}

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        self._sessions[session_id] = SessionState(
            session_id=session_id,
            turn_count=0,
            created_at=now,
            last_active_at=now,
            context_token_count=0
        )
        return session_id

    def get(self, session_id: str) -> SessionState:
        if session_id not in self._sessions:
            raise ValueError(f"Session {session_id} not found")
        return self._sessions[session_id]

    def ensure_session(self, session_id: str) -> None:
        """Register session_id if missing (e.g. client restored from localStorage after restart)."""
        if session_id in self._sessions:
            return
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        self._sessions[session_id] = SessionState(
            session_id=session_id,
            turn_count=0,
            created_at=now,
            last_active_at=now,
            context_token_count=0,
        )

    def increment_turn(self, session_id: str) -> int:
        session = self.get(session_id)
        session.turn_count += 1
        session.last_active_at = datetime.now(timezone.utc).replace(tzinfo=None)
        return session.turn_count

    def update_token_count(self, session_id: str, count: int) -> None:
        session = self.get(session_id)
        session.context_token_count = count
