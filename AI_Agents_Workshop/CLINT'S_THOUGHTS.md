These are my thoughts from the session, after the process finished running. (The process actually finished about 5 minutes after everyone left.)

1. I forogt to mention that, currently, Python 3.11 works better than the latest Python 3.13 for most GenAI generated code. Using 3.11 will prevent a lot of errors when installing the Python requirements (which the README.md explains how to do, and it's simple). I modified the README.md to explain how to install Python 3.11 in your virtual environment.

2. In your initial cursor prompt, if you tell Cursor to create the virtual environment and install all Python and Node packages once the application is built, you won't need to worry about doing anything manually as described in the README.md.

3. I meant to have Cursor use LangChain, but I forgot. I'll explain this in the upcoming bonus webinar, but you can read more about LangChain in the URLs provided in the References. In short, LangChain provided a bunch of packages that "shortcuts" many LLM functions from doing it manually.

4. Cursor chose to do a manual OpenAI API call rather than using LangChain or even the OpenAI Python package.

5. It did not create an orchestrator agent as we had asked in the initial prompt.