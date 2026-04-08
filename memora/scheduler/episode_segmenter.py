import uuid
from typing import Optional
from memora.core.types import Episode
from memora.scheduler.boundary_detector import BoundaryDetector

class EpisodeSegmenter:
    def __init__(self, detector: BoundaryDetector):
        self.detector = detector
        self._buffer: list[str] = []
        self._turn_index: int = 0
        self._episode_start: int = 0

    async def process_turn(self, turn: str, session_id: str) -> Optional[Episode]:
        self._turn_index += 1
        
        if not self._buffer:
            self._buffer.append(turn)
            return None
            
        shift_score = await self.detector.score(" ".join(self._buffer[-3:]), turn)
        is_bound = await self.detector.is_boundary(self._buffer, turn)
        
        if not is_bound:
            self._buffer.append(turn)
            return None
            
        episode = Episode(
            id=str(uuid.uuid4()),
            content=" ".join(self._buffer),
            start_turn=self._episode_start,
            end_turn=self._turn_index - 2, 
            session_id=session_id,
            boundary_score=shift_score
        )
        
        self._buffer = [turn]
        self._episode_start = self._turn_index - 1
        
        return episode

    async def flush(self, session_id: str) -> Optional[Episode]:
        if not self._buffer:
            return None
            
        episode = Episode(
            id=str(uuid.uuid4()),
            content=" ".join(self._buffer),
            start_turn=self._episode_start,
            end_turn=self._turn_index - 1,
            session_id=session_id,
            boundary_score=1.0 
        )
        
        self._buffer.clear()
        
        return episode
