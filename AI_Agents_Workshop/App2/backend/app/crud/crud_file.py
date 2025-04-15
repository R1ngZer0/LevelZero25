"""CRUD operations for the File model."""

from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from typing import List, Optional

from backend.app.models import File
from backend.app.schemas import FileCreate, FileUpdate

def create_file(db: Session, file_in: FileCreate, relative_path: str) -> File:
    """Creates a new file record in the database."""
    db_file = File(
        filename=file_in.filename,
        relative_path=relative_path,
        media_type=file_in.media_type,
        file_size_bytes=file_in.file_size_bytes,
        is_processing=False, # Default status
        is_vectorized=False
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_file(db: Session, file_id: int) -> Optional[File]:
    """Gets a file record by its ID."""
    return db.get(File, file_id)

def get_file_by_relative_path(db: Session, relative_path: str) -> Optional[File]:
    """Gets a file record by its relative path."""
    stmt = select(File).where(File.relative_path == relative_path)
    return db.execute(stmt).scalar_one_or_none()

def get_files(db: Session, skip: int = 0, limit: int = 100) -> List[File]:
    """Gets a list of file records."""
    stmt = select(File).offset(skip).limit(limit).order_by(File.created_at.desc())
    return db.execute(stmt).scalars().all()

def update_file(db: Session, db_file: File, file_in: FileUpdate) -> File:
    """Updates a file record."""
    update_data = file_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_file, key, value)
    # Explicitly handle clearing the error if set to None
    if file_in.vectorization_error is None and 'vectorization_error' in update_data:
        setattr(db_file, 'vectorization_error', None)

    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def delete_file(db: Session, file_id: int) -> Optional[File]:
    """Deletes a file record by its ID."""
    db_file = db.get(File, file_id)
    if db_file:
        db.delete(db_file)
        db.commit()
        return db_file
    return None 