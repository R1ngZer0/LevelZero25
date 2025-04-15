"""SQLAlchemy model for storing file metadata."""

import datetime
from sqlalchemy import String, DateTime, func, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class File(Base):
    """Represents a file stored in the knowledge base."""
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String, index=True, nullable=False)
    # Store the path relative to the KNOWLEDGE_BASE_PATH
    relative_path: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=True)
    content_hash: Mapped[str] = mapped_column(String, nullable=True, index=True) # Optional hash of file content
    media_type: Mapped[str] = mapped_column(String, nullable=True) # e.g., application/pdf, text/plain

    is_processing: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_vectorized: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    vectorization_error: Mapped[str] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<File(id={self.id}, filename='{self.filename}', relative_path='{self.relative_path}')>" 