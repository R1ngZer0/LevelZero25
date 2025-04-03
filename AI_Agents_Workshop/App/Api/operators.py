"""
API endpoints for operator management.

This file contains FastAPI routes for creating, reading, updating, and deleting
operator records in the database.
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from AI_Agents_Workshop.App.Database.db import get_db
from AI_Agents_Workshop.App.Database.models import Operator as OperatorModel
from AI_Agents_Workshop.App.Api.schemas import Operator, OperatorCreate, OperatorUpdate, OperatorWithInterviews

router = APIRouter(
    prefix="/operators",
    tags=["operators"],
    responses={404: {"description": "Operator not found"}},
)


@router.post("/", response_model=Operator, status_code=status.HTTP_201_CREATED)
def create_operator(operator: OperatorCreate, db: Session = Depends(get_db)):
    """
    Create a new operator.
    """
    db_operator = OperatorModel(**operator.dict())
    db.add(db_operator)
    db.commit()
    db.refresh(db_operator)
    return db_operator


@router.get("/", response_model=List[Operator])
def read_operators(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get a list of all operators.
    """
    operators = db.query(OperatorModel).offset(skip).limit(limit).all()
    return operators


@router.get("/{operator_id}", response_model=OperatorWithInterviews)
def read_operator(operator_id: UUID, db: Session = Depends(get_db)):
    """
    Get a specific operator by ID, including their interviews.
    """
    db_operator = db.query(OperatorModel).filter(OperatorModel.operator_id == operator_id).first()
    if db_operator is None:
        raise HTTPException(status_code=404, detail="Operator not found")
    return db_operator


@router.put("/{operator_id}", response_model=Operator)
def update_operator(operator_id: UUID, operator: OperatorUpdate, db: Session = Depends(get_db)):
    """
    Update an operator's information.
    """
    db_operator = db.query(OperatorModel).filter(OperatorModel.operator_id == operator_id).first()
    if db_operator is None:
        raise HTTPException(status_code=404, detail="Operator not found")
        
    for key, value in operator.dict(exclude_unset=True).items():
        setattr(db_operator, key, value)
        
    db.commit()
    db.refresh(db_operator)
    return db_operator


@router.delete("/{operator_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_operator(operator_id: UUID, db: Session = Depends(get_db)):
    """
    Delete an operator.
    """
    db_operator = db.query(OperatorModel).filter(OperatorModel.operator_id == operator_id).first()
    if db_operator is None:
        raise HTTPException(status_code=404, detail="Operator not found")
        
    db.delete(db_operator)
    db.commit()
    return None 