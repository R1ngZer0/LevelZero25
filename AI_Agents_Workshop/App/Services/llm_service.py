"""
LLM service for the OT Interview Application.

This file provides functions to interact with different LLM providers,
handle API calls, and process responses.
"""

import logging
import os
from typing import Optional
import requests
import json

from AI_Agents_Workshop.App.Config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def get_llm_response(prompt: str, temperature: float = 0.7, max_tokens: int = 1500) -> str:
    """
    Gets a response from the configured LLM provider.
    
    Args:
        prompt: The text prompt to send to the LLM
        temperature: Controls randomness (0 to 1, lower is more deterministic)
        max_tokens: Maximum tokens to generate in the response
        
    Returns:
        The text response from the LLM
    """
    provider = settings.llm_provider.lower()
    
    if provider == "openai":
        return _get_openai_response(prompt, temperature, max_tokens)
    elif provider == "local":
        return _get_local_llm_response(prompt, temperature, max_tokens)
    else:
        logger.error(f"Unsupported LLM provider: {provider}")
        return "Error: Unsupported LLM provider."


def _get_openai_response(prompt: str, temperature: float = 0.7, max_tokens: int = 1500) -> str:
    """
    Gets a response from the OpenAI API.
    
    Args:
        prompt: The text prompt to send
        temperature: Controls randomness
        max_tokens: Maximum tokens in the response
        
    Returns:
        The text response from OpenAI
    """
    api_key = settings.llm_api_key
    
    if not api_key:
        logger.error("OpenAI API key not found")
        return "Error: OpenAI API key not configured."
    
    model_name = settings.llm_model_name or "gpt-4"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )
        
        response.raise_for_status()
        result = response.json()
        
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"].strip()
        else:
            logger.error(f"Unexpected response format: {result}")
            return "Error: Unexpected response format from OpenAI."
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making request to OpenAI: {str(e)}")
        return f"Error: Failed to get response from OpenAI: {str(e)}"


def _get_local_llm_response(prompt: str, temperature: float = 0.7, max_tokens: int = 1500) -> str:
    """
    Gets a response from a locally hosted LLM service.
    
    Args:
        prompt: The text prompt to send
        temperature: Controls randomness
        max_tokens: Maximum tokens in the response
        
    Returns:
        The text response from the local LLM
    """
    # This implementation depends on the specific local LLM being used
    # Below is a placeholder for a generic API call
    
    local_api_url = os.getenv("LOCAL_LLM_API_URL", "http://localhost:8080/v1/completions")
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(
            local_api_url,
            headers=headers,
            data=json.dumps(payload)
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Adapt this to match your local LLM's response format
        if "text" in result:
            return result["text"].strip()
        else:
            logger.error(f"Unexpected response format: {result}")
            return "Error: Unexpected response format from local LLM."
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making request to local LLM: {str(e)}")
        return f"Error: Failed to get response from local LLM: {str(e)}" 