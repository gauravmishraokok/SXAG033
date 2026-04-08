from dataclasses import dataclass
from datetime import datetime
from memora.core.types import MemCube
from memora.core.interfaces import IQuarantineRepo

@dataclass
class QuarantineQueueItem:
    quarantine_id: str
    incoming_cube: MemCube
    conflicting_cube_id: str
    contradiction_score: float
    reasoning: str
    suggested_resolution: str | None
    created_at: datetime

class QuarantineManager:
    def __init__(self, repo: IQuarantineRepo):
        self.repo = repo

    async def get_queue(self) -> list[QuarantineQueueItem]:
        pending_records = await self.repo.list_pending()
        
        queue = []
        for r in pending_records:
            queue.append(QuarantineQueueItem(
                quarantine_id=r.id,
                incoming_cube=r.incoming_cube,
                conflicting_cube_id=r.conflicting_cube_id,
                contradiction_score=r.contradiction_score,
                reasoning=r.reasoning,
                suggested_resolution=r.suggested_resolution,
                created_at=r.created_at
            ))
            
        return queue

    async def get_health(self) -> dict:
        return {
            "pending_count": await self.repo.count_pending(),
            "resolved_today": await self.repo.count_resolved_today(),
            "total_quarantined_all_time": await self.repo.count_total_quarantined(),
            "average_contradiction_score": await self.repo.get_average_score()
        }
