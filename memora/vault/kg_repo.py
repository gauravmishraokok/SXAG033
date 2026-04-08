"""KGRepo implements IKGRepo wrapper.

Delegates to Neo4jClient or NetworkXClient based on configuration.
"""

from typing import List, Dict, Optional
from ...core.interfaces import IKGRepo
from ...core.types import MemCube
from ...core.config import get_settings
from ..storage.graph.neo4j_client import Neo4jClient
from ..storage.graph.networkx_client import NetworkXClient


class KGRepo(IKGRepo):
    """Knowledge graph repository wrapper that delegates to appropriate client."""
    
    def __init__(self):
        settings = get_settings()
        if settings.use_networkx_fallback:
            self._client = NetworkXClient()
        else:
            self._client = Neo4jClient(
                uri=settings.neo4j_uri,
                user=settings.neo4j_user,
                password=settings.neo4j_password
            )
    
    async def upsert_node(self, cube: MemCube) -> str:
        """Insert or update a KG node. Returns node ID."""
        return await self._client.upsert_node(cube)
    
    async def add_edge(self, from_id: str, to_id: str, label: str,
                       metadata: Optional[Dict] = None) -> str:
        """Add a directed edge. Returns edge ID. Old edges are archived, not deleted."""
        return await self._client.add_edge(from_id, to_id, label, metadata)
    
    async def deprecate_edge(self, edge_id: str, reason: str) -> None:
        """Mark edge as deprecated with a reason and deprecated_at timestamp."""
        await self._client.deprecate_edge(edge_id, reason)
    
    async def get_neighbors(self, cube_id: str, depth: int = 1) -> List[MemCube]:
        """Return all nodes reachable within `depth` hops. Active edges only."""
        return await self._client.get_neighbors(cube_id, depth)
    
    async def get_all_nodes(self) -> List[Dict]:
        """For graph visualization. Returns list of {id, label, type, tier}."""
        return await self._client.get_all_nodes()
    
    async def get_all_edges(self) -> List[Dict]:
        """For graph visualization. Returns list of {id, from, to, label, active, deprecated_at}."""
        return await self._client.get_all_edges()
    
    async def close(self):
        """Close underlying connections."""
        if hasattr(self._client, 'close'):
            await self._client.close()