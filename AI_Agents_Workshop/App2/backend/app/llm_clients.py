"""Provides functions to get configured Pydantic AI LLM and Embedding clients."""

import logging
from functools import lru_cache

from pydantic_ai.langchain import LLM, Embedding
from pydantic_ai.langchain.openai import OpenAI, OpenAIEmbeddings
from pydantic_ai.langchain.ollama import Ollama, OllamaEmbeddings

from backend.app.config import get_settings, Settings

logger = logging.getLogger(__name__)

@lru_cache()
def get_llm_client() -> LLM:
    """Returns a configured Pydantic AI LLM client based on settings."""
    settings = get_settings()
    logger.info(f"Creating LLM client for APP_MODE: {settings.APP_MODE}")

    if settings.APP_MODE == "CLOUD":
        if not settings.OPENAI_API_KEY:
            logger.error("OPENAI_API_KEY not set for CLOUD mode.")
            raise ValueError("OpenAI API key is required for CLOUD mode.")
        logger.info(f"Using OpenAI LLM: {settings.OPENAI_LLM_MODEL}")
        return OpenAI(api_key=settings.OPENAI_API_KEY, model=settings.OPENAI_LLM_MODEL)

    elif settings.APP_MODE == "LOCAL":
        logger.info(f"Using Ollama LLM: {settings.OLLAMA_LLM_MODEL} at {settings.OLLAMA_BASE_URL}")
        # Add error handling for Ollama connection if needed
        return Ollama(model=settings.OLLAMA_LLM_MODEL, base_url=settings.OLLAMA_BASE_URL)

    else:
        logger.error(f"Unsupported APP_MODE: {settings.APP_MODE}")
        raise ValueError(f"Unsupported APP_MODE: {settings.APP_MODE}")

@lru_cache()
def get_embedding_client() -> Embedding:
    """Returns a configured Pydantic AI Embedding client based on settings."""
    settings = get_settings()
    logger.info(f"Creating Embedding client for APP_MODE: {settings.APP_MODE}")

    if settings.APP_MODE == "CLOUD":
        if not settings.OPENAI_API_KEY:
            logger.error("OPENAI_API_KEY not set for CLOUD mode.")
            raise ValueError("OpenAI API key is required for CLOUD mode.")
        logger.info(f"Using OpenAI Embedding: {settings.OPENAI_EMBEDDING_MODEL}")
        return OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY, model=settings.OPENAI_EMBEDDING_MODEL)

    elif settings.APP_MODE == "LOCAL":
        logger.info(f"Using Ollama Embedding: {settings.OLLAMA_EMBEDDING_MODEL} at {settings.OLLAMA_BASE_URL}")
        # Add error handling for Ollama connection if needed
        return OllamaEmbeddings(model=settings.OLLAMA_EMBEDDING_MODEL, base_url=settings.OLLAMA_BASE_URL)

    else:
        logger.error(f"Unsupported APP_MODE: {settings.APP_MODE}")
        raise ValueError(f"Unsupported APP_MODE: {settings.APP_MODE}")

# Example Usage:
# from backend.app.llm_clients import get_llm_client, get_embedding_client
# llm = get_llm_client()
# embedder = get_embedding_client() 