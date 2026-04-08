from datetime import datetime, timezone
from dataclasses import dataclass
from memora.core.types import MemCube
from memora.core.config import Settings

@dataclass
class ContextSlot:
    cube: MemCube
    token_count: int
    priority: float
    injected_at: datetime

class ContextPager:
    def __init__(self, settings: Settings):
        self.budget = settings.context_window_budget
        self._active: list[ContextSlot] = []

    def _priority(self, cube: MemCube, rerank_score: float) -> float:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        updated_at = cube.provenance.updated_at if cube.provenance else now
        days_since = max(0, (now - updated_at).days)
        recency = 1.0 / (1.0 + days_since)
        return 0.6 * rerank_score + 0.4 * recency

    async def build_context(self, retrieved: list[MemCube], current_tokens_used: int) -> list[MemCube]:
        available_budget = self.budget - current_tokens_used
        
        for i, cube in enumerate(retrieved):
            token_count = max(1, len(cube.content) // 4)
            # using mock rerank score scaling down based on index
            mock_score = 1.0 / (1.0 + i) 
            priority = self._priority(cube, mock_score)
            
            # Check if already active
            if not any(slot.cube.id == cube.id for slot in self._active):
                self._active.append(ContextSlot(
                    cube=cube,
                    token_count=token_count,
                    priority=priority,
                    injected_at=datetime.now(timezone.utc).replace(tzinfo=None)
                ))
        
        self._active.sort(key=lambda x: x.priority, reverse=True)
        
        while sum(slot.token_count for slot in self._active) > available_budget and self._active:
            # Evict lowest priority
            self._active.pop()
            
        return [slot.cube for slot in self._active]

    async def evict_all(self) -> None:
        self._active.clear()
