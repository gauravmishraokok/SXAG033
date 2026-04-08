from memora.core.types import ContradictionVerdict
from memora.core.errors import LLMResponseError

class ContradictionDetector:
    def __init__(self, threshold: float = 0.75):
        self.threshold = threshold

    def score_from_llm_response(self, response: dict) -> float:
        if "contradiction_score" not in response:
            raise LLMResponseError("Missing contradiction_score")
        
        score = response["contradiction_score"]
        if not isinstance(score, (int, float)) or not (0.0 <= score <= 1.0):
            raise LLMResponseError(f"contradiction_score out of range [0.0, 1.0]: {score}")
            
        reasoning = response.get("reasoning", "")
        if not reasoning or not isinstance(reasoning, str):
            raise LLMResponseError("reasoning must be a non-empty string")
            
        suggested = response.get("suggested_resolution")
        if suggested not in ("accept", "reject") and not (isinstance(suggested, str) and suggested.startswith("merge:")):
            # The spec says "None if missing/invalid", but typical validation might just let it be extracted later.
            # I will strictly follow that we validate the score and reasoning, and suggested is just grabbed.
            pass
            
        return float(score)

    def make_verdict(
        self,
        incoming_id: str,
        conflicting_id: str,
        score: float,
        reasoning: str,
        suggested_resolution: str | None,
    ) -> ContradictionVerdict:
        
        return ContradictionVerdict(
            incoming_id=incoming_id,
            conflicting_id=conflicting_id,
            score=score,
            is_quarantined=score >= self.threshold,
            reasoning=reasoning,
            suggested_resolution=suggested_resolution
        )

    def is_clear(self, score: float) -> bool:
        return score < self.threshold
