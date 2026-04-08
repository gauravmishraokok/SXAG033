content = """
import pytest
from memora.core.config import Settings
@pytest.fixture
def settings():
    return Settings(
        database_url="postgresql+asyncpg://memora:memora@localhost:5432/memora_test",
        contradiction_threshold=0.75,
        top_k_retrieval=3,
        context_window_budget=2000,
        embedding_dim=384,
        use_networkx_fallback=True,
        anthropic_api_key="test-key",
    )
"""
with open('d:\\solarisx\\tests\\conftest.py', 'a') as f:
    f.write(content)
