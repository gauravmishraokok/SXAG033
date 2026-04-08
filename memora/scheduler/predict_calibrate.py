from typing import Optional
from memora.core.interfaces import ILLM
from memora.core.types import Episode, MemCube
from memora.retrieval.hybrid_retriever import IRetriever

class PredictCalibrateLoop:
    def __init__(self, retriever: IRetriever, llm: ILLM):
        self.retriever = retriever
        self.llm = llm

    async def find_gap(self, episode: Episode, existing_memories: list[MemCube]) -> Optional[str]:
        if not existing_memories:
            return episode.content
            
        summaries = "\n".join(f"- {c.content}" for c in existing_memories)
        
        system = (
            "You are analyzing what new information an episode adds to an agent's knowledge base.\n\n"
            f"EXISTING KNOWLEDGE:\n{summaries}\n\n"
            f"NEW EPISODE:\n{episode.content}\n\n"
            "Identify only information in the NEW EPISODE that is NOT already covered by EXISTING KNOWLEDGE.\n"
            "If everything is already known, respond with exactly: \"NO_NEW_INFORMATION\"\n"
            "Otherwise, summarize only the genuinely new information in 1-2 sentences."
        )
        
        try:
            res = await self.llm.complete(system, "")
            res = res.strip()
            if res.upper() == "NO_NEW_INFORMATION":
                return None
                
            return res
        except Exception:
            # Fallback is to assume everything is new
            return episode.content
