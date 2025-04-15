"""Pydantic schemas for file data transfer."""

import datetime
from pydantic import BaseModel
from typing import Optional

class FileBase(BaseModel):
    """Base schema for file properties."""
    filename: str
    media_type: Optional[str] = None
    file_size_bytes: Optional[int] = None

class FileCreate(FileBase):
    """Schema used for creating a file record (doesn't include path)."""
    pass # Path is determined internally on save

class FileRead(FileBase):
    """Schema for reading file data, including DB fields."""
    id: int
    relative_path: str
    is_processing: bool
    is_vectorized: bool
    vectorization_error: Optional[str] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True # Enable ORM mode

class FileUpdate(BaseModel):
    """Schema for updating file properties (e.g., processing status)."""
    is_processing: Optional[bool] = None
    is_vectorized: Optional[bool] = None
    vectorization_error: Optional[str] = None # Use Optional to allow clearing the error 