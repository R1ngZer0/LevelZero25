"""
Main application entry point for the OT Interview Application.

This file initializes the FastAPI application, registers all routes,
configures middleware, and serves as the central point for the API.
"""

import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from AI_Agents_Workshop.App.Config.settings import get_settings
from AI_Agents_Workshop.App.Config.logging import configure_logging
from AI_Agents_Workshop.App.Database.db import get_db, engine
from AI_Agents_Workshop.App.Database.models import Base

from AI_Agents_Workshop.App.Api import auth, operators, interviews, analyses
from AI_Agents_Workshop.App.Api.auth import get_current_active_user, User

# Configure logging
configure_logging()
logger = logging.getLogger(__name__)

# Initialize settings
settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)
logger.info("Database tables created")

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API for interviewing and analyzing OT operators' workflows and experiences",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(
    operators.router, 
    prefix=settings.api_prefix, 
    dependencies=[Depends(get_current_active_user)]
)
app.include_router(
    interviews.router, 
    prefix=settings.api_prefix, 
    dependencies=[Depends(get_current_active_user)]
)
app.include_router(
    analyses.router, 
    prefix=settings.api_prefix, 
    dependencies=[Depends(get_current_active_user)]
)

logger.info("API routes registered")


@app.get("/")
def read_root():
    """
    Root endpoint providing basic information about the API.
    """
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "description": "API for interviewing and analyzing OT operators",
        "api_docs": f"{settings.api_prefix}/docs",
    }


@app.get("/healthcheck")
def healthcheck():
    """
    Healthcheck endpoint for monitoring systems.
    """
    logger.debug("Healthcheck endpoint called")
    return {"status": "healthy"}


@app.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get information about the currently authenticated user.
    """
    return current_user


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.app_name}")


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting development server")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 