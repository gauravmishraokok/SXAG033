from dataclasses import dataclass
from typing import Optional
from memora.core.interfaces import IKGRepo
from memora.retrieval.symbolic_retriever import SymbolicRetriever

@dataclass
class ExpandedQuery:
    original: str
    expanded_tags: list[str]
    related_cube_ids: list[str]

class QueryExpander:
    def __init__(self, kg_repo: IKGRepo, symbolic_retriever: SymbolicRetriever):
        self.kg_repo = kg_repo
        self.symbolic_retriever = symbolic_retriever

    async def expand(self, query: str, seed_tags: Optional[list[str]] = None) -> ExpandedQuery:
        if seed_tags is not None:
            tags_to_search = seed_tags
        else:
            stopwords = {"the", "a", "an", "is", "are", "what", "how", "why"}
            tags_to_search = [word.lower() for word in query.replace("?", "").replace(",", "").split() if word.lower() not in stopwords]
            
        if not tags_to_search:
            return ExpandedQuery(original=query, expanded_tags=[], related_cube_ids=[])
            
        memories = await self.symbolic_retriever.search_by_tags(tags_to_search, top_k=20)
        
        expanded_tags = set(tags_to_search)
        related_cube_ids = []
        for mem in memories:
            related_cube_ids.append(mem.id)
            for tag in mem.tags:
                expanded_tags.add(tag)
                
        return ExpandedQuery(
            original=query,
            expanded_tags=list(expanded_tags),
            related_cube_ids=related_cube_ids
        )
