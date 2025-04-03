"""
Pydantic schemas for the OT Interview Application.

This file contains Pydantic models that provide data validation, 
serialization, and documentation for the API endpoints.
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class OperatorBase(BaseModel):
    """Base model for Operator data."""
    name: str
    role: str
    department: Optional[str] = None


class OperatorCreate(OperatorBase):
    """Schema for creating a new operator."""
    pass


class OperatorUpdate(OperatorBase):
    """Schema for updating an operator."""
    name: Optional[str] = None
    role: Optional[str] = None


class Operator(OperatorBase):
    """Schema for a complete operator record."""
    operator_id: UUID = Field(default_factory=uuid4)
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class InterviewBase(BaseModel):
    """Base model for Interview data."""
    workflow: Optional[str] = None
    environment: Optional[str] = None
    tools_used: Optional[str] = None
    concerns_risks: Optional[str] = None
    safety_challenges: Optional[str] = None
    additional_notes: Optional[str] = None


class InterviewCreate(InterviewBase):
    """Schema for creating a new interview."""
    operator_id: UUID


class InterviewUpdate(InterviewBase):
    """Schema for updating an interview."""
    pass


class Interview(InterviewBase):
    """Schema for a complete interview record."""
    interview_id: UUID = Field(default_factory=uuid4)
    operator_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class AnalysisBase(BaseModel):
    """Base model for Analysis data."""
    analysis_type: str  # 'individual' or 'cross_section'
    summary: Optional[str] = None
    details: Optional[str] = None


class AnalysisCreate(AnalysisBase):
    """Schema for creating a new analysis."""
    interview_id: Optional[UUID] = None  # Optional for cross-section analysis


class Analysis(AnalysisBase):
    """Schema for a complete analysis record."""
    analysis_id: UUID = Field(default_factory=uuid4)
    interview_id: Optional[UUID] = None
    created_at: datetime

    class Config:
        orm_mode = True


class OperatorWithInterviews(Operator):
    """Schema for an operator with all their interviews."""
    interviews: List[Interview] = []


class InterviewWithAnalyses(Interview):
    """Schema for an interview with all its analyses."""
    analyses: List[Analysis] = []
    operator: Operator 