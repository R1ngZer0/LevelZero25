# Multi-Agent AI Application

This project implements a multi-agent AI application featuring a chatbot and a document writer, leveraging a vector knowledge base built from user-uploaded files. It uses FastAPI for the backend, React with Material UI for the frontend, and PostgreSQL with pgvector for vector storage.

## Features

*   **Dual Modes:** Operates in 'Cloud' mode (using OpenAI APIs) or 'Local' mode (using Ollama).
*   **Knowledge Base:** Upload files (.txt, .pdf, .docx) to build a searchable vector knowledge base.
*   **Chat Interface:** Interact with a chatbot that utilizes the knowledge base (RAG) and conversation history.
*   **Document Writer Agent:** Generate structured documents (.docx) based on prompts, using the knowledge base and a multi-step agent process (outline -> section writing with QA -> formatting).
*   **Persistent Conversations:** Chat history is saved in the database, allowing multiple conversations.
*   **File Management:** Upload, list, download, and delete files in the knowledge base via the UI.

## Project Structure

```
/
├── backend/         # FastAPI application
│   ├── app/         # Core application code (routers, agents, schemas, etc.)
│   ├── alembic/     # Database migration scripts
│   ├── .env         # Backend environment variables (!!! IMPORTANT - see setup)
│   ├── requirements.txt
│   └── ...
├── frontend/        # React application
│   ├── src/         # Frontend source code
│   ├── public/
│   ├── .env.development # Optional frontend environment variables
│   ├── package.json
│   └── ...
├── knowledgebase/   # Stores uploaded and generated files (created automatically)
├── _DESIGN/         # Project design documents (PRD, progress, architecture)
├── docker-compose.yml # Docker configuration for PostgreSQL + pgvector
└── README.md        # This file
```

## Setup Instructions

### Prerequisites

*   **Python:** 3.10 or higher recommended.
*   **Node.js:** LTS version recommended (e.g., v18+).
*   **Docker & Docker Compose:** Required for running the PostgreSQL database.
*   **(Optional) Ollama:** Required if you want to run in 'Local' mode. Follow Ollama installation instructions and pull required models (`llama3.1:8b`, `nomic-text-embed`).
*   **API Keys:**
    *   OpenAI API Key (if using 'Cloud' mode).

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure Environment Variables
# IMPORTANT: Create a .env file in the 'backend' directory.
# Copy the structure from backend/.env.example (if provided) or create it manually.
# Example backend/.env:
# DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/ai_app_db
# APP_MODE=cloud # or "local"
# KNOWLEDGE_BASE_PATH=../knowledgebase # Relative path from backend dir
# 
# # --- OpenAI Settings (if APP_MODE=cloud) ---
# OPENAI_API_KEY=your_openai_api_key
# OPENAI_LLM_MODEL="gpt-4.1" # Or other compatible model
# OPENAI_EMBEDDING_MODEL="text-embedding-3-small"
# 
# # --- Ollama Settings (if APP_MODE=local) ---
# OLLAMA_BASE_URL=http://localhost:11434 # Default Ollama URL
# OLLAMA_LLM_MODEL="llama3.1:8b"       # Ensure this model is pulled via `ollama pull`
# OLLAMA_EMBEDDING_MODEL="nomic-text-embed" # Ensure this model is pulled
#
# Fill in your actual database credentials and API keys.

# Setup and Run Database (using Docker Compose)
# Make sure Docker Desktop is running.
# Navigate back to the project root directory
cd .. 

# Start PostgreSQL and pgvector service
docker-compose up -d

# Navigate back to backend directory
cd backend

# Run Database Migrations (Alembic)
# This creates the necessary tables (files, vector_embeddings, conversations, chat_messages)
alembic upgrade head

# (Optional) Verify backend setup before running frontend
# uvicorn app.main:app --reload --port 8000
# You can stop it with Ctrl+C after verification.
```

### 3. Frontend Setup

```bash
# Navigate to the frontend directory (from project root)
cd ../frontend 

# Install dependencies
npm install

# (Optional) Frontend Environment Variables
# The frontend API client defaults to http://127.0.0.1:8000.
# If your backend runs on a different URL/port, create a file 
# named `.env.development` in the 'frontend' directory:
# VITE_API_BASE_URL=http://your-backend-url:port
```

## Running the Application

1.  **Start the Backend Server:**
    *   Make sure your backend virtual environment is activated (`source backend/.venv/bin/activate`).
    *   Navigate to the `backend` directory.
    *   Run: `uvicorn app.main:app --reload --port 8000`

2.  **Start the Frontend Development Server:**
    *   Open a *new* terminal window/tab.
    *   Navigate to the `frontend` directory.
    *   Run: `npm run dev`

3.  **Access the Application:**
    *   Open your web browser and go to the URL provided by the frontend server (usually `http://localhost:5173`).

## Usage

1.  **Mode Selection:** Go to the `Settings` page (gear icon) to choose between `Cloud (OpenAI)` and `Local (Ollama)` modes. The selected mode affects which LLM and embedding models are used by the backend.
2.  **Knowledge Base:** Go to the `Knowledge Base` page (folder icon) to upload files (.txt, .pdf, .docx). Uploaded files will be processed, chunked, vectorized, and stored for use in RAG.
You can also download or delete existing files here.
3.  **Chat:** Select an existing conversation from the sidebar or click "New Chat". Type messages in the input box. The chatbot will use the selected mode's LLM, conversation history, and relevant context from the knowledge base to respond.
4.  **Document Creation:** Use the "Create Document" section at the bottom of the chat page. Enter a prompt describing the document you want to create. The Document Writer agent will generate the document in the background (using the selected mode's LLM and knowledge base) and save it as a .docx file in the `knowledgebase` folder.
You should see a success message, and the file will appear in the Knowledge Base list after generation.

## Stopping the Application

1.  Stop the frontend server (Press `Ctrl+C` in the frontend terminal).
2.  Stop the backend server (Press `Ctrl+C` in the backend terminal).
3.  Stop the database container:
    ```bash
    # From the project root directory
    docker-compose down
    ``` 