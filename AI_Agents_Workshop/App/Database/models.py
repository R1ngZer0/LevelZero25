"""
Database models for the OT Interview Application.

This file contains SQLAlchemy models that represent the database schema
for storing operator profiles, interviews, and analysis results.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, create_engine, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """
    Represents a user who can log into the system.
    Users can have different roles (operator, admin, etc.).
    """
    __tablename__ = 'users'
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    role = Column(String(20), default="operator")  # operator or admin
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with Operator (optional)
    operator = relationship("Operator", back_populates="user", uselist=False)


class Operator(Base):
    """
    Represents an OT operator in the system.
    """
    __tablename__ = 'operators'
    
    operator_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    department = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key to User
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=True)
    
    # Relationships
    interviews = relationship("Interview", back_populates="operator")
    user = relationship("User", back_populates="operator")


class Interview(Base):
    """
    Represents an interview with an OT operator.
    """
    __tablename__ = 'interviews'
    
    interview_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    operator_id = Column(UUID(as_uuid=True), ForeignKey('operators.operator_id'), nullable=False)
    workflow = Column(Text)
    environment = Column(Text)
    tools_used = Column(Text)
    concerns_risks = Column(Text)
    safety_challenges = Column(Text)
    additional_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    operator = relationship("Operator", back_populates="interviews")
    analyses = relationship("Analysis", back_populates="interview")


class Analysis(Base):
    """
    Represents an analysis of an interview, either for a single operator 
    or a cross-section of multiple operators.
    """
    __tablename__ = 'analyses'
    
    analysis_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    interview_id = Column(UUID(as_uuid=True), ForeignKey('interviews.interview_id'), nullable=True)
    analysis_type = Column(String(20), nullable=False)  # 'individual' or 'cross_section'
    summary = Column(Text)
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    interview = relationship("Interview", back_populates="analyses")


# Database connection setup
def get_engine(connection_string):
    """
    Creates and returns a SQLAlchemy engine using the provided connection string.
    """
    return create_engine(connection_string)


def init_db(engine):
    """
    Initializes the database by creating all tables if they don't exist.
    """
    Base.metadata.create_all(engine) 