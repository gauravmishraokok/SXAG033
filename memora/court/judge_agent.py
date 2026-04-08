"""
court/judge_agent.py — The Memory Court Judge.

Responsibilities:
- Subscribe to MemoryWriteRequested
- Retrieve top-3 existing memories most similar to the candidate
- Call LLM (Groq) with a two-shot contradiction detection prompt
- Publish MemoryApproved or MemoryQuarantined

Key design: Court NEVER writes to DB. It only emits verdicts via events.
This means Court has zero dependency on vault/ or storage/.
Court only depends on: core/, llm/, retrieval/ (read-only).

Contradiction threshold: configurable in config.py (default: 0.75)
"""
from memora.core.events import bus, MemoryWriteRequested, MemoryApproved, MemoryQuarantined
from memora.core.types import ContradictionVerdict
from memora.core.config import Settings
from memora.llm.groq_client import GroqClient
from memora.llm.prompts.judge_prompts import JUDGE_SYSTEM_PROMPT
from memora.retrieval.hybrid_retriever import HybridRetriever
from .contradiction_detector import ContradictionDetector


class JudgeAgent:
    def __init__(
        self,
        llm: GroqClient,
        retriever: HybridRetriever,
        detector: ContradictionDetector,
        settings: Settings,
    ):
        self.llm = llm
        self.retriever = retriever
        self.detector = detector
        self.threshold = settings.contradiction_threshold
        bus.subscribe(MemoryWriteRequested, self._on_write_requested)

    async def _on_write_requested(self, event: MemoryWriteRequested) -> None:
        """
        1. Retrieve top-3 existing memories similar to candidate
        2. Run LLM contradiction check
        3. Publish approved or quarantined
        """
        ...
