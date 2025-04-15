"""Service for processing uploaded files: text extraction and chunking."""

import os
from typing import List, Optional, Generator
import logging

# Import necessary libraries for file types
import docx # python-docx
from pypdf import PdfReader

from app import schemas
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# --- Text Extraction --- 

def extract_text_from_txt(file_path: str) -> str:
    """Extracts text content from a plain text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading text file {file_path}: {e}", exc_info=True)
        raise ValueError(f"Could not read text file: {e}")

def extract_text_from_docx(file_path: str) -> str:
    """Extracts text content from a DOCX file."""
    try:
        doc = docx.Document(file_path)
        full_text = [para.text for para in doc.paragraphs]
        return '\n'.join(full_text)
    except Exception as e:
        logger.error(f"Error reading docx file {file_path}: {e}", exc_info=True)
        raise ValueError(f"Could not read docx file: {e}")

def extract_text_from_pdf(file_path: str) -> str:
    """Extracts text content from a PDF file."""
    try:
        reader = PdfReader(file_path)
        full_text = []
        for page in reader.pages:
            full_text.append(page.extract_text() or "") # Handle cases where extraction might return None
        return "\n".join(full_text)
    except Exception as e:
        logger.error(f"Error reading pdf file {file_path}: {e}", exc_info=True)
        raise ValueError(f"Could not read pdf file: {e}")

def extract_text(file_path: str, media_type: Optional[str]) -> str:
    """Extracts text from a file based on its path or media type."""
    logger.info(f"Attempting to extract text from {file_path} (media_type: {media_type})")
    _, extension = os.path.splitext(file_path)
    effective_media_type = media_type or ""

    try:
        if extension.lower() == ".txt" or "text/plain" in effective_media_type:
            return extract_text_from_txt(file_path)
        elif extension.lower() == ".docx" or "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in effective_media_type:
            return extract_text_from_docx(file_path)
        elif extension.lower() == ".pdf" or "application/pdf" in effective_media_type:
            return extract_text_from_pdf(file_path)
        else:
            logger.warning(f"Unsupported file type/extension: {extension} / {media_type}")
            raise ValueError(f"Unsupported file type: {extension or media_type}")
    except ValueError as ve:
        # Re-raise ValueErrors (like unsupported type or read errors) directly
        raise ve
    except Exception as e:
        # Catch any other unexpected errors during extraction
        logger.error(f"Unexpected error extracting text from {file_path}: {e}", exc_info=True)
        raise ValueError(f"Unexpected error during text extraction: {e}")

# --- Chunking --- 

# TODO: Implement chunking strategies (e.g., fixed size, recursive character)
# Consider using libraries like langchain.text_splitter or similar logic.

def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 100) -> List[str]:
    """Placeholder for text chunking logic."""
    logger.info(f"Chunking text (length: {len(text)}), chunk_size={chunk_size}, overlap={chunk_overlap}")
    # Simple placeholder: split by paragraphs or fixed length
    # In a real app, use a more robust method like RecursiveCharacterTextSplitter
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
        if start < 0: # Avoid issues if overlap > size
             start = end
    logger.info(f"Generated {len(chunks)} chunks.")
    return chunks

# --- Full Processing Pipeline --- 

def process_file_and_vectorize(db_file_id: int, db_session): # Needs DB session
    """Orchestrates the file processing and vectorization.
       Placeholder - to be implemented, likely triggered by upload endpoint.
    """
    from app import crud
    from app.services import vector_store

    db_file = crud.file.get_file(db_session, db_file_id)
    if not db_file:
        logger.error(f"File with ID {db_file_id} not found for processing.")
        return

    full_path = os.path.join(settings.KNOWLEDGE_BASE_PATH, db_file.relative_path)
    logger.info(f"Starting processing for file: {full_path} (ID: {db_file.id})")

    try:
        # 1. Update status to processing
        crud.file.update_file(db_session, db_file, schemas.file.FileUpdate(is_processing=True))

        # 2. Extract Text
        text_content = extract_text(full_path, db_file.media_type)
        logger.info(f"Extracted text content (length: {len(text_content)}) for file ID: {db_file.id}")

        # 3. Chunk Text
        # TODO: Make chunk size/overlap configurable?
        text_chunks = chunk_text(text_content)

        # 4. Generate & Store Embeddings for each chunk
        embedding_model = settings.OLLAMA_EMBEDDING_MODEL if settings.APP_MODE == "LOCAL" else settings.OPENAI_EMBEDDING_MODEL
        for chunk in text_chunks:
            if chunk.strip(): # Avoid embedding empty chunks
                 vector_store.add_vector_embedding(
                     db=db_session,
                     file_id=db_file.id,
                     text_chunk=chunk,
                     embedding_model=embedding_model
                 )
        logger.info(f"Finished generating and storing embeddings for file ID: {db_file.id}")

        # 5. Update status to vectorized
        crud.file.update_file(db_session, db_file, schemas.file.FileUpdate(is_processing=False, is_vectorized=True))
        logger.info(f"Successfully processed and vectorized file ID: {db_file.id}")

    except Exception as e:
        logger.error(f"Error processing file ID {db_file.id}: {e}", exc_info=True)
        # Update status with error
        error_message = str(e)
        crud.file.update_file(db_session, db_file, schemas.file.FileUpdate(is_processing=False, is_vectorized=False, vectorization_error=error_message))

    finally:
        # Ensure session is managed appropriately if called as background task
        pass 