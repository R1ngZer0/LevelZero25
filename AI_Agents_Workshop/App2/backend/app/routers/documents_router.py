"""
API Router for Document Creation interactions.
"""

from fastapi import APIRouter, HTTPException, Body, BackgroundTasks
from pydantic import BaseModel

from app.agents.doc_writer_agent import create_document, DocumentCreationResult

router = APIRouter()

class DocumentCreateRequest(BaseModel):
    """Request model for initiating document creation."""
    prompt: str
    mode: str = "cloud" # Allow specifying mode

@router.post("/create", response_model=DocumentCreationResult, status_code=202) # Use 202 Accepted for background tasks
def create_document_endpoint(
    request: DocumentCreateRequest = Body(...),
    background_tasks: BackgroundTasks = None # Inject background tasks
):
    """Initiates the document creation process in the background."""
    # Add the potentially long-running task to the background
    background_tasks.add_task(create_document, request.prompt, request.mode)
    
    # Immediately return an accepted response
    return DocumentCreationResult(
        message="Document creation process initiated in the background. Check logs or status endpoint (if implemented) for progress.",
        file_path=None # File path is not known yet
    )

# TODO (Optional): Implement a status check endpoint using the task ID if 
# using a more sophisticated background task system like Celery. 