"""
CRUD operations for Conversation and ChatMessage models.
"""

from typing import List, Optional
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.chat import Conversation, ChatMessage
from app.schemas.chat_schemas import ConversationCreate, ChatMessageCreate


# --- Conversation CRUD --- 

def create_conversation(db: Session, conversation: ConversationCreate) -> Conversation:
    """Creates a new conversation record in the database."""
    db_conversation = Conversation(**conversation.dict())
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

def get_conversation(db: Session, conversation_id: uuid.UUID) -> Optional[Conversation]:
    """Retrieves a conversation by its ID."""
    return db.query(Conversation).filter(Conversation.id == conversation_id).first()

def list_conversations(db: Session, skip: int = 0, limit: int = 100) -> List[Conversation]:
    """Retrieves a list of conversations, ordered by creation date descending."""
    return db.query(Conversation).order_by(desc(Conversation.created_at)).offset(skip).limit(limit).all()

# Optional: Add delete_conversation, update_conversation etc. here if needed

# --- ChatMessage CRUD --- 

def add_message(db: Session, conversation_id: uuid.UUID, message: ChatMessageCreate) -> ChatMessage:
    """Adds a new chat message linked to a conversation."""
    db_message = ChatMessage(
        **message.dict(), 
        conversation_id=conversation_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages_for_conversation(
    db: Session, 
    conversation_id: uuid.UUID, 
    skip: int = 0, 
    limit: int = 100
) -> List[ChatMessage]:
    """Retrieves messages for a specific conversation, ordered by creation date ascending."""
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.conversation_id == conversation_id)
        .order_by(ChatMessage.created_at.asc()) # Show oldest first
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_recent_messages(
    db: Session, 
    conversation_id: uuid.UUID, 
    limit: int = 10 # Default to match MAX_HISTORY_LENGTH in agent?
) -> List[ChatMessage]:
    """Retrieves the most recent messages for a specific conversation."""
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.conversation_id == conversation_id)
        .order_by(ChatMessage.created_at.desc()) # Get newest first
        .limit(limit)
        .all()[::-1] # Reverse list to return oldest of the limited set first
    ) 