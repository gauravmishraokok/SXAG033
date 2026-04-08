"""
core/config.py — All configuration from environment variables.
Single source of truth. Import Settings from here everywhere.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # LLM
    anthropic_api_key: str = ""
    openai_api_key: str = ""

    # Databases
    database_url: str = "postgresql+asyncpg://memora:memora@localhost:5432/memora"
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "memorapass"
    redis_url: str = "redis://localhost:6379"

    # Memory Court
    contradiction_threshold: float = 0.75

    # Retrieval
    top_k_retrieval: int = 5
    context_window_budget: int = 8000

    # Embedding
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_dim: int = 384

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
