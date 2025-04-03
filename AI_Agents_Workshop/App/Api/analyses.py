"""
API endpoints for analysis management.

This file contains FastAPI routes for creating, reading, and managing
analysis records. It also provides endpoints to trigger individual and
cross-sectional analyses.
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from AI_Agents_Workshop.App.Database.db import get_db
from AI_Agents_Workshop.App.Database.models import Analysis as AnalysisModel, Interview as InterviewModel
from AI_Agents_Workshop.App.Api.schemas import Analysis, AnalysisCreate
from AI_Agents_Workshop.App.Core.nodes.analysis import (
    trigger_individual_analysis,
    trigger_cross_section_analysis
)

router = APIRouter(
    prefix="/analyses",
    tags=["analyses"],
    responses={404: {"description": "Analysis not found"}},
)


@router.get("/", response_model=List[Analysis])
def read_analyses(
    analysis_type: Optional[str] = None,
    interview_id: Optional[UUID] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get a list of analyses, optionally filtered by type or interview ID.
    """
    query = db.query(AnalysisModel)
    
    if analysis_type:
        query = query.filter(AnalysisModel.analysis_type == analysis_type)
    
    if interview_id:
        query = query.filter(AnalysisModel.interview_id == interview_id)
    
    analyses = query.offset(skip).limit(limit).all()
    return analyses


@router.get("/{analysis_id}", response_model=Analysis)
def read_analysis(analysis_id: UUID, db: Session = Depends(get_db)):
    """
    Get a specific analysis by ID.
    """
    db_analysis = db.query(AnalysisModel).filter(
        AnalysisModel.analysis_id == analysis_id
    ).first()
    
    if db_analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return db_analysis


@router.post("/trigger/individual/{interview_id}", status_code=status.HTTP_202_ACCEPTED)
def trigger_individual(
    interview_id: UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Trigger an individual analysis for the specified interview.
    """
    # Check if the interview exists
    db_interview = db.query(InterviewModel).filter(
        InterviewModel.interview_id == interview_id
    ).first()
    
    if db_interview is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    # Trigger the analysis in the background
    background_tasks.add_task(
        trigger_individual_analysis,
        interview_id=interview_id
    )
    
    return {"message": "Individual analysis triggered successfully"}


@router.post("/trigger/cross-section", status_code=status.HTTP_202_ACCEPTED)
def trigger_cross_section(
    background_tasks: BackgroundTasks,
    operator_ids: Optional[List[UUID]] = None,
    db: Session = Depends(get_db)
):
    """
    Trigger a cross-section analysis for all interviews or a specified subset.
    """
    # Trigger the cross-section analysis in the background
    background_tasks.add_task(
        trigger_cross_section_analysis,
        operator_ids=operator_ids
    )
    
    return {"message": "Cross-section analysis triggered successfully"} 