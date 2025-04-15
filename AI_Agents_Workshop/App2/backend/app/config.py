"""Application configuration using Pydantic Settings."""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    """Defines application settings loaded from environment variables."""
    # General
    # APP_MODE: str = "CLOUD" # No longer needed, only CLOUD supported
    KNOWLEDGE_BASE_PATH: str = "./knowledgebase"

    # Database
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "ai_agent_db"
    DATABASE_URL: Optional[str] = None

    # OpenAI (Cloud Mode)
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_LLM_MODEL: str = "gpt-4.1"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    # Ollama settings removed
    # OLLAMA_BASE_URL: str = "http://localhost:11434"
    # OLLAMA_LLM_MODEL: str = "llama3.1:8b"
    # OLLAMA_EMBEDDING_MODEL: str = "nomic-embed-text"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra='ignore' # Ignore extra fields from .env
    )

    def __init__(self, **values):
        super().__init__(**values)
        # Construct DATABASE_URL after loading other variables
        self.DATABASE_URL = (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

@lru_cache()
def get_settings() -> Settings:
    """Returns the cached Settings instance."""
    return Settings()

# Example usage:
# from app.config import get_settings
# settings = get_settings()
# print(settings.DATABASE_URL) 