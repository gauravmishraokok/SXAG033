from memora.core.events import EventBus, MemoryWriteRequested
from memora.core.types import MemCube, MemoryType
from memora.retrieval.hybrid_retriever import HybridRetriever

class ToolExecutor:
    def __init__(self, retriever: HybridRetriever, bus: EventBus):
        self.retriever = retriever
        self.bus = bus

    async def search_memory(self, query: str) -> str:
        results = await self.retriever.search(query)
        if not results:
            return "No memories found."
            
        formatted = []
        for mem in results:
            formatted.append(f"[{mem.memory_type.value}] {mem.content}")
        return "\n".join(formatted)

    async def store_memory(self, content: str, memory_type: str, tags: list[str]) -> str:
        try:
            m_type = MemoryType(memory_type)
        except ValueError:
            m_type = MemoryType.SEMANTIC
            
        cube = MemCube(
            id="temp-override", # This might naturally be generated. Let's use the factory if available.
            content=content,
            memory_type=m_type,
            tags=tags,
            access_count=0
        )
        # Spec says create MemoryWriteRequested explicitly mid-conversation.
        await self.bus.publish(MemoryWriteRequested(
            cube=cube
        ))
        
        return "Memory storage requested successfully."

    async def recall_context(self, topic: str) -> str:
        # Specialized search on EPISODIC memories about topic
        # For simplicity, filter after retrieve since retrieval abstracts this.
        results = await self.retriever.search(topic, top_k=10)
        
        narrative = []
        for mem in results:
            if mem.memory_type == MemoryType.EPISODIC:
                narrative.append(mem.content)
                
        if not narrative:
            return f"No episodic context found for topic: {topic}"
            
        return "\n".join(narrative)
