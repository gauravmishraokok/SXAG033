from datetime import datetime
from dataclasses import dataclass
from memora.core.types import MemCube
from memora.core.config import Settings
from memora.retrieval.experience_learner import ExperienceLearner

@dataclass
class RankedMemory:
    cube: MemCube
    final_score: float
    dense_score: float
    symbolic_hit: bool
    failure_penalized: bool
    reasoning: str

class Reranker:
    def __init__(self, failure_reader: ExperienceLearner, settings: Settings):
        self.failure_reader = failure_reader
        self.dense_weight = settings.dense_weight
        self.symbolic_weight = settings.symbolic_weight
        self.failure_penalty = settings.failure_penalty

    async def rerank(self, dense_results: list[tuple[MemCube, float]], symbolic_results: list[MemCube], query: str) -> list[RankedMemory]:
        unique_cubes = {}
        dense_scores = {}
        
        for cube, score in dense_results:
            unique_cubes[cube.id] = cube
            dense_scores[cube.id] = score
            
        symbolic_hits = set()
        for cube in symbolic_results:
            unique_cubes[cube.id] = cube
            symbolic_hits.add(cube.id)
            
        penalized_ids = await self.failure_reader.get_penalized_ids()
        
        ranked = []
        now = datetime.utcnow()
        
        for cube_id, cube in unique_cubes.items():
            dense_score = dense_scores.get(cube_id, 0.0)
            symbolic_hit = cube_id in symbolic_hits
            
            updated_at = cube.provenance.updated_at if cube.provenance else now
            days_since = (now - updated_at).days
            if days_since < 0:
                days_since = 0
            recency_score = 1.0 / (1.0 + days_since)
            
            base_score = (self.dense_weight * dense_score) + (self.symbolic_weight * (1.0 if symbolic_hit else 0.0))
            
            failure_penalized = cube_id in penalized_ids
            failure_multiplier = self.failure_penalty if failure_penalized else 1.0
            
            final_score = base_score * recency_score * failure_multiplier
            reasoning = f"Base: {base_score:.2f} (Dense: {dense_score:.2f}, Sym: {symbolic_hit}), Recency: {recency_score:.2f}, Pen: {failure_multiplier}"
            
            ranked.append(RankedMemory(
                cube=cube,
                final_score=final_score,
                dense_score=dense_score,
                symbolic_hit=symbolic_hit,
                failure_penalized=failure_penalized,
                reasoning=reasoning
            ))
            
        ranked.sort(key=lambda x: x.final_score, reverse=True)
        return ranked
