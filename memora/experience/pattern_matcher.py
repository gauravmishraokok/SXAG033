from datetime import datetime
from dataclasses import dataclass
from memora.core.interfaces import IFailureLog
from memora.core.config import Settings

@dataclass
class FailureMatch:
    cube_id: str
    failure_count: int
    last_failure_at: datetime
    penalty_multiplier: float

class PatternMatcher:
    def __init__(self, failure_log: IFailureLog, settings: Settings):
        self.failure_log = failure_log
        self.settings = settings

    async def find_overlapping_failures(self, candidate_ids: list[str]) -> list[FailureMatch]:
        patterns = await self.failure_log.get_patterns()
        
        matches = []
        for pattern in patterns:
            if pattern["cube_id"] in candidate_ids:
                matches.append(FailureMatch(
                    cube_id=pattern["cube_id"],
                    failure_count=pattern["failure_count"],
                    last_failure_at=pattern["last_failure_at"],
                    penalty_multiplier=self.settings.failure_penalty if pattern["failure_count"] >= 2 else 1.0
                ))
                
        return matches
