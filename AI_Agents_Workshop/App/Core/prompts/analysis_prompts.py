"""
Prompts for the LLM-based analysis of operator interviews.

This file contains prompt templates for both individual operator analysis
and cross-sectional analysis of multiple operators.
"""

# Individual analysis prompt
INDIVIDUAL_ANALYSIS_PROMPT = """
You are an expert analyst specializing in Operational Technology (OT) environments. 
I will provide you with an interview from an OT operator. Your task is to analyze this interview 
and provide insights on the operator's workflow, environment, tools, concerns, risks, and safety challenges.

Here is the interview data:
- Operator Name: {name}
- Operator Role: {role}
- Department: {department}
- Workflow Description: {workflow}
- Work Environment: {environment}
- Tools Used: {tools_used}
- Concerns and Risks: {concerns_risks}
- Safety Challenges: {safety_challenges}
- Additional Notes: {additional_notes}

Please provide an analysis with the following sections:
1. Summary: A brief overview of the operator's role and key insights.
2. Workflow Analysis: Identify patterns, efficiency opportunities, and bottlenecks.
3. Tool Usage: Evaluate the tools mentioned and potential gaps or improvement areas.
4. Risk Assessment: Analyze mentioned concerns, risks, and safety challenges.
5. Recommendations: Suggest improvements for workflow, tools, or safety measures.

Your analysis should be detailed, insightful, and actionable.
"""

# Cross-sectional analysis prompt
CROSS_SECTION_ANALYSIS_PROMPT = """
You are an expert analyst specializing in Operational Technology (OT) environments.
I will provide you with data from multiple OT operator interviews. Your task is to perform 
a cross-sectional analysis to identify patterns, common challenges, and insights across all operators.

Here are the interviews:
{interviews_data}

Please provide a comprehensive cross-sectional analysis with the following sections:
1. Executive Summary: Key findings across all interviews.
2. Common Workflows: Patterns and variations in how operators work.
3. Tool Ecosystem: Overview of tools mentioned, their frequency, and potential standardization opportunities.
4. Shared Concerns: Common risks and safety challenges mentioned across interviews.
5. Divergent Practices: Areas where operators have different approaches to similar tasks.
6. Recommendations: Strategic suggestions that would benefit multiple operators or the entire organization.
7. Areas for Further Investigation: Topics that emerged from the analysis that warrant deeper exploration.

Your analysis should identify both the commonalities and the unique aspects across all operators,
providing actionable insights for improving the OT environment as a whole.
""" 