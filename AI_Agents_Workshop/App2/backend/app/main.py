"""Main FastAPI application entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import files, agents, chat_router, documents_router # Import the documents_router

# TODO: Implement proper settings management (e.g., using Pydantic Settings)
# from . import config

settings = get_settings()

app = FastAPI(
    title="Multi-Agent AI Application Backend",
    description="API for handling agent interactions, knowledge base, and document generation.",
    version="0.1.0",
)

# Configure CORS
# TODO: Restrict origins in production
origins = [
    "http://localhost",
    "http://localhost:5173", # Default Vite dev server port
    "http://127.0.0.1:5173",
    # Add other frontend origins if necessary
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["General"])
def health_check():
    """Check if the API is running."""
    return {"status": "ok"}

# Include routers
app.include_router(files.router, prefix="/files", tags=["Files"])
app.include_router(agents.router, prefix="/agents", tags=["Agents"]) # Add agents router
app.include_router(chat_router.router, prefix="/chats", tags=["Chat"]) # Add chat router
app.include_router(documents_router.router, prefix="/documents", tags=["Documents"]) # Add documents router

# Add other routers and endpoints here later
# Example:
# from .routers import chat
# app.include_router(chat.router)

if __name__ == "__main__":
    import uvicorn
    # This is for local development running the script directly
    # Production deployments should use a process manager like Gunicorn/Uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 