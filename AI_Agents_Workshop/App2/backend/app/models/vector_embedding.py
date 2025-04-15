"""SQLAlchemy model for storing vector embeddings."""

import datetime
from sqlalchemy import Integer, ForeignKey, DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from .base import Base

# Determine vector dimensions based on embedding model in config?
# Or just set a reasonably large default? OpenAI text-embedding-3-small is 1536
# Nomic-embed-text is 768. Let's use 1536 for now to be safe.
VECTOR_DIMENSIONS = 1536

class VectorEmbedding(Base):
    """Represents a vector embedding associated with a file or chunk."""
    __tablename__ = "vector_embeddings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Foreign key to the file this embedding belongs to
    file_id: Mapped[int] = mapped_column(Integer, ForeignKey("files.id", ondelete="CASCADE"), index=True)
    # TODO: Add chunk identifier if implementing chunking

    # The actual vector embedding
    embedding: Mapped[Vector] = mapped_column(Vector(VECTOR_DIMENSIONS))

    # Metadata
    embedding_model: Mapped[str] = mapped_column(String, nullable=True) # Store which model generated it
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationship back to the File model (optional but useful)
    # file = relationship("File", back_populates="embeddings") # Needs back_populates on File model

    def __repr__(self) -> str:
        return f"<VectorEmbedding(id={self.id}, file_id={self.file_id}, model='{self.embedding_model}')>" 