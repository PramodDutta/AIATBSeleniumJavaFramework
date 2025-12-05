"""Configuration settings for AI Test Analysis Pipeline."""

import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    LOGS_PATH: Path = Path(__file__).parent.parent.parent / "target" / "analytics-logs" / "test-events.jsonl"
    
    # Qdrant Settings
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "test_failures"
    
    # Embedding Model
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Analysis Settings
    SIMILARITY_THRESHOLD: float = 0.3
    TOP_K_RESULTS: int = 5
    
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

