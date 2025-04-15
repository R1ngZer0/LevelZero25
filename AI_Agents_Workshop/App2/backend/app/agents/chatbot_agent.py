"""
Implements the Chatbot Agent logic, including history management (DB-backed), 
RAG, LLM interaction, and QA loop.
"""

from sqlalchemy.orm import Session
import uuid

from app.schemas.chat_schemas import (
    ChatMessageBase, 
    ConversationDetailOutput, 
    AssistantMessageOutput,
    ChatMessageCreate, # Import DB related schemas
    ConversationCreate,
    ConversationOutput
)
from app.schemas.qa_schemas import QAInput
from app.agents.qa_agent import review_content
from app.llm_clients import get_llm_client
from app.services.vector_store import find_similar_embeddings
from app.db.session import get_db # Use get_db for session management
from app.crud import crud_chat # Import the new CRUD module
from pydantic_ai import Agent
from typing import Dict, List

# Remove in-memory storage
# chat_histories: Dict[str, ChatHistory] = {}

MAX_REVISIONS = 3
# MAX_HISTORY_LENGTH = 10 # Now handled by crud_chat.get_recent_messages limit

# --- History Management (DB Based) --- 

def get_conversation_details(conversation_id: uuid.UUID, db: Session) -> ConversationDetailOutput:
    """Retrieves full conversation details including messages from DB."""
    db_convo = crud_chat.get_conversation(db, conversation_id)
    if not db_convo:
        # Or raise HTTPException? Depends on router handling
        return ConversationDetailOutput(id=conversation_id, created_at=None, messages=[]) 
    db_messages = crud_chat.get_messages_for_conversation(db, conversation_id, limit=200) # Get all messages (or limit)
    return ConversationDetailOutput.from_orm(db_convo) # Pydantic v2 from_orm

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
    return [ConversationOutput.from_orm(convo) for convo in db_convos]

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
    mode: str = "cloud"
) -> AssistantMessageOutput:
    """Generates the chatbot response using DB history, RAG, and QA loop."""
    
    with get_db() as db:
        # 1. Ensure conversation exists, get its UUID
        conversation_id = get_or_create_conversation_db(conversation_id_str, db)

        # 2. Add user message to DB history
        add_message_to_db(conversation_id, "user", user_prompt, db)
        
        # 3. Get history & RAG context from DB
        history = get_recent_history_formatted_db(conversation_id, db)
        rag_context = retrieve_rag_context(user_prompt, history, db) 

        llm_client = get_llm_client(mode)
        
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
        
        chat_llm = Agent(
            llm=llm_client,
            system_prompt=system_prompt,
            output_model=str
        )

        current_response_content = ""
        feedback = None
        
        # 4. QA Loop (largely unchanged, uses generate response)
        for attempt in range(MAX_REVISIONS + 1):
            print(f"Chatbot attempt {attempt + 1} for chat {conversation_id}")
            prompt_for_llm = full_prompt
            if feedback:
                prompt_for_llm += f"\n\n## Previous Attempt Feedback (Please Address):\n{feedback}"
            
            try:
                current_response_content = chat_llm.invoke(prompt_for_llm)
            except Exception as e:
                print(f"Error during LLM generation (attempt {attempt + 1}): {e}")
                current_response_content = f"Error generating response: {e}"
                break 

            qa_input = QAInput(content_to_review=current_response_content, original_prompt=user_prompt, context=rag_context)
            qa_result = review_content(qa_input, mode=mode)
            
            if qa_result.is_approved:
                print(f"QA approved response on attempt {attempt + 1}")
                feedback = None 
                break 
            else:
                feedback = qa_result.feedback
                print(f"QA requires revision (attempt {attempt + 1}): {feedback}")
                if attempt == MAX_REVISIONS:
                    print(f"Max revisions reached for chat {conversation_id}. Using last response despite feedback.")
                    break
                    
        # 5. Add final assistant message to DB history
        final_response_content = current_response_content 
        add_message_to_db(conversation_id, "assistant", final_response_content, db)
        
        # 6. Return final response
        return AssistantMessageOutput(content=final_response_content)

# --- Functions called by Router (Using DB) ---

def list_all_conversations() -> List[ConversationOutput]:
    """Returns a list of all conversations."""
    with get_db() as db:
        return list_all_conversations_db(db)

def get_conversation(conversation_id_str: str) -> ConversationDetailOutput:
    """Retrieves the full message history for a given conversation ID."""
    try:
        conversation_id = uuid.UUID(conversation_id_str)
        with get_db() as db:
            return get_conversation_details(conversation_id, db)
    except ValueError:
        # Handle invalid UUID - maybe return empty history or raise 404 in router
        return ConversationDetailOutput(id=conversation_id_str, created_at=None, messages=[]) 