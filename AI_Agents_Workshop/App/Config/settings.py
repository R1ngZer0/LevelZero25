"""
Application settings and configuration management.

This file defines application settings and provides a function to access them.
Settings can be loaded from environment variables or default values.
"""

import os
from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    Application settings, configured from environment variables.
    """
    # Application info
    app_name: str = "OT Interview Analysis System"
    app_version: str = "0.1.0"
    
    # Database
    database_url: str = Field(
        default="sqlite:///./ot_interviews.db",
        env="DATABASE_URL"
    )
    
    # API settings
    api_prefix: str = "/api"
    
    # Security
    secret_key: str = Field(
        default="devkey_replace_in_production", 
        env="SECRET_KEY"
    )
    access_token_expire_minutes: int = 60 * 24  # 1 day
    
    # LLM settings
    llm_provider: str = Field(default="openai", env="LLM_PROVIDER")
    llm_api_key: str = Field(default="", env="LLM_API_KEY")
    llm_model_name: str = Field(default="gpt-4", env="LLM_MODEL_NAME")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Returns the application settings, cached for efficiency.
    """
    return Settings() 