import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool
from dotenv import load_dotenv

from alembic import context

# Add the project root to the Python path to find modules like 'app'
# Adjust this path if your project structure is different
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Import the base model from your application
# This assumes you will have a models.py or similar containing Base
# Adjust the import path as necessary
from backend.app.models.base import Base # Placeholder for actual model base

# --- Import all models here so Base knows about them for autogenerate --- 
from backend.app.models.file import File
from backend.app.models.vector_embedding import VectorEmbedding
from backend.app.models.chat import Conversation, ChatMessage
# --- End model imports --- 

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Load environment variables from .env file specified in alembic.ini
if config.get_main_option('config_file'):
    load_dotenv(config.get_main_option('config_file'))

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def get_url():
    """Construct database URL from environment variables."""
    user = os.getenv("POSTGRES_USER", "user")
    password = os.getenv("POSTGRES_PASSWORD", "password")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "ai_agent_db")
    # Use postgresql+psycopg2 driver scheme
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Construct configuration dictionary manually
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_url()

    # Use create_engine directly with the constructed URL
    connectable = create_engine(
        get_url(),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
