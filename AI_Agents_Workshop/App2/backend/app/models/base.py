"""Base model for SQLAlchemy models."""

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

# Define naming conventions for constraints
# See: https://alembic.sqlalchemy.org/en/latest/naming.html
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Create a metadata object with the naming convention
metadata = MetaData(naming_convention=convention)

class Base(DeclarativeBase):
    """Base class for all models, includes metadata with naming conventions."""
    metadata = metadata 