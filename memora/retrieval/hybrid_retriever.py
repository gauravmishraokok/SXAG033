from memora.core.types import MemCube
from memora.core.config import Settings
from memora.retrieval.dense_retriever import DenseRetriever
from memora.retrieval.symbolic_retriever import SymbolicRetriever
from memora.retrieval.query_expander import QueryExpander
from memora.retrieval.reranker import Reranker

class IRetriever:
    async def search(self, query: str, top_k: int = 5) -> list[MemCube]:
        pass

class HybridRetriever(IRetriever):
    def __init__(
        self,
        dense: DenseRetriever,
        symbolic: SymbolicRetriever,
        expander: QueryExpander,
        reranker: Reranker,
        settings: Settings,
    ):
        self.dense = dense
        self.symbolic = symbolic
        self.expander = expander
        self.reranker = reranker
        self.settings = settings

    async def search(self, query: str, top_k: int = 5) -> list[MemCube]:
        expanded = await self.expander.expand(query)
        dense_results = await self.dense.search(query, top_k=top_k * 2)
        symbolic_results = await self.symbolic.search_by_tags(expanded.expanded_tags, top_k=top_k * 2)
        
        ranked = await self.reranker.rerank(dense_results, symbolic_results, query)
        
        return [r.cube for r in ranked[:top_k]]
