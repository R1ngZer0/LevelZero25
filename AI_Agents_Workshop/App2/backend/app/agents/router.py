"""Logic for the Router Agent/Orchestrator."""

import logging
from pydantic_ai import Agent

from app.llm_clients import get_llm_client
from app.schemas import RouterInput, RouterOutput, RouteDecision, AgentType

logger = logging.getLogger(__name__)

async def route_prompt(input_data: RouterInput) -> RouterOutput:
    """Determines the appropriate agent for a given prompt using an LLM call."""

    llm_client = get_llm_client()
    pydantic_ai_router = Agent(
        llm=llm_client,
        output_model=RouteDecision
    )

    prompt_lines = [
        "Analyze the following user prompt and determine the most appropriate agent to handle it.",
        "",
        "Available agents:",
        f"- {AgentType.CHATBOT.value}: Best for general conversation, questions about existing knowledge, or information retrieval.",
        f"- {AgentType.DOC_WRITER.value}: Best for requests to create new documents, outlines, reports, or structured content based on a topic or existing knowledge.",
        "",
        "User Prompt:",
       f'"""{input_data.prompt}"""',
        "",
        "Based on the prompt, decide which agent "
       f"({AgentType.CHATBOT.value} or {AgentType.DOC_WRITER.value}) is the best fit and provide a brief reasoning."
    ]
    prompt_template = "\n".join(prompt_lines)

    logger.info(f"Routing prompt (conversation ID: {input_data.conversation_id}): '{input_data.prompt[:100]}...'")

    try:
        decision: RouteDecision = await pydantic_ai_router.run_async(prompt_template)
        logger.info(f"LLM decided route: Agent='{decision.agent}', Reasoning='{decision.reasoning}'")

        router_output = RouterOutput(
            agent_type=decision.agent,
            original_prompt=input_data.prompt,
            conversation_id=input_data.conversation_id
        )
        return router_output

    except Exception as e:
        logger.error(f"Error during prompt routing: {e}", exc_info=True)
        logger.warning("Routing failed. Defaulting to Chatbot Agent.")
        return RouterOutput(
            agent_type=AgentType.CHATBOT,
            original_prompt=input_data.prompt,
            conversation_id=input_data.conversation_id
        )

# Placeholder for downstream agent calls (will be replaced by actual agent logic)
async def invoke_chatbot(data: RouterOutput):
    logger.info(f"[Placeholder] Invoking Chatbot for prompt: {data.original_prompt[:50]}...")
    return {"response": f"Chatbot received: {data.original_prompt}", "agent": "chatbot"}

async def invoke_doc_writer(data: RouterOutput):
    logger.info(f"[Placeholder] Invoking Doc Writer for prompt: {data.original_prompt[:50]}...")
    return {"response": f"Doc Writer received: {data.original_prompt}", "agent": "doc_writer"}
 