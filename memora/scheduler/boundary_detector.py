from memora.core.interfaces import IEmbeddingModel
from memora.core.config import Settings

class BoundaryDetector:
    def __init__(self, embedder: IEmbeddingModel, settings: Settings):
        self.embedder = embedder
        self.threshold = settings.boundary_threshold
        self.buffer_size = settings.episode_buffer_size

    async def score(self, turn_a: str, turn_b: str) -> float:
        embeddings = await self.embedder.embed_batch([turn_a, turn_b])
        emb_a, emb_b = embeddings[0], embeddings[1]
        dot = sum(a * b for a, b in zip(emb_a, emb_b))
        norm_a = sum(a * a for a in emb_a) ** 0.5
        norm_b = sum(b * b for b in emb_b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            sim = 0.0
        else:
            sim = dot / (norm_a * norm_b)
        return 1.0 - sim

    async def is_boundary(self, turn_history: list[str], new_turn: str) -> bool:
        if len(turn_history) >= self.buffer_size:
            return True
            
        if not turn_history:
            return False
            
        last_turns = " ".join(turn_history[-3:])
        shift_score = await self.score(last_turns, new_turn)
        
        return shift_score >= self.threshold
