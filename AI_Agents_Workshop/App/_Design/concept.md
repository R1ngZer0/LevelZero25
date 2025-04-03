# App Concept
An app that interviews OT operators to understand their job, workflow, environment, tools they use, concerns, risks, what works and what doesn't, safey challenges, and notes section where the operators can enter in additional comments. Web front-end. Structured database to store interviews. We'll need to store and cross-reference the different kinds of operators. We should then have an agent/node that uses an LLM to analyze the results and provide analysis on each operator, which includes a summary and details. And then another node/agent that can do a cross section anlysis over all interviewees. 

This will be a multi-agent system that uses a supervisor/coordinator agent and the the nodes described above.

# Tech Stack
Python backend
Node.js/React frontend
Pydantic for structured input/output validation



# Directory Structure

├── Api
├── Config
├── Core
│   ├── nodes
│   └── prompts
├── Database
├── Logs
├── Pipelines
├── Services
└── Utils