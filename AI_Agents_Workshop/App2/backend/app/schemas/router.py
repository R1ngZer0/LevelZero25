"""Pydantic schemas for the Router Agent."""

from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class AgentType(str, Enum):
    """Enum for the types of agents the router can delegate to."""
    CHATBOT = "chatbot"
    DOC_WRITER = "doc_writer"
    # Add other agent types if needed

class RouterInput(BaseModel):
    """Input schema for the router agent."""
    prompt: str = Field(..., description="The user's input prompt.")
    conversation_id: Optional[str] = Field(None, description="Optional ID for existing conversation context.")

class RouterOutput(BaseModel):
    """Output schema indicating the determined agent type and original prompt."""
    agent_type: AgentType = Field(..., description="The agent determined to handle the prompt.")
    original_prompt: str = Field(..., description="The original prompt received by the router.")
    # Include conversation_id if needed by downstream agents
    conversation_id: Optional[str] = Field(None, description="Optional ID for existing conversation context.")

# Internal model used by the router LLM call
class RouteDecision(BaseModel):
    """Internal Pydantic model for the LLM to decide the route."""
    agent: AgentType = Field(..., description="The agent best suited to handle the user's prompt (chatbot or doc_writer).")
    reasoning: str = Field(..., description="A brief explanation for why this agent was chosen.") 