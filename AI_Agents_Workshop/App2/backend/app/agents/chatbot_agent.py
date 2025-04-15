"""
Implements the Chatbot Agent logic, including history management (DB-backed), 
RAG, LLM interaction, and QA loop.
"""

from sqlalchemy.orm import Session
import uuid
from fastapi import HTTPException
import logging

# --- Setup Logger --- 
logger = logging.getLogger(__name__)
# -------------------

from app.schemas.chat_schemas import (
    ChatMessageBase, 
    ConversationDetailOutput, 
    AssistantMessageOutput,
    ChatMessageCreate, # Import DB related schemas
    ConversationCreate,
    ConversationOutput,
    ChatMessageOutput
)
from app.schemas.qa_schemas import QAInput
from app.agents.qa_agent import review_content
from app.llm_clients import get_llm_client
from app.services.vector_store import find_similar_embeddings
from app.db.session import get_db # Use get_db for session management
from app.crud import crud_chat # Import the new CRUD module
from pydantic_ai import Agent
from typing import Dict, List
from pydantic import BaseModel, Field

# Define a Pydantic model for the LLM's expected chat response
class ChatResponseModel(BaseModel):
    """Structure for the LLM's chat response."""
    response_text: str = Field(..., description="The generated chat response text from the AI assistant.")

# Remove in-memory storage
# chat_histories: Dict[str, ChatHistory] = {}

MAX_REVISIONS = 3
# MAX_HISTORY_LENGTH = 10 # Now handled by crud_chat.get_recent_messages limit

# --- History Management (DB Based) --- 

def get_conversation_details(conversation_id: uuid.UUID, db: Session) -> ConversationDetailOutput:
    """Retrieves full conversation details including messages from DB."""
    db_convo = crud_chat.get_conversation(db, conversation_id)
    if not db_convo:
        # Raise HTTPException here, as the calling agent function expects a valid object or an exception
        # The router's exception handling should catch this.
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    # db_messages = crud_chat.get_messages_for_conversation(db, conversation_id, limit=200) # REDUNDANT - messages are loaded by get_conversation
    
    # Manual serialization instead of from_orm
    message_outputs = []
    if db_convo.messages: # Check relationship was loaded
        for msg in db_convo.messages:
            message_outputs.append(ChatMessageOutput(
                id=msg.id,
                conversation_id=msg.conversation_id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at
            ))

    return ConversationDetailOutput(
        id=db_convo.id,
        created_at=db_convo.created_at,
        messages=message_outputs
        # title=db_convo.title # Include if title is added to model/schema
    )
    # return ConversationDetailOutput.from_orm(db_convo) # Bypass potentially problematic from_orm

def add_message_to_db(conversation_id: uuid.UUID, role: str, content: str, db: Session):
    """Adds a new message to the database for the specified conversation."""
    message_data = ChatMessageCreate(role=role, content=content)
    crud_chat.add_message(db, conversation_id=conversation_id, message=message_data)

def get_recent_history_formatted_db(conversation_id: uuid.UUID, db: Session, limit: int = 10) -> List[Dict[str, str]]:
    """Gets the recent chat history from DB, formatted for LLM prompts."""
    db_messages = crud_chat.get_recent_messages(db, conversation_id=conversation_id, limit=limit)
    formatted_history = [
        {"role": msg.role, "content": msg.content} 
        for msg in db_messages
    ]
    return formatted_history

def list_all_conversations_db(db: Session) -> List[ConversationOutput]:
    """Returns a list of all conversations from the DB."""
    db_convos = crud_chat.list_conversations(db, limit=1000) # Add reasonable limit
    
    # Manual serialization instead of from_orm list comprehension
    output_list = []
    for convo in db_convos:
        output_list.append(ConversationOutput(
            id=convo.id,
            created_at=convo.created_at
            # title=convo.title # Include if title is added to model/schema
        ))
    return output_list
    # return [ConversationOutput.from_orm(convo) for convo in db_convos] # Bypass potentially problematic from_orm

def get_or_create_conversation_db(conversation_id_str: str, db: Session) -> uuid.UUID:
    """Tries to get a conversation by UUID str, creates if not found/invalid."""
    try:
        conversation_id = uuid.UUID(conversation_id_str)
        db_convo = crud_chat.get_conversation(db, conversation_id)
        if not db_convo:
             # If UUID was valid but not found, create it
             print(f"Conversation ID {conversation_id} not found, creating new one.")
             db_convo = crud_chat.create_conversation(db, conversation=ConversationCreate())
             conversation_id = db_convo.id # Get the actual generated ID
        # else: conversation exists, use the provided valid ID
        return conversation_id
    except ValueError:
        # Invalid UUID string provided, create a new conversation
        print(f"Invalid UUID string {conversation_id_str}, creating new conversation.")
        db_convo = crud_chat.create_conversation(db, conversation=ConversationCreate())
        return db_convo.id


# --- RAG Logic (Unchanged, but uses DB session now if needed) --- 
def retrieve_rag_context(query: str, history: List[Dict[str, str]], db: Session) -> str:
    """Retrieves relevant context from the vector store."""
    search_query = query
    context_str = "No relevant context found in knowledge base."
    try:
        # Assuming find_similar_embeddings handles its own DB session or accepts one
        # If find_similar_embeddings needs a session, pass `db`
        similar_embeddings = find_similar_embeddings(db=db, query_text=search_query, limit=3)
        if similar_embeddings:
            context_str = f"Found {len(similar_embeddings)} potentially relevant snippets in the knowledge base."
        else:
            context_str = "No relevant context found in knowledge base for the query."
    except Exception as e:
        print(f"Error during RAG context retrieval: {e}")
    return context_str

# --- Core Chat Logic & QA Loop (Adapted for DB) ---
def generate_chat_response(
    conversation_id_str: str, 
    user_prompt: str, 
    # mode: str = "cloud" # Removed mode parameter
) -> AssistantMessageOutput:
    """Generates the chatbot response using DB history, RAG, and QA loop."""
    
    # with get_db() as db: # Incorrect usage
    db_gen = get_db()
    db = next(db_gen)
    try:
        # 1. Ensure conversation exists, get its UUID
        conversation_id = get_or_create_conversation_db(conversation_id_str, db)

        # 2. Add user message to DB history
        add_message_to_db(conversation_id, "user", user_prompt, db)
        
        # 3. Get history & RAG context from DB
        history = get_recent_history_formatted_db(conversation_id, db)
        rag_context = retrieve_rag_context(user_prompt, history, db) 

        # llm_client = get_llm_client(mode) # Incorrect call signature
        llm_client = get_llm_client() # Correct: Client determines mode internally
        
        formatted_history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
        system_prompt = (
            "You are a helpful assistant. Use the provided conversation history and knowledge base context to answer the user's query. "
            "If the context is relevant, integrate it into your response. If not, answer based on the history and general knowledge."
        )
        full_prompt = (
            f"## Conversation History:\n{formatted_history_str}\n\n" 
            f"## Knowledge Base Context:\n{rag_context}\n\n"
            f"## User Query:\n{user_prompt}"
        )
        
        # --- LLM Agent Setup --- 
        logger.debug("Setting up main Chat LLM Agent...")
        try:
            chat_llm = Agent(
                llm=llm_client,
                system_prompt=system_prompt,
                output_model=ChatResponseModel 
            )
        except Exception as e:
            logger.error(f"Error setting up Chat LLM Agent: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to initialize chat agent")
        logger.debug("Chat LLM Agent setup complete.")

        current_response_content = ""
        feedback = None
        final_response_content = "Error: Could not generate response."
        
        # 4. QA Loop (largely unchanged, uses generate response)
        for attempt in range(MAX_REVISIONS + 1):
            logger.debug(f"Chatbot attempt {attempt + 1} for chat {conversation_id}")
            prompt_for_llm = full_prompt
            if feedback:
                prompt_for_llm += f"\n\n## Previous Attempt Feedback (Please Address):\n{feedback}"
            
            # --- LLM Invoke --- 
            logger.debug(f"Invoking Chat LLM (Attempt {attempt + 1})...")
            try:
                llm_result: ChatResponseModel = chat_llm.invoke(prompt_for_llm)
                current_response_content = llm_result.response_text 
                logger.debug(f"Chat LLM raw response (Attempt {attempt + 1}): {current_response_content[:100]}...")
            except Exception as e:
                logger.error(f"Error during LLM generation (attempt {attempt + 1}): {e}", exc_info=True)
                # Save the error as the content? Or just use default error?
                final_response_content = f"Error generating response internally (attempt {attempt+1})."
                # Break QA loop on LLM error
                break 

            # --- QA Invoke --- 
            logger.debug(f"Invoking QA Agent (Attempt {attempt + 1})...")
            try:
                qa_input = QAInput(content_to_review=current_response_content, original_prompt=user_prompt, context=rag_context)
                qa_result = review_content(qa_input) # Call simplified function
                logger.debug(f"QA Result (Attempt {attempt + 1}): Approved={qa_result.is_approved}, Feedback='{qa_result.feedback[:100]}...'")
            except Exception as e:
                 logger.error(f"Error during QA review (attempt {attempt + 1}): {e}", exc_info=True)
                 # If QA fails, maybe use the last LLM response directly?
                 final_response_content = current_response_content # Use pre-QA content
                 feedback = None # Ensure we don't loop again with QA error feedback
                 break # Exit QA loop on QA error
            
            if qa_result.is_approved:
                logger.debug(f"QA approved response on attempt {attempt + 1}")
                final_response_content = current_response_content # Store approved content
                feedback = None 
                break # Exit loop on approval
            else:
                feedback = qa_result.feedback
                logger.debug(f"QA requires revision (attempt {attempt + 1}): {feedback}")
                if attempt == MAX_REVISIONS:
                    logger.warning(f"Max revisions reached for chat {conversation_id}. Using last response despite feedback.")
                    final_response_content = current_response_content # Use last generated content
                    break # Exit loop after max revisions
                    
        # 5. Add final assistant message to DB history
        # final_response_content = current_response_content # Moved logic into loop
        logger.debug(f"Adding final assistant message to DB: {final_response_content[:100]}...")
        add_message_to_db(conversation_id, "assistant", final_response_content, db)
        logger.debug("Assistant message added to DB.")
        
        # 6. Return final response
        return AssistantMessageOutput(content=final_response_content)
        
    finally:
        try:
            next(db_gen, None) # Consume generator to close session
        except StopIteration:
            pass # Generator already exhausted

# --- Functions called by Router (Using DB) ---

def list_all_conversations() -> List[ConversationOutput]:
    """Returns a list of all conversations."""
    db_gen = get_db()
    db = next(db_gen)
    try:
        return list_all_conversations_db(db)
    finally:
        try:
            next(db_gen, None) # Consume generator to close session
        except StopIteration:
            pass # Generator already exhausted

def get_conversation(conversation_id_str: str) -> ConversationDetailOutput:
    """Retrieves the full message history for a given conversation ID."""
    try:
        conversation_id = uuid.UUID(conversation_id_str)
        db_gen = get_db()
        db = next(db_gen)
        try:
             return get_conversation_details(conversation_id, db)
        finally:
             try:
                 next(db_gen, None) # Consume generator to close session
             except StopIteration:
                 pass # Generator already exhausted
    except ValueError:
        # Handle invalid UUID - return empty history
        # Ensure the ID field matches the expected type (UUID or str based on schema)
        # ConversationDetailOutput expects uuid.UUID for id. If we can't parse,
        # maybe it's better to let the router handle a 404 based on the agent raising?
        # For now, returning default is safer than crashing.
        # However, the Pydantic model expects a UUID. Let's return None or raise?
        # Raising here would be caught by the router's generic exception handler.
        # Let's stick to returning default for now, but this might hide issues.
        # Returning an object that doesn't match the schema严格ly can cause issues.
        # Revisit: Can we make ID Optional[uuid.UUID] in the schema?
        # For now, let's return the *string* ID if UUID parsing failed.
        # But ConversationDetailOutput needs a UUID... This is tricky.
        # Safest bet: Re-raise the ValueError and let the router return 400/404/500.
        print(f"Invalid UUID format provided: {conversation_id_str}")
        raise ValueError(f"Invalid conversation ID format: {conversation_id_str}") 
        # return ConversationDetailOutput(id=None, created_at=None, messages=[]) # Placeholder if ID were optional 