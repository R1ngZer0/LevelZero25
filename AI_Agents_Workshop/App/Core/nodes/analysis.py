"""
Analysis nodes for processing operator interviews using LLMs.

This file contains functions for performing individual operator analysis
and cross-sectional analysis across multiple operators.
"""

import json
import logging
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from AI_Agents_Workshop.App.Config.settings import get_settings
from AI_Agents_Workshop.App.Core.prompts.analysis_prompts import (
    INDIVIDUAL_ANALYSIS_PROMPT,
    CROSS_SECTION_ANALYSIS_PROMPT
)
from AI_Agents_Workshop.App.Database.db import get_db_context
from AI_Agents_Workshop.App.Database.models import Analysis, Interview, Operator
from AI_Agents_Workshop.App.Services.llm_service import get_llm_response

# Set up logging
logger = logging.getLogger(__name__)
settings = get_settings()


def trigger_individual_analysis(interview_id: UUID):
    """
    Triggers an individual analysis for a specific interview.
    
    Args:
        interview_id: The UUID of the interview to analyze
    """
    logger.info(f"Triggering individual analysis for interview {interview_id}")
    
    with get_db_context() as db:
        # Fetch the interview and operator
        interview = db.query(Interview).filter(Interview.interview_id == interview_id).first()
        
        if not interview:
            logger.error(f"Interview {interview_id} not found")
            return
        
        operator = db.query(Operator).filter(Operator.operator_id == interview.operator_id).first()
        
        if not operator:
            logger.error(f"Operator {interview.operator_id} not found")
            return
        
        # Prepare the prompt for the LLM
        prompt = INDIVIDUAL_ANALYSIS_PROMPT.format(
            name=operator.name,
            role=operator.role,
            department=operator.department or "Not specified",
            workflow=interview.workflow or "Not provided",
            environment=interview.environment or "Not provided",
            tools_used=interview.tools_used or "Not provided",
            concerns_risks=interview.concerns_risks or "Not provided",
            safety_challenges=interview.safety_challenges or "Not provided",
            additional_notes=interview.additional_notes or "None"
        )
        
        try:
            # Get response from LLM
            llm_response = get_llm_response(prompt)
            
            # Extract summary and details (first section is summary, rest is details)
            sections = llm_response.split("\n\n")
            summary = sections[0] if sections else "Analysis completed"
            details = "\n\n".join(sections[1:]) if len(sections) > 1 else llm_response
            
            # Create a new analysis record
            analysis = Analysis(
                interview_id=interview_id,
                analysis_type="individual",
                summary=summary,
                details=details
            )
            
            db.add(analysis)
            db.commit()
            
            logger.info(f"Individual analysis completed for interview {interview_id}")
            
        except Exception as e:
            logger.error(f"Error during individual analysis: {str(e)}")
            db.rollback()


def trigger_cross_section_analysis(operator_ids: Optional[List[UUID]] = None):
    """
    Triggers a cross-sectional analysis for multiple interviews.
    
    Args:
        operator_ids: Optional list of operator IDs to include in the analysis.
                     If None, all operators are included.
    """
    logger.info("Triggering cross-sectional analysis")
    
    with get_db_context() as db:
        # Build the query for interviews
        query = db.query(Interview).join(Operator)
        
        # Filter by operator IDs if provided
        if operator_ids:
            query = query.filter(Operator.operator_id.in_(operator_ids))
        
        # Get all relevant interviews
        interviews = query.all()
        
        if not interviews:
            logger.error("No interviews found for cross-sectional analysis")
            return
        
        # Format interviews for the prompt
        interviews_data = []
        for idx, interview in enumerate(interviews, 1):
            operator = db.query(Operator).filter(
                Operator.operator_id == interview.operator_id
            ).first()
            
            interview_data = {
                "Operator": f"{operator.name} ({operator.role})",
                "Department": operator.department or "Not specified",
                "Workflow": interview.workflow or "Not provided",
                "Environment": interview.environment or "Not provided",
                "Tools Used": interview.tools_used or "Not provided",
                "Concerns/Risks": interview.concerns_risks or "Not provided",
                "Safety Challenges": interview.safety_challenges or "Not provided",
                "Additional Notes": interview.additional_notes or "None"
            }
            
            interviews_data.append(f"Interview #{idx}:\n" + 
                                 "\n".join([f"- {k}: {v}" for k, v in interview_data.items()]))
        
        # Join all interview data with separator
        all_interviews = "\n\n---\n\n".join(interviews_data)
        
        # Prepare the prompt for the LLM
        prompt = CROSS_SECTION_ANALYSIS_PROMPT.format(
            interviews_data=all_interviews
        )
        
        try:
            # Get response from LLM
            llm_response = get_llm_response(prompt)
            
            # Extract summary and details (first section is executive summary, rest is details)
            sections = llm_response.split("\n\n")
            summary = sections[0] if sections else "Cross-sectional analysis completed"
            details = "\n\n".join(sections[1:]) if len(sections) > 1 else llm_response
            
            # Create a new analysis record (without linking to a specific interview)
            analysis = Analysis(
                analysis_type="cross_section",
                summary=summary,
                details=details
            )
            
            db.add(analysis)
            db.commit()
            
            logger.info("Cross-sectional analysis completed")
            
        except Exception as e:
            logger.error(f"Error during cross-sectional analysis: {str(e)}")
            db.rollback() 