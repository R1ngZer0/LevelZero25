"""
Defines the Pydantic models for Chatbot interactions, including messages and history.
"""
from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from datetime import datetime
import uuid

# --- Base Schemas --- 
class ChatMessageBase(BaseModel):
    """Base schema for a single message."""
    role: Literal["user", "assistant"] = Field(..., description="The role of the sender (user or assistant).")
    content: str = Field(..., description="The text content of the message.")

class ConversationBase(BaseModel):
    """Base schema for a conversation (e.g., for creation)."""
    # Optional: Add title if you add it to the model
    # title: Optional[str] = Field(None, description="Optional title for the conversation.")
    pass # No fields needed for creation if ID/time are defaults

# --- Schemas for API Input --- 
class UserMessageInput(BaseModel):
    """Input schema for receiving a user message."""
    content: str = Field(..., description="The text content of the user's message.")

# --- Schemas for Database Interaction (used by CRUD) ---
class ChatMessageCreate(ChatMessageBase):
    """Schema for creating a message in the DB (needs conversation_id)."""
    pass # Role and content come from ChatMessageBase

class ChatMessageInDB(ChatMessageBase):
    """Schema representing a message retrieved from the DB."""
    id: int
    conversation_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True # Allow mapping from SQLAlchemy models

class ConversationCreate(ConversationBase):
    """Schema for creating a conversation in the DB."""
    pass # Nothing needed beyond base if only defaults are used

class ConversationInDBBase(ConversationBase):
    """Base schema representing a conversation retrieved from the DB."""
    id: uuid.UUID
    created_at: datetime
    # title: Optional[str] # Include if added to model

    class Config:
        from_attributes = True

# --- Schemas for API Output --- 
class AssistantMessageOutput(BaseModel):
    """Output schema for sending an assistant message."""
    role: Literal["assistant"] = "assistant"
    content: str = Field(..., description="The text content of the assistant's response.")

class ChatMessageOutput(ChatMessageInDB):
    """Output schema for a single message (includes DB fields)."""
    pass # Inherits all from ChatMessageInDB

class ConversationOutput(ConversationInDBBase):
    """Output schema for a conversation listing (basic info)."""
    pass # Inherits ID and created_at from ConversationInDBBase

class ConversationDetailOutput(ConversationInDBBase):
    """Output schema for retrieving a single conversation with messages."""
    messages: List[ChatMessageOutput] = []

# --- Legacy ChatHistory (Kept for potential compatibility, but DB is preferred) ---
# class ChatHistory(BaseModel):
#     """Represents the history of a single chat conversation (legacy in-memory style)."""
#     chat_id: str = Field(..., description="Unique identifier for the chat session.") # Keep as string for now?
#     messages: List[ChatMessageBase] = Field(default_factory=list, description="A list of messages exchanged in the conversation.") 