from typing import Optional
from memora.core.interfaces import IVectorSearch, IEmbeddingModel
from memora.core.types import MemCube, MemoryType

class DenseRetriever:
    def __init__(self, vector_client: IVectorSearch, embedder: IEmbeddingModel):
        self.vector_client = vector_client
        self.embedder = embedder

    async def search(self, query: str, top_k: int = 5, memory_types: Optional[list[MemoryType]] = None) -> list[tuple[MemCube, float]]:
        embedding = await self.embedder.embed(query)
        results = await self.vector_client.similarity_search(embedding, top_k, memory_types)
        return results
