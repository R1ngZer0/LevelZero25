"""Provides functions to get configured Pydantic AI LLM and Embedding clients.
   Supports only OpenAI (CLOUD mode).
"""

import logging
from functools import lru_cache
from typing import Union
import os

# Imports:
from pydantic_ai.models.openai import OpenAIModel
# Import the provider
from pydantic_ai.providers.openai import OpenAIProvider
# from pydantic_ai.models.ollama import OllamaModel # Removed Ollama import

# Use langchain_community for embeddings
from langchain_community.embeddings import OpenAIEmbeddings # Only OpenAI needed
# from langchain_community.embeddings import OllamaEmbeddings # Removed Ollama import

# Corrected config import
from app.config import get_settings, Settings

logger = logging.getLogger(__name__)

# Define specific return types using Union
LlmClientType = OpenAIModel # Only OpenAI supported
EmbeddingClientType = OpenAIEmbeddings # Only OpenAI supported

@lru_cache()
def get_llm_client() -> LlmClientType:
    """Returns a configured Pydantic AI OpenAI LLM client."""
    settings = get_settings()
    logger.info(f"Creating OpenAI LLM client") # Simplified log

    # Always use CLOUD settings now
    if not settings.OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY not set.")
        raise ValueError("OpenAI API key is required.")
    logger.info(f"Using PydanticAI OpenAI LLM: {settings.OPENAI_LLM_MODEL}")
    # Explicitly pass the key loaded from settings (from .env)
    # return OpenAIModel(settings.OPENAI_LLM_MODEL, api_key=settings.OPENAI_API_KEY)

    # Use the provider to pass the API key
    provider = OpenAIProvider(api_key=settings.OPENAI_API_KEY)
    return OpenAIModel(settings.OPENAI_LLM_MODEL, provider=provider)

@lru_cache()
def get_embedding_client() -> EmbeddingClientType:
    """Returns a configured Langchain OpenAI Embedding client."""
    settings = get_settings()
    logger.info(f"Creating OpenAI Embedding client") # Simplified log

    # # --- DEBUG: Print the key from the environment --- 
    # env_api_key = os.environ.get('OPENAI_API_KEY')
    # logger.info(f"DEBUG: Value of os.environ.get('OPENAI_API_KEY') is: {env_api_key}") 
    # # -----------------------------------------------

    # Always use CLOUD settings now
    if not settings.OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY not set.")
        raise ValueError("OpenAI API key is required.")
    logger.info(f"Using Langchain OpenAI Embedding: {settings.OPENAI_EMBEDDING_MODEL}")
    # Explicitly pass the key loaded from settings (from .env)
    return OpenAIEmbeddings(model=settings.OPENAI_EMBEDDING_MODEL, openai_api_key=settings.OPENAI_API_KEY)

# Example Usage:
# from app.llm_clients import get_llm_client, get_embedding_client
# llm = get_llm_client()
# embedder = get_embedding_client() 