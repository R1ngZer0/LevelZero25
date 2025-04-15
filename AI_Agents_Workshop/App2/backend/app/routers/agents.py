"""API Endpoints for Agent interactions."""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any # For placeholder response

from app import schemas
from app.agents import router as router_agent # Import the router agent logic

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/invoke", response_model=Any, status_code=status.HTTP_200_OK)
async def invoke_agent(input_data: schemas.RouterInput):
    """Receives a user prompt, routes it, and invokes the appropriate agent.

    Currently returns a placeholder response based on the routed agent.
    """
    try:
        # 1. Route the prompt
        route_result: schemas.RouterOutput = await router_agent.route_prompt(input_data)
        logger.info(f"Prompt routed to: {route_result.agent_type.value}")

        # 2. Invoke the chosen agent (using placeholders for now)
        if route_result.agent_type == schemas.AgentType.CHATBOT:
            # In a real implementation, this would call the Chatbot Agent logic
            # which might involve RAG, history management, and QA loop.
            response = await router_agent.invoke_chatbot(route_result)
        elif route_result.agent_type == schemas.AgentType.DOC_WRITER:
            # In a real implementation, this would call the Doc Writer Agent logic
            # which might involve tool use (outline, section, report) and QA loop.
            response = await router_agent.invoke_doc_writer(route_result)
        else:
            logger.error(f"Unknown agent type determined by router: {route_result.agent_type}")
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail=f"Agent type '{route_result.agent_type}' not implemented."
            )

        # Return the result from the invoked agent (currently placeholder)
        return response

    except HTTPException as http_exc:
        # Re-raise HTTP exceptions directly
        raise http_exc
    except ValueError as val_err:
        # Handle specific value errors (e.g., config issues from llm_clients)
        logger.error(f"Configuration or Value Error during agent invocation: {val_err}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Configuration Error: {val_err}"
        )
    except Exception as e:
        logger.error(f"Unexpected error during agent invocation: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request."
        ) 