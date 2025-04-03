"""
API endpoints for interview management.

This file contains FastAPI routes for creating, reading, updating, and deleting
interview records in the database.
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from AI_Agents_Workshop.App.Database.db import get_db
from AI_Agents_Workshop.App.Database.models import Interview as InterviewModel, Operator as OperatorModel
from AI_Agents_Workshop.App.Api.schemas import Interview, InterviewCreate, InterviewUpdate, InterviewWithAnalyses
from AI_Agents_Workshop.App.Core.nodes.analysis import trigger_individual_analysis

router = APIRouter(
    prefix="/interviews",
    tags=["interviews"],
    responses={404: {"description": "Interview not found"}},
)


@router.post("/", response_model=Interview, status_code=status.HTTP_201_CREATED)
def create_interview(
    interview: InterviewCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create a new interview and optionally trigger analysis in the background.
    """
    # Check if the operator exists
    db_operator = db.query(OperatorModel).filter(
        OperatorModel.operator_id == interview.operator_id
    ).first()
    
    if db_operator is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operator not found"
        )
    
    # Create the interview
    db_interview = InterviewModel(**interview.dict())
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    
    # Trigger analysis in the background
    background_tasks.add_task(
        trigger_individual_analysis,
        interview_id=db_interview.interview_id
    )
    
    return db_interview


@router.get("/", response_model=List[Interview])
def read_interviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get a list of all interviews.
    """
    interviews = db.query(InterviewModel).offset(skip).limit(limit).all()
    return interviews


@router.get("/{interview_id}", response_model=InterviewWithAnalyses)
def read_interview(interview_id: UUID, db: Session = Depends(get_db)):
    """
    Get a specific interview by ID, including its analyses.
    """
    db_interview = db.query(InterviewModel).filter(
        InterviewModel.interview_id == interview_id
    ).first()
    
    if db_interview is None:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    return db_interview


@router.put("/{interview_id}", response_model=Interview)
def update_interview(
    interview_id: UUID, 
    interview: InterviewUpdate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Update an interview's information and optionally trigger a new analysis.
    """
    db_interview = db.query(InterviewModel).filter(
        InterviewModel.interview_id == interview_id
    ).first()
    
    if db_interview is None:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    # Update the interview fields
    for key, value in interview.dict(exclude_unset=True).items():
        setattr(db_interview, key, value)
    
    db.commit()
    db.refresh(db_interview)
    
    # Trigger a new analysis in the background
    background_tasks.add_task(
        trigger_individual_analysis,
        interview_id=interview_id
    )
    
    return db_interview


@router.delete("/{interview_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interview(interview_id: UUID, db: Session = Depends(get_db)):
    """
    Delete an interview.
    """
    db_interview = db.query(InterviewModel).filter(
        InterviewModel.interview_id == interview_id
    ).first()
    
    if db_interview is None:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    db.delete(db_interview)
    db.commit()
    
    return None 