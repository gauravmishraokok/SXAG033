from dataclasses import dataclass
from typing import Optional
from memora.core.interfaces import ILLM
from memora.core.types import Episode, MemoryType
from memora.llm.prompts.segmenter_prompts import CLASSIFIER_SYSTEM_PROMPT
import logging

logger = logging.getLogger(__name__)

@dataclass
class ClassificationResult:
    memory_type: MemoryType
    content: str
    tags: list[str]
    key: Optional[str] = None

class TypeClassifier:
    def __init__(self, llm: ILLM):
        self.llm = llm

    async def classify(self, episode: Episode) -> list[ClassificationResult]:
        try:
            res = await self.llm.complete_json(
                system=CLASSIFIER_SYSTEM_PROMPT,
                user=episode.content,
                schema={"memories": list}
            )
            
            results = []
            for mem in res.get("memories", []):
                mtype = MemoryType.EPISODIC if mem.get("type") == "episodic" else MemoryType.SEMANTIC
                results.append(ClassificationResult(
                    memory_type=mtype,
                    content=mem.get("content", ""),
                    tags=mem.get("tags", []),
                    key=mem.get("key")
                ))
            
            if not any(r.memory_type == MemoryType.EPISODIC for r in results):
                results.append(ClassificationResult(
                    memory_type=MemoryType.EPISODIC,
                    content=episode.content,
                    tags=[]
                ))
                
            return results
        except Exception as e:
            logger.warning(f"TypeClassification failed: {e}")
            return [ClassificationResult(
                memory_type=MemoryType.EPISODIC,
                content=episode.content,
                tags=[]
            )]
