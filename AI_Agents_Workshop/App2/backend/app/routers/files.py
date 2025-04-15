"""API Endpoints for file management."""

import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FastAPIFile, status
from sqlalchemy.orm import Session
from typing import List
import logging

from app import schemas, crud, models
from app.db.session import get_db
from app.config import get_settings
from app.services import file_processor, vector_store # Ensure vector_store is imported

router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__) # Add logger

@router.post("/upload", response_model=schemas.FileRead, status_code=status.HTTP_201_CREATED)
def upload_file(file: UploadFile = FastAPIFile(...), db: Session = Depends(get_db)):
    """Handles file uploads, saves the file, and creates a DB record.

    This currently saves the file directly. In a production scenario,
    consider background tasks for processing and vectorization.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")

    kb_path = settings.KNOWLEDGE_BASE_PATH
    # Basic sanitization (consider more robust checks)
    safe_filename = os.path.basename(file.filename)
    relative_save_path = safe_filename # Simplistic path for now
    full_save_path = os.path.join(kb_path, relative_save_path)

    # Ensure knowledgebase directory exists
    os.makedirs(kb_path, exist_ok=True)

    # Check if file with the same relative path already exists
    db_existing_file = crud.get_file_by_relative_path(db, relative_path=relative_save_path)
    if db_existing_file:
        raise HTTPException(
            status_code=409, # Conflict
            detail=f"File with path '{relative_save_path}' already exists."
        )

    file_size = 0
    try:
        with open(full_save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_size = os.path.getsize(full_save_path)
    except Exception as e:
        # Clean up partially saved file if error occurs
        if os.path.exists(full_save_path):
            os.remove(full_save_path)
        raise HTTPException(
            status_code=500,
            detail=f"Could not save file: {e}"
        )
    finally:
        file.file.close()

    # Create DB entry
    file_in = schemas.FileCreate(
        filename=safe_filename,
        media_type=file.content_type,
        file_size_bytes=file_size
    )
    db_file = crud.create_file(db=db, file_in=file_in, relative_path=relative_save_path)

    # --- Trigger processing synchronously (for now) --- 
    print(f"File '{safe_filename}' uploaded successfully. DB ID: {db_file.id}")
    print("Triggering synchronous file processing/vectorization...")
    try:
        # Pass the db_file.id and the existing session
        file_processor.process_file_and_vectorize(db_file.id, db)
        print(f"Synchronous processing finished for file ID: {db_file.id}")
        # Refresh the file object to get updated status
        db.refresh(db_file)
    except Exception as e:
        # Log the error but don't crash the upload request itself
        # The processing function should handle setting the error state in the DB
        print(f"Error during synchronous processing trigger for file ID {db_file.id}: {e}")

    return db_file

@router.get("/", response_model=List[schemas.FileRead])
def list_files(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lists files currently in the knowledge base (metadata from DB)."""
    files = crud.get_files(db, skip=skip, limit=limit)
    return files

@router.delete("/{file_id}", response_model=schemas.FileRead, status_code=status.HTTP_200_OK)
def delete_file_endpoint(
    file_id: int,
    db: Session = Depends(get_db)
):
    """Deletes a file, its database record, and associated vector embeddings."""
    db_file = crud.get_file(db, file_id=file_id)
    if not db_file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    # Construct the full path *before* deleting the DB record
    full_path = os.path.join(settings.KNOWLEDGE_BASE_PATH, db_file.relative_path)

    try:
        # 1. Delete vector embeddings first
        deleted_vector_count = vector_store.delete_vector_embeddings_for_file(db=db, file_id=file_id)
        logger.info(f"Deleted {deleted_vector_count} vector embeddings for file ID {file_id}.")

        # 2. Delete the database record
        deleted_db_file = crud.delete_file(db=db, file_id=file_id)
        if not deleted_db_file:
            # This shouldn't happen if get_file succeeded, but check anyway
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File found initially but failed to delete from DB")
        logger.info(f"Deleted file record from DB for file ID {file_id}.")

        # 3. Delete the physical file
        if os.path.exists(full_path):
            os.remove(full_path)
            logger.info(f"Deleted physical file: {full_path}")
        else:
            logger.warning(f"Physical file not found for deletion: {full_path}")

        # Return the data of the deleted file
        # Note: deleted_db_file is the object before deletion commit, safe to return
        return deleted_db_file

    except Exception as e:
        logger.error(f"Error deleting file ID {file_id}: {e}", exc_info=True)
        # Consider rolling back DB changes if possible/needed, though vector delete and file delete were committed.
        # For simplicity, we raise a generic server error here.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during file deletion: {e}"
        )

# TODO: Add endpoints for getting a single file, downloading a file. 