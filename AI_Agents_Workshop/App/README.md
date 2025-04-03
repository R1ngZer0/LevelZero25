# OT Interview Analysis System

A multi-agent system for conducting interviews with Operational Technology (OT) operators, storing their responses, and providing both individual and cross-sectional analyses.

## Features

- **Interview Capture**: Web-based forms to collect detailed information from OT operators about their workflows, environment, tools, concerns, risks, and safety challenges.
- **Structured Storage**: Secure database for storing operator profiles and their interview responses.
- **LLM-Powered Analysis**: 
  - Individual operator analysis that identifies patterns, efficiency opportunities, tool usage, and risks.
  - Cross-sectional analysis that reveals common trends, shared concerns, and improvement areas across all operators.
- **Multi-Agent Architecture**: 
  - Supervisor/Coordinator agent orchestrates data flow and analysis requests.
  - Individual analysis agent processes single interviews in depth.
  - Cross-section agent consolidates insights across multiple operators.
- **Security**: Role-based access control ensures operators can only view their own data while supervisors have broader access.

## Implementation Details

### Backend (Python/FastAPI)

- **Database Models**: SQLAlchemy ORM models for Operators, Interviews, Analyses, and Users
- **API Endpoints**: FastAPI routes for CRUD operations on all entities
- **Authentication**: JWT-based authentication with role-based access control
- **LLM Integration**: 
  - OpenAI API integration (default) with fallback to local LLM
  - Structured prompt templates for individual and cross-sectional analyses
- **Multi-Agent System**:
  - Coordinator agent for managing data flow and analysis requests
  - Analysis nodes for processing individual interviews and cross-sectional datasets

### Frontend (React)

- **Authentication**: JWT-based login with secure token storage
- **Dashboard**: Overview of operators, interviews, and analyses with recent activity
- **Interview Form**: Comprehensive form for capturing OT operator interviews
- **Analysis Views**: Components for viewing individual and cross-sectional analyses
- **User Management**: Role-based interfaces (operator vs. admin)

## System Architecture

The application follows a modern, modular architecture:

- **Backend**: Python with FastAPI and SQLAlchemy
- **Database**: PostgreSQL (configurable)
- **LLM Integration**: OpenAI API (default) with support for local LLM deployment
- **Authentication**: JWT-based with role authorization
- **Frontend**: React with Material-UI components

## Directory Structure

```
App/
├── Api/           # FastAPI routes and API endpoints
├── Config/        # Application configuration
├── Core/          # Core functionality
│   ├── nodes/     # Multi-agent nodes
│   └── prompts/   # LLM prompt templates
├── Database/      # Database models and connection handling
├── frontend/      # React frontend application
├── Logs/          # Application logs
├── Pipelines/     # Analysis pipelines
├── Services/      # External services integration (LLM, etc.)
└── Utils/         # Utility functions
```

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Node.js 14 or higher
- PostgreSQL (optional, SQLite can be used for development)

### Backend Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd AI_Agents_Workshop/App
   ```

2. Create and activate a virtual environment:
   ```
   python311 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the App directory with the following variables:
   ```
   DATABASE_URL=postgresql://user:password@localhost/ot_interviews
   SECRET_KEY=your_secret_key_here
   LLM_PROVIDER=openai
   LLM_API_KEY=your_openai_api_key
   LLM_MODEL_NAME=gpt-4
   ```

### Frontend Installation

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

### Running the Application

1. Start the backend:
   ```
   cd AI_Agents_Workshop/App
   python main.py
   ```

2. Start the frontend (in a separate terminal):
   ```
   cd AI_Agents_Workshop/App/frontend
   npm start
   ```

3. Access the application at:
   ```
   http://localhost:3000
   ```

4. Access the API documentation at:
   ```
   http://localhost:8000/api/docs
   ```

## Development

### Adding a New Feature

1. Create appropriate models in `Database/models.py`
2. Add Pydantic schemas in `Api/schemas.py`
3. Create API endpoints in `Api/your_feature.py`
4. Register your router in `main.py`
5. Implement React components in the frontend

### Working with LLMs

To modify prompts for analysis:
1. Edit templates in `Core/prompts/analysis_prompts.py`
2. If needed, update the analysis logic in `Core/nodes/analysis.py`

## License

[License information] 