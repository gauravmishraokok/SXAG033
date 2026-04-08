import json
from uuid import uuid4
from datetime import datetime
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from memora.core.interfaces import IFailureLog
from memora.core.events import EventBus, NegativeOutcomeRecorded

class FailureLogger(IFailureLog):
    def __init__(self, session_factory: Callable[[], AsyncSession], bus: EventBus):
        self.session_factory = session_factory
        bus.subscribe(NegativeOutcomeRecorded, self.handle)

    async def handle(self, event: NegativeOutcomeRecorded) -> None:
        await self.log(
            action=event.action_description,
            memory_ids=event.memory_cluster_ids,
            feedback=event.feedback,
            session_id=event.session_id
        )

    async def log(self, action: str, memory_ids: list[str], feedback: str, session_id: str) -> str:
        failure_log_id = str(uuid4())
        
        query = text("""
            INSERT INTO failure_log (id, session_id, action_description, memory_cluster_ids, feedback, created_at)
            VALUES (:id, :session_id, :action, :memory_ids::jsonb, :feedback, NOW())
        """)
        
        async with self.session_factory() as db_session:
            await db_session.execute(query, {
                "id": failure_log_id,
                "session_id": session_id,
                "action": action,
                "memory_ids": json.dumps(memory_ids),
                "feedback": feedback
            })
            await db_session.commit()
            
        return failure_log_id

    async def get_patterns(self) -> list[dict]:
        query = text("""
            SELECT
                jsonb_array_elements_text(memory_cluster_ids) AS cube_id,
                COUNT(*) AS failure_count,
                MAX(created_at) AS last_failure_at
            FROM failure_log
            GROUP BY cube_id
            HAVING COUNT(*) >= 1
            ORDER BY failure_count DESC
        """)
        
        async with self.session_factory() as db_session:
            result = await db_session.execute(query)
            rows = result.fetchall()
            
        patterns = []
        for row in rows:
            patterns.append({
                "cube_id": row.cube_id,
                "failure_count": row.failure_count,
                "last_failure_at": row.last_failure_at
            })
            
        return patterns
