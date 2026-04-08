from dataclasses import dataclass

@dataclass
class ActiveSession:
    session_id: str
    last_retrieved_ids: list[str]
    last_action: str

class OutcomeTracker:
    def __init__(self):
        self._active_sessions: dict[str, ActiveSession] = {}

    def record_retrieval(self, session_id: str, cube_ids: list[str], action: str) -> None:
        self._active_sessions[session_id] = ActiveSession(
            session_id=session_id,
            last_retrieved_ids=cube_ids,
            last_action=action
        )

    def get_active_cluster(self, session_id: str) -> tuple[list[str], str]:
        session = self._active_sessions.get(session_id)
        if not session:
            return ([], "")
        return (session.last_retrieved_ids, session.last_action)
