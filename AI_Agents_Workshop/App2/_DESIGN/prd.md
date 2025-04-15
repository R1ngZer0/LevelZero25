# Product Requirements Document (PRD) - Multi-Agent AI Application

## 1. Introduction & Goals

This document outlines the requirements for a multi-agent application designed to assist users with knowledge management and document creation. The application leverages Pydantic AI for its backend agent system and features a Node.js REACT frontend.

**Core Goals:**

*   Provide a chatbot interface for querying a knowledge base and general LLM capabilities.
*   Enable users to upload files to build a searchable knowledge base.
*   Offer an agent-driven process for creating structured documents based on prompts and the knowledge base.
*   Ensure the quality and relevance of generated content through a reflection/QA agent.
*   Provide a user-friendly interface for managing files within the knowledge base.

## 2. System Architecture

*(Refer to `app_architecture.jpg` for a visual representation)*

**Key Components:**

*   **Frontend:** Node.js REACT application with Material UI for user interaction, file uploads, chat interface, and knowledge base management.
*   **Backend API:** Built with a framework compatible with Pydantic AI (e.g., FastAPI, Flask) to handle requests from the frontend.
*   **Router Agent/Orchestrator:** Directs user prompts to the appropriate agent (Chatbot or Doc Writer).
*   **Chatbot Agent:** Handles conversational interactions, querying the vector store and base LLM, and managing conversation history.
*   **Doc Writer Agent:** Manages the document creation process using specialized tools (Outline Creator, Section Writer, Report Writer).
*   **File Processor:** Handles uploaded files, stores them, and initiates vectorization.
*   **Reflection/QA Agent:** Reviews outputs from the Chatbot and Doc Writer agents, provides feedback, and ensures quality before final output. Iterates up to 3 times for revisions.
*   **Vector Store:** PostgreSQL database with the pgvector extension, storing vectorized representations of knowledge base documents for RAG.
*   **File Storage:** A designated folder (e.g., `/knowledgebase`) for storing original uploaded and generated documents.
*   **(Optional) Task Queue:** Celery and Redis if asynchronous task management becomes necessary for file processing or agent operations.

## 3. Functional Requirements

### 3.1. User Interface (Frontend)

*   Allow users to upload files.
*   Display files currently in the knowledge base.
*   Allow users to download files from the knowledge base.
*   Allow users to delete files from the knowledge base.
*   Provide a chat interface for interacting with the Chatbot Agent.
*   Allow users to select and manage multiple chat conversations.
*   Provide an interface to initiate document creation requests.
*   Allow users to select the operational mode (Cloud/Local LLM).

### 3.2. File Management

*   When a file is uploaded:
    *   Store the file in the `/knowledgebase` folder.
    *   Process the file content.
    *   Vectorize the file content using the appropriate embedding model (based on mode).
    *   Store the vectors in the Vector Store (PostgreSQL with pgvector).
*   When a file is deleted:
    *   Remove the file from the `/knowledgebase` folder.
    *   Remove the corresponding vectors from the Vector Store.

### 3.3. Router Agent / Orchestrator

*   Receive user prompts (from chat or document creation request).
*   Determine if the prompt is for general chat or document creation.
*   Route the request to the Chatbot Agent or Doc Writer Agent accordingly.

### 3.4. Chatbot Agent

*   Receive prompts routed by the Router Agent.
*   Maintain separate conversation histories for context.
*   Query the Vector Store for relevant information from the knowledge base (RAG).
*   Utilize the base LLM (defined by the selected mode) for general knowledge and conversation.
*   Formulate responses based on query results and conversation history.
*   Submit responses to the Reflection/QA Agent for review.
*   Revise responses based on feedback from the Reflection/QA Agent (up to 3 revisions).
*   Send the final, approved response to the frontend.

### 3.5. Document Writer Agent

*   Receive document creation prompts routed by the Router Agent.
*   Utilize an "Outline Creator" tool (LLM-based) to generate a document outline.
*   For each section in the outline:
    *   Utilize a "Section Writer" tool (LLM-based) to generate content for that section.
    *   Maintain context from previously generated sections.
    *   Submit the generated section content to the Reflection/QA Agent for review.
    *   Revise section content based on feedback (up to 3 revisions per section).
    *   Store the approved section content temporarily.
*   Once all sections are complete and approved:
    *   Assemble the full document text.
    *   Utilize a "Report Writer" tool to:
        *   Format the text into an HTML file.
        *   Convert the HTML file into a Word (.docx) file.
    *   Store the final .docx file in the `/knowledgebase` folder.
    *   Vectorize the full document text.
    *   Store the vectors in the Vector Store.

### 3.6. Reflection/QA Agent

*   Receive draft responses/content from the Chatbot Agent and Doc Writer Agent.
*   Evaluate the content based on relevance, accuracy, and quality, using its own training and the knowledge base (Vector Store).
*   Provide feedback for revision or approve the content.
*   Limit revisions to a maximum of 3 per interaction cycle.

### 3.7. File Processing & Vectorization

*   Handle various common file types for text extraction (e.g., .txt, .pdf, .docx).
*   Chunk documents appropriately for vectorization.
*   Utilize the selected embedding model (OpenAI or Nomic via Ollama) to generate vectors.
*   Interface with the Vector Store (PostgreSQL/pgvector) to store and retrieve vectors.

## 4. Technical Requirements

*   **Backend Frameworks:** Pydantic, Pydantic AI
*   **Backend API Framework:** To be determined (compatible with Pydantic AI, e.g., FastAPI, Flask)
*   **Frontend Framework:** Node.js REACT
*   **UI Library:** Material UI
*   **Database (Structured Data):** PostgreSQL (if needed beyond vector storage)
*   **Vector Database:** PostgreSQL with pgvector extension
*   **Database Migration:** Alembic
*   **LLM Integration:** Pydantic AI
*   **LLM Models:**
    *   Cloud Mode: `gpt-4.1` (via OpenAI API)
    *   Local Mode: `Llama3.1:8b` (via Ollama)
*   **Embedding Models:**
    *   Cloud Mode: `text-embedding-3-small` (via OpenAI API)
    *   Local Mode: `nomic-text-embed` (via Ollama)
*   **Configuration:** Environment variables stored in `.env` file at the project root.
*   **Task Queue (if needed):** Celery and Redis
*   **Knowledge Base Storage:** `/knowledgebase` folder within the project structure.

## 5. Non-Functional Requirements

*   **Platform Compatibility:** Must run on Windows, Linux, and macOS.
*   **Mode Selection:** User must be able to switch between Cloud and Local modes via the UI.
*   **Maintainability:** Code should be clean, organized, and follow best practices (simple solutions, avoid duplication, adhere to file size limits).
*   **Scalability:** Consider potential future needs for handling larger knowledge bases or more concurrent users (Celery/Redis might be relevant here). 