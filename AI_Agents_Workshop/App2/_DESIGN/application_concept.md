App Description:

This is a multi-agent application based on Pydantic AI as the backend with a Node.js REACT frontend. The frontend can accept user files for upload to be processed into the knowledgebase. The frontend should be able to display the files in the knowledgebase and provide the ability to manage those files, including the ability to delete and download the files. When a file is deleted, it should remove it from the knowledebase folder and also remove it from the vector store. There is a chatbot that allows the user to allow the user to ask questions about the knowledgebase as well as have the agent system create documentation based on both the LLM training data as well as the knowledgebase. There should be a reflection/validation agent that reviews all other LLM responses and provides feedback (using its own training data as well as the knowledgebase data). All agents use LLM calls, via Pydantic AI. The validation agent will provide feedback to the chatbot agent and the document writer agent. The agents will revise and pass back to the validation agent until the validation agent approves the response, OR until a maximum of 3 revisions. Uploaded docs and created docs are stored in the /knowldgebase folder.

Use the app_architecture.jpg as an architecture reference

Router functionality:

    - The router should determine if the incoming prompt is general chat or document creation and route appropriately

Chatbot specifics:

    - The chatbot should be able to start and store multiple conversations and allow the user to select a given conversation
    - The chatbot should be able to check the knowledgebase for information but also be able to use its own training data
    - Message history for each conversation should be maintained for conversation context
    - The chatbot interfaces with the validation agent until the validation agent approves the output and then the chatbot sends the final reponse to the user

Document writer agent process:

    - The document writer will first use a @tool (outline creator) that uses the LLM to create an outline
    - The document writer will then use another @tool (section writer) for each part of the outline
    - For each section of the outline, the tool uses an LLM call to flesh out that section
    - Each run should interface with the validation agent for final approval before submitting the final output to the current doc creation storage
    - The previous doc section creations should be maintained and passed to the next subsequent section creation step to maintain context and to prevent duplication
    - Once the entire document text is completed, the document writer will use another @tool (report writer) to convert the document into a nicely formatted HTML file. The HTML file should then be converted to a Word docx file. The final docments should be stored in the /knowledgebase folder
    - The original text should also be vectorized and stored in the vector store

Specific Requirements:

    - The application should run on Windows, Linux, and MacOS, but is being developed on MacOS.
    - The application should use the following LLM models via Pydantic AI:
        - gpt-4.1 for cloud mode
        - Llama3.1:8b via Ollama for local mode
        - The mode should be set in the main menu.
    - The application should use the following database:
        - PostGreSQL for structured data (if applicable)
    - The application should use the following vector database:
        - Pgvector extension for PostgreSQL
    - Environment variables should be stored in /.env at the root
    - The application should use the following text embedding models:
        - text-embedding-3-small via OpenAI for cloud mode
        - nomic-text-embed via Ollama for local mode
    - When the application processes an data file from user upload, it should put the files in the /knowledgebase folder and then vectorize it for RAG.
    - The application should use the following for the frontend/UI:
        - Node.js REACT
        - Materials UI
    - The application should use the following frameworks for the backend:
        - Pydantic
        - Pydantic AI
    - The application should use the following API framework:
        - Whatever works best with Pydantic AI