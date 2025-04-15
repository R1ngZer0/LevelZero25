"""
API Router for Chatbot interactions (DB-backed).
"""

from fastapi import APIRouter, HTTPException, Body, Depends
from typing import List
# Removed unused Depends from sqlalchemy.orm import Session
# Removed unused app.db.session import get_db 

from app.schemas.chat_schemas import (
    UserMessageInput, 
    AssistantMessageOutput, 
    ConversationOutput, # Use new output schema for listing
    ConversationDetailOutput # Use new output schema for getting details
)
# Import the refactored agent functions
from app.agents.chatbot_agent import (
    generate_chat_response, 
    get_conversation, 
    list_all_conversations
)

router = APIRouter()

# Renamed chat_id to conversation_id for clarity
@router.post("/chats/{conversation_id}/messages", response_model=AssistantMessageOutput)
def send_message(
    conversation_id: str, # Keep as string, agent handles UUID conversion/creation
    user_message: UserMessageInput = Body(...),
    # db: Session = Depends(get_db) # No longer needed if agent uses get_db()
):
    """Receives a user message, generates a response, and adds both to the DB history."""
    try:
        # Agent function now handles getting/creating conversation and adding messages
        assistant_response = generate_chat_response(
            conversation_id_str=conversation_id, 
            user_prompt=user_message.content,
            mode=user_message.mode
        )
        return assistant_response
    except Exception as e:
        print(f"Error processing chat message for {conversation_id}: {e}")
        # Consider more specific error handling based on agent exceptions
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

# Use the new ConversationOutput schema
@router.get("/chats", response_model=List[ConversationOutput])
def list_conversations_endpoint():
    """Lists all conversations stored in the database."""
    try:
        # Call the refactored agent function that uses the DB
        return list_all_conversations()
    except Exception as e:
        print(f"Error listing conversations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Use the new ConversationDetailOutput schema
@router.get("/chats/{conversation_id}", response_model=ConversationDetailOutput)
def get_conversation_endpoint(conversation_id: str):
    """Retrieves the full message history for a given conversation ID."""
    try:
        # Call the refactored agent function that uses the DB
        conversation_details = get_conversation(conversation_id)
        # Optional: Check if messages list is empty and conversation_id is not a valid UUID 
        # (indicating agent couldn't find/create) and raise 404? 
        # For now, let agent return empty structure for invalid ID.
        # if not conversation_details.messages and not conversation_details.created_at:
        #     raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation_details
    except Exception as e:
        print(f"Error retrieving conversation history for {conversation_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Note on starting chats remains the same: 
# Frontend generates UUID, calls POST /chats/{new_uuid}/messages.
# The agent's generate_chat_response handles creation via get_or_create_conversation_db. 