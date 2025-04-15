"""Service layer for interacting with the vector store (pgvector)."""

import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from typing import List, Optional
import logging

# Use centralized clients
from backend.app.llm_clients import get_embedding_client

from backend.app.models import File, VectorEmbedding
from backend.app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

def add_vector_embedding(
    db: Session,
    file_id: int,
    text_chunk: str,
    embedding_model_name: str
) -> VectorEmbedding:
    """Generates and stores a vector embedding for a text chunk associated with a file."""
    try:
        # Get the client using the provided model name (logic inside get_embedding_client handles mode)
        embedding_client = get_embedding_client() # Get client based on config
        # Verify if the model name passed matches the client's expected model if needed, or rely on get_embedding_client logic
        if embedding_client.model != embedding_model_name:
             logger.warning(f"Provided model name '{embedding_model_name}' differs from client model '{embedding_client.model}'. Using client model.")
             actual_model_name = embedding_client.model
        else:
            actual_model_name = embedding_model_name

        embedding_result = embedding_client.create(input=[text_chunk])
        if not embedding_result or not embedding_result.embeddings:
             raise ValueError("Embedding generation failed or returned empty result.")
        embedding_vector = embedding_result.embeddings[0]
        logger.info(f"Generated {len(embedding_vector)}-dim embedding using {actual_model_name}")

    except Exception as e:
        logger.error(f"Failed to generate embedding for file ID {file_id} using {actual_model_name}: {e}", exc_info=True)
        raise

    db_embedding = VectorEmbedding(
        file_id=file_id,
        embedding=np.array(embedding_vector, dtype=np.float32),
        embedding_model=actual_model_name # Store the model actually used
    )
    db.add(db_embedding)
    db.commit()
    db.refresh(db_embedding)
    logger.info(f"[VectorStoreService] Added embedding ID {db_embedding.id} for file ID {file_id}")
    return db_embedding

def delete_vector_embeddings_for_file(db: Session, file_id: int) -> int:
    """Deletes all vector embeddings associated with a specific file ID."""
    stmt = delete(VectorEmbedding).where(VectorEmbedding.file_id == file_id)
    result = db.execute(stmt)
    db.commit()
    deleted_count = result.rowcount
    logger.info(f"[VectorStoreService] Deleted {deleted_count} embeddings for file ID {file_id}")
    return deleted_count

def find_similar_embeddings(
    db: Session,
    query_text: str,
    # embedding_model_name: str, # No longer needed, use the configured client
    limit: int = 5
) -> List[VectorEmbedding]:
    """Finds vector embeddings similar to the query text using the configured model."""
    try:
        embedding_client = get_embedding_client() # Get configured client
        embedding_model_name = embedding_client.model # Get model name from client

        embedding_result = embedding_client.create(input=[query_text])
        if not embedding_result or not embedding_result.embeddings:
             raise ValueError("Query embedding generation failed or returned empty result.")
        query_embedding = embedding_result.embeddings[0]
        query_embedding_np = np.array(query_embedding, dtype=np.float32)
        logger.info(f"Generated {len(query_embedding)}-dim query embedding using {embedding_model_name}")

    except Exception as e:
        logger.error(f"Failed to generate query embedding using {embedding_model_name}: {e}", exc_info=True)
        return []

    # Ensure the search uses the same model embeddings that the client is configured for
    stmt = (
        select(VectorEmbedding)
        .where(VectorEmbedding.embedding_model == embedding_model_name)
        .order_by(VectorEmbedding.embedding.cosine_distance(query_embedding_np))
        .limit(limit)
    )

    results = db.execute(stmt).scalars().all()
    logger.info(f"[VectorStoreService] Found {len(results)} similar embeddings for query.")
    return results

# TODO:
# - Handle chunking properly: Associate embeddings with specific chunks/metadata.
# - Consider indexing strategies (e.g., HNSW index on the embedding column).
# - Refine error handling for embedding generation.
# - Implement actual embedding generation using Pydantic AI / configured models.
# - Consider indexing strategies for performance (e.g., HNSW index on the embedding column).
# - Decide on distance metric (Cosine, L2, Inner Product) and ensure consistency. 