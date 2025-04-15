https://ai.pydantic.dev/
https://ai.pydantic.dev/agents/
https://ai.pydantic.dev/models/
https://ai.pydantic.dev/dependencies/
https://ai.pydantic.dev/tools/
https://ai.pydantic.dev/results/
https://ai.pydantic.dev/message-history/
https://ai.pydantic.dev/multi-agent-applications/
https://ai.pydantic.dev/graph/


# Tools & Dependency Injection Example
Here is a concise example using PydanticAI to build a support agent for a bank:

bank_support.py
```
from dataclasses import dataclass

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

from bank_database import DatabaseConn


@dataclass
class SupportDependencies:  
    customer_id: int
    db: DatabaseConn  


class SupportResult(BaseModel):  
    support_advice: str = Field(description='Advice returned to the customer')
    block_card: bool = Field(description="Whether to block the customer's card")
    risk: int = Field(description='Risk level of query', ge=0, le=10)


support_agent = Agent(  
    'openai:gpt-4o',  
    deps_type=SupportDependencies,
    result_type=SupportResult,  
    system_prompt=(  
        'You are a support agent in our bank, give the '
        'customer support and judge the risk level of their query.'
    ),
)


@support_agent.system_prompt  
async def add_customer_name(ctx: RunContext[SupportDependencies]) -> str:
    customer_name = await ctx.deps.db.customer_name(id=ctx.deps.customer_id)
    return f"The customer's name is {customer_name!r}"


@support_agent.tool  
async def customer_balance(
    ctx: RunContext[SupportDependencies], include_pending: bool
) -> float:
    """Returns the customer's current account balance."""  
    return await ctx.deps.db.customer_balance(
        id=ctx.deps.customer_id,
        include_pending=include_pending,
    )


...  


async def main():
    deps = SupportDependencies(customer_id=123, db=DatabaseConn())
    result = await support_agent.run('What is my balance?', deps=deps)  
    print(result.data)  
    """
    support_advice='Hello John, your current account balance, including pending transactions, is $123.45.' block_card=False risk=1
    """

    result = await support_agent.run('I just lost my card!', deps=deps)
    print(result.data)
    """
    support_advice="I'm sorry to hear that, John. We are temporarily blocking your card to prevent unauthorized transactions." block_card=True risk=8
    """
```

Complete bank_support.py example

The code included here is incomplete for the sake of brevity (the definition of DatabaseConn is missing); you can find the complete bank_support.py example here.

Instrumentation with Pydantic Logfire
To understand the flow of the above runs, we can watch the agent in action using Pydantic Logfire.

To do this, we need to set up logfire, and add the following to our code:

bank_support_with_logfire.py
```
...
from bank_database import DatabaseConn

import logfire
logfire.configure()  
logfire.instrument_asyncpg()  
...
```

# Agents
## Introduction
Agents are PydanticAI's primary interface for interacting with LLMs.

In some use cases a single Agent will control an entire application or component, but multiple agents can also interact to embody more complex workflows.

The Agent class has full API documentation, but conceptually you can think of an agent as a container for:

Component	                Description
System prompt(s)	        A set of instructions for the LLM written by the developer.
Function tool(s)	        Functions that the LLM may call to get information while generating a response.
Structured result type	    The structured datatype the LLM must return at the end of a run, if specified.
Dependency type constraint	System prompt functions, tools, and result validators may all use dependencies when they're run.
LLM model	                Optional default LLM model associated with the agent. Can also be specified when running the agent.
Model Settings	            Optional default model settings to help fine tune requests. Can also be specified when running the agent.

In typing terms, agents are generic in their dependency and result types, e.g., an agent which required dependencies of type Foobar and returned results of type list[str] would have type Agent[Foobar, list[str]]. In practice, you shouldn't need to care about this, it should just mean your IDE can tell you when you have the right type, and if you choose to use static type checking it should work well with PydanticAI.

Here's a toy example of an agent that simulates a roulette wheel:

roulette_wheel.py
```
from pydantic_ai import Agent, RunContext

roulette_agent = Agent(  
    'openai:gpt-4o',
    deps_type=int,
    result_type=bool,
    system_prompt=(
        'Use the `roulette_wheel` function to see if the '
        'customer has won based on the number they provide.'
    ),
)


@roulette_agent.tool
async def roulette_wheel(ctx: RunContext[int], square: int) -> str:  
    """check if the square is a winner"""
    return 'winner' if square == ctx.deps else 'loser'


# Run the agent
success_number = 18  
result = roulette_agent.run_sync('Put my money on square eighteen', deps=success_number)
print(result.data)  
#> True

result = roulette_agent.run_sync('I bet five is the winner', deps=success_number)
print(result.data)
#> False
```

Agents are designed for reuse, like FastAPI Apps

Agents are intended to be instantiated once (frequently as module globals) and reused throughout your application, similar to a small FastAPI app or an APIRouter.

## Running Agents
There are three ways to run an agent:

agent.run() — a coroutine which returns a RunResult containing a completed response
agent.run_sync() — a plain, synchronous function which returns a RunResult containing a completed response (internally, this just calls loop.run_until_complete(self.run()))
agent.run_stream() — a coroutine which returns a StreamedRunResult, which contains methods to stream a response as an async iterable
Here's a simple example demonstrating all three:

run_agent.py
```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

result_sync = agent.run_sync('What is the capital of Italy?')
print(result_sync.data)
#> Rome


async def main():
    result = await agent.run('What is the capital of France?')
    print(result.data)
    #> Paris

    async with agent.run_stream('What is the capital of the UK?') as response:
        print(await response.get_data())
        #> London
```

(This example is complete, it can be run "as is" — you'll need to add asyncio.run(main()) to run main)
You can also pass messages from previous runs to continue a conversation or provide context, as described in Messages and Chat History.

## Additional Configuration
### Usage Limits
PydanticAI offers a UsageLimits structure to help you limit your usage (tokens and/or requests) on model runs.

You can apply these settings by passing the usage_limits argument to the run{_sync,_stream} functions.

Consider the following example, where we limit the number of response tokens:

```
from pydantic_ai import Agent
from pydantic_ai.exceptions import UsageLimitExceeded
from pydantic_ai.usage import UsageLimits

agent = Agent('anthropic:claude-3-5-sonnet-latest')

result_sync = agent.run_sync(
    'What is the capital of Italy? Answer with just the city.',
    usage_limits=UsageLimits(response_tokens_limit=10),
)
print(result_sync.data)
#> Rome
print(result_sync.usage())
"""
Usage(requests=1, request_tokens=62, response_tokens=1, total_tokens=63, details=None)
"""

try:
    result_sync = agent.run_sync(
        'What is the capital of Italy? Answer with a paragraph.',
        usage_limits=UsageLimits(response_tokens_limit=10),
    )
except UsageLimitExceeded as e:
    print(e)
    #> Exceeded the response_tokens_limit of 10 (response_tokens=32)
```

Restricting the number of requests can be useful in preventing infinite loops or excessive tool calling:

```
from typing_extensions import TypedDict

from pydantic_ai import Agent, ModelRetry
from pydantic_ai.exceptions import UsageLimitExceeded
from pydantic_ai.usage import UsageLimits


class NeverResultType(TypedDict):
    """
    Never ever coerce data to this type.
    """

    never_use_this: str


agent = Agent(
    'anthropic:claude-3-5-sonnet-latest',
    retries=3,
    result_type=NeverResultType,
    system_prompt='Any time you get a response, call the `infinite_retry_tool` to produce another response.',
)


@agent.tool_plain(retries=5)  
def infinite_retry_tool() -> int:
    raise ModelRetry('Please try again.')


try:
    result_sync = agent.run_sync(
        'Begin infinite retry loop!', usage_limits=UsageLimits(request_limit=3)  
    )
except UsageLimitExceeded as e:
    print(e)
    #> The next request would exceed the request_limit of 3
```

**Note**

This is especially relevant if you're registered a lot of tools, request_limit can be used to prevent the model from choosing to make too many of these calls.

### Model (Run) Settings
PydanticAI offers a settings.ModelSettings structure to help you fine tune your requests. This structure allows you to configure common parameters that influence the model's behavior, such as temperature, max_tokens, timeout, and more.

There are two ways to apply these settings: 1. Passing to run{_sync,_stream} functions via the model_settings argument. This allows for fine-tuning on a per-request basis. 2. Setting during Agent initialization via the model_settings argument. These settings will be applied by default to all subsequent run calls using said agent. However, model_settings provided during a specific run call will override the agent's default settings.

For example, if you'd like to set the temperature setting to 0.0 to ensure less random behavior, you can do the following:

```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

result_sync = agent.run_sync(
    'What is the capital of Italy?', model_settings={'temperature': 0.0}
)
print(result_sync.data)
#> Rome
```

### Model specific settings
If you wish to further customize model behavior, you can use a subclass of ModelSettings, like GeminiModelSettings, associated with your model of choice.

For example:

```
from pydantic_ai import Agent, UnexpectedModelBehavior
from pydantic_ai.models.gemini import GeminiModelSettings

agent = Agent('google-gla:gemini-1.5-flash')

try:
    result = agent.run_sync(
        'Write a list of 5 very rude things that I might say to the universe after stubbing my toe in the dark:',
        model_settings=GeminiModelSettings(
            temperature=0.0,  # general model settings can also be specified
            gemini_safety_settings=[
                {
                    'category': 'HARM_CATEGORY_HARASSMENT',
                    'threshold': 'BLOCK_LOW_AND_ABOVE',
                },
                {
                    'category': 'HARM_CATEGORY_HATE_SPEECH',
                    'threshold': 'BLOCK_LOW_AND_ABOVE',
                },
            ],
        ),
    )
except UnexpectedModelBehavior as e:
    print(e)  
    """
    Safety settings triggered, body:
    <safety settings details>
    """
```

### Runs vs. Conversations
An agent run might represent an entire conversation — there's no limit to how many messages can be exchanged in a single run. However, a conversation might also be composed of multiple runs, especially if you need to maintain state between separate interactions or API calls.

Here's an example of a conversation comprised of multiple runs:

conversation_example.py

```
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

# First run
result1 = agent.run_sync('Who was Albert Einstein?')
print(result1.data)
#> Albert Einstein was a German-born theoretical physicist.

# Second run, passing previous messages
result2 = agent.run_sync(
    'What was his most famous equation?',
    message_history=result1.new_messages(),  
)
print(result2.data)
#> Albert Einstein's most famous equation is (E = mc^2).
(This example is complete, it can be run "as is")
```

### Type safe by design
PydanticAI is designed to work well with static type checkers, like mypy and pyright.

Typing is (somewhat) optional

PydanticAI is designed to make type checking as useful as possible for you if you choose to use it, but you don't have to use types everywhere all the time.

That said, because PydanticAI uses Pydantic, and Pydantic uses type hints as the definition for schema and validation, some types (specifically type hints on parameters to tools, and the result_type arguments to Agent) are used at runtime.

We (the library developers) have messed up if type hints are confusing you more than helping you, if you find this, please create an issue explaining what's annoying you!

In particular, agents are generic in both the type of their dependencies and the type of results they return, so you can use the type hints to ensure you're using the right types.

Consider the following script with type mistakes:

type_mistakes.py

```
from dataclasses import dataclass

from pydantic_ai import Agent, RunContext


@dataclass
class User:
    name: str


agent = Agent(
    'test',
    deps_type=User,  
    result_type=bool,
)


@agent.system_prompt
def add_user_name(ctx: RunContext[str]) -> str:  
    return f"The user's name is {ctx.deps}."


def foobar(x: bytes) -> None:
    pass


result = agent.run_sync('Does their name start with "A"?', deps=User('Anne'))
foobar(result.data)  
```

Running mypy on this will give the following output:

```
➤ uv run mypy type_mistakes.
➤ uv run mypy type_mistakes.py
type_mistakes.py:18: error: Argument 1 to "system_prompt" of "Agent" has incompatible type "Callable[[RunContext[str]], str]"; expected "Callable[[RunContext[User]], str]"  [arg-type]
type_mistakes.py:28: error: Argument 1 to "foobar" has incompatible type "bool"; expected "bytes"  [arg-type]
Found 2 errors in 1 file (checked 1 source file)
```

Running pyright would identify the same issues.

## System Prompts
System prompts might seem simple at first glance since they're just strings (or sequences of strings that are concatenated), but crafting the right system prompt is key to getting the model to behave as you want.

Generally, system prompts fall into two categories:

Static system prompts: These are known when writing the code and can be defined via the system_prompt parameter of the Agent constructor.
Dynamic system prompts: These depend in some way on context that isn't known until runtime, and should be defined via functions decorated with @agent.system_prompt.
You can add both to a single agent; they're appended in the order they're defined at runtime.

Here's an example using both types of system prompts:

system_prompts.py

```
from datetime import date

from pydantic_ai import Agent, RunContext

agent = Agent(
    'openai:gpt-4o',
    deps_type=str,  
    system_prompt="Use the customer's name while replying to them.",  
)


@agent.system_prompt  
def add_the_users_name(ctx: RunContext[str]) -> str:
    return f"The user's name is {ctx.deps}."


@agent.system_prompt
def add_the_date() -> str:  
    return f'The date is {date.today()}.'


result = agent.run_sync('What is the date?', deps='Frank')
print(result.data)
#> Hello Frank, the date today is 2032-01-02.
```
(This example is complete, it can be run "as is")

## Reflection and self-correction
Validation errors from both function tool parameter validation and structured result validation can be passed back to the model with a request to retry.

You can also raise ModelRetry from within a tool or result validator function to tell the model it should retry generating a response.

The default retry count is 1 but can be altered for the entire agent, a specific tool, or a result validator.
You can access the current retry count from within a tool or result validator via ctx.retry.
Here's an example:

tool_retry.py

```
from pydantic import BaseModel

from pydantic_ai import Agent, RunContext, ModelRetry

from fake_database import DatabaseConn


class ChatResult(BaseModel):
    user_id: int
    message: str


agent = Agent(
    'openai:gpt-4o',
    deps_type=DatabaseConn,
    result_type=ChatResult,
)


@agent.tool(retries=2)
def get_user_by_name(ctx: RunContext[DatabaseConn], name: str) -> int:
    """Get a user's ID from their full name."""
    print(name)
    #> John
    #> John Doe
    user_id = ctx.deps.users.get(name=name)
    if user_id is None:
        raise ModelRetry(
            f'No user found with name {name!r}, remember to provide their full name'
        )
    return user_id


result = agent.run_sync(
    'Send a message to John Doe asking for coffee next week', deps=DatabaseConn()
)
print(result.data)
"""
user_id=123 message='Hello John, would you be free for coffee sometime next week? Let me know what works for you!'
"""
```

## Model errors
If models behave unexpectedly (e.g., the retry limit is exceeded, or their API returns 503), agent runs will raise UnexpectedModelBehavior.

In these cases, capture_run_messages can be used to access the messages exchanged during the run to help diagnose the issue.

```
from pydantic_ai import Agent, ModelRetry, UnexpectedModelBehavior, capture_run_messages

agent = Agent('openai:gpt-4o')


@agent.tool_plain
def calc_volume(size: int) -> int:  
    if size == 42:
        return size**3
    else:
        raise ModelRetry('Please try again.')


with capture_run_messages() as messages:  
    try:
        result = agent.run_sync('Please get me the volume of a box with size 6.')
    except UnexpectedModelBehavior as e:
        print('An error occurred:', e)
        #> An error occurred: Tool exceeded max retries count of 1
        print('cause:', repr(e.__cause__))
        #> cause: ModelRetry('Please try again.')
        print('messages:', messages)
        """
        messages:
        [
            ModelRequest(
                parts=[
                    UserPromptPart(
                        content='Please get me the volume of a box with size 6.',
                        timestamp=datetime.datetime(...),
                        part_kind='user-prompt',
                    )
                ],
                kind='request',
            ),
            ModelResponse(
                parts=[
                    ToolCallPart(
                        tool_name='calc_volume',
                        args={'size': 6},
                        tool_call_id=None,
                        part_kind='tool-call',
                    )
                ],
                model_name='function:model_logic',
                timestamp=datetime.datetime(...),
                kind='response',
            ),
            ModelRequest(
                parts=[
                    RetryPromptPart(
                        content='Please try again.',
                        tool_name='calc_volume',
                        tool_call_id=None,
                        timestamp=datetime.datetime(...),
                        part_kind='retry-prompt',
                    )
                ],
                kind='request',
            ),
            ModelResponse(
                parts=[
                    ToolCallPart(
                        tool_name='calc_volume',
                        args={'size': 6},
                        tool_call_id=None,
                        part_kind='tool-call',
                    )
                ],
                model_name='function:model_logic',
                timestamp=datetime.datetime(...),
                kind='response',
            ),
        ]
        """
    else:
        print(result.data)
```

(This example is complete, it can be run "as is")

**Note**

If you call run, run_sync, or run_stream more than once within a single capture_run_messages context, messages will represent the messages exchanged during the first call only.


# Models
## OpenAI

Install
To use OpenAI models, you need to either install pydantic-ai, or install pydantic-ai-slim with the openai optional group:


pip
uv

pip install 'pydantic-ai-slim[openai]'

Configuration
To use OpenAIModel through their main API, go to platform.openai.com and follow your nose until you find the place to generate an API key.

Environment variable
Once you have the API key, you can set it as an environment variable:


export OPENAI_API_KEY='your-api-key'
You can then use OpenAIModel by name:

openai_model_by_name.py

from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')
...
Or initialise the model directly with just the model name:

openai_model_init.py

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

model = OpenAIModel('gpt-4o')
agent = Agent(model)
...
api_key argument
If you don't want to or can't set the environment variable, you can pass it at runtime via the api_key argument:

openai_model_api_key.py

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

model = OpenAIModel('gpt-4o', api_key='your-api-key')
agent = Agent(model)
...
Custom OpenAI Client
OpenAIModel also accepts a custom AsyncOpenAI client via the openai_client parameter, so you can customise the organization, project, base_url etc. as defined in the OpenAI API docs.

You could also use the AsyncAzureOpenAI client to use the Azure OpenAI API.

openai_azure.py

from openai import AsyncAzureOpenAI

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

client = AsyncAzureOpenAI(
    azure_endpoint='...',
    api_version='2024-07-01-preview',
    api_key='your-api-key',
)

model = OpenAIModel('gpt-4o', openai_client=client)
agent = Agent(model)
...

Ollama
To use Ollama, you must first download the Ollama client, and then download a model using the Ollama model library.

You must also ensure the Ollama server is running when trying to make requests to it. For more information, please see the Ollama documentation.

Example local usage
With ollama installed, you can run the server with the model you want to use:

terminal-run-ollama

ollama run llama3.2
(this will pull the llama3.2 model if you don't already have it downloaded)
Then run your code, here's a minimal example:

ollama_example.py

from pydantic import BaseModel

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel


class CityLocation(BaseModel):
    city: str
    country: str


ollama_model = OpenAIModel(model_name='llama3.2', base_url='http://localhost:11434/v1')
agent = Agent(ollama_model, result_type=CityLocation)

result = agent.run_sync('Where were the olympics held in 2012?')
print(result.data)
#> city='London' country='United Kingdom'
print(result.usage())
"""
Usage(requests=1, request_tokens=57, response_tokens=8, total_tokens=65, details=None)
"""
Example using a remote server
ollama_example_with_remote_server.py

from pydantic import BaseModel

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

ollama_model = OpenAIModel(
    model_name='qwen2.5-coder:7b',  
    base_url='http://192.168.1.74:11434/v1',  
)


class CityLocation(BaseModel):
    city: str
    country: str


agent = Agent(model=ollama_model, result_type=CityLocation)

result = agent.run_sync('Where were the olympics held in 2012?')
print(result.data)
#> city='London' country='United Kingdom'
print(result.usage())
"""
Usage(requests=1, request_tokens=57, response_tokens=8, total_tokens=65, details=None)
"""
OpenRouter
To use OpenRouter, first create an API key at openrouter.ai/keys.

Once you have the API key, you can pass it to OpenAIModel as the api_key argument:

openrouter_model_init.py

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

model = OpenAIModel(
    'anthropic/claude-3.5-sonnet',
    base_url='https://openrouter.ai/api/v1',
    api_key='your-openrouter-api-key',
)
agent = Agent(model)
...
Grok (xAI)
Go to xAI API Console and create an API key. Once you have the API key, follow the xAI API Documentation, and set the base_url and api_key arguments appropriately:

grok_model_init.py

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

model = OpenAIModel(
    'grok-2-1212',
    base_url='https://api.x.ai/v1',
    api_key='your-xai-api-key',
)
agent = Agent(model)
...
DeepSeek
Go to DeepSeek API Platform and create an API key. Once you have the API key, follow the DeepSeek API Documentation, and set the base_url and api_key arguments appropriately:

deepseek_model_init.py

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

model = OpenAIModel(
    'deepseek-chat',
    base_url='https://api.deepseek.com',
    api_key='your-deepseek-api-key',
)
agent = Agent(model)
...
Implementing Custom Models
To implement support for models not already supported, you will need to subclass the Model abstract base class.

For streaming, you'll also need to implement the following abstract base class:

StreamedResponse
The best place to start is to review the source code for existing implementations, e.g. OpenAIModel.

For details on when we'll accept contributions adding new models to PydanticAI, see the contributing guidelines.

# Dependencies
PydanticAI uses a dependency injection system to provide data and services to your agent's system prompts, tools and result validators.

Matching PydanticAI's design philosophy, our dependency system tries to use existing best practice in Python development rather than inventing esoteric "magic", this should make dependencies type-safe, understandable easier to test and ultimately easier to deploy in production.

Defining Dependencies
Dependencies can be any python type. While in simple cases you might be able to pass a single object as a dependency (e.g. an HTTP connection), dataclasses are generally a convenient container when your dependencies included multiple objects.

Here's an example of defining an agent that requires dependencies.

(Note: dependencies aren't actually used in this example, see Accessing Dependencies below)

unused_dependencies.py

from dataclasses import dataclass

import httpx

from pydantic_ai import Agent


@dataclass
class MyDeps:  
    api_key: str
    http_client: httpx.AsyncClient


agent = Agent(
    'openai:gpt-4o',
    deps_type=MyDeps,  
)


async def main():
    async with httpx.AsyncClient() as client:
        deps = MyDeps('foobar', client)
        result = await agent.run(
            'Tell me a joke.',
            deps=deps,  
        )
        print(result.data)
        #> Did you hear about the toothpaste scandal? They called it Colgate.
(This example is complete, it can be run "as is" — you'll need to add asyncio.run(main()) to run main)

Accessing Dependencies
Dependencies are accessed through the RunContext type, this should be the first parameter of system prompt functions etc.

system_prompt_dependencies.py

from dataclasses import dataclass

import httpx

from pydantic_ai import Agent, RunContext


@dataclass
class MyDeps:
    api_key: str
    http_client: httpx.AsyncClient


agent = Agent(
    'openai:gpt-4o',
    deps_type=MyDeps,
)


@agent.system_prompt  
async def get_system_prompt(ctx: RunContext[MyDeps]) -> str:  
    response = await ctx.deps.http_client.get(  
        'https://example.com',
        headers={'Authorization': f'Bearer {ctx.deps.api_key}'},  
    )
    response.raise_for_status()
    return f'Prompt: {response.text}'


async def main():
    async with httpx.AsyncClient() as client:
        deps = MyDeps('foobar', client)
        result = await agent.run('Tell me a joke.', deps=deps)
        print(result.data)
        #> Did you hear about the toothpaste scandal? They called it Colgate.
(This example is complete, it can be run "as is" — you'll need to add asyncio.run(main()) to run main)

Asynchronous vs. Synchronous dependencies
System prompt functions, function tools and result validators are all run in the async context of an agent run.

If these functions are not coroutines (e.g. async def) they are called with run_in_executor in a thread pool, it's therefore marginally preferable to use async methods where dependencies perform IO, although synchronous dependencies should work fine too.

run vs. run_sync and Asynchronous vs. Synchronous dependencies

Whether you use synchronous or asynchronous dependencies, is completely independent of whether you use run or run_sync — run_sync is just a wrapper around run and agents are always run in an async context.

Here's the same example as above, but with a synchronous dependency:

sync_dependencies.py

from dataclasses import dataclass

import httpx

from pydantic_ai import Agent, RunContext


@dataclass
class MyDeps:
    api_key: str
    http_client: httpx.Client  


agent = Agent(
    'openai:gpt-4o',
    deps_type=MyDeps,
)


@agent.system_prompt
def get_system_prompt(ctx: RunContext[MyDeps]) -> str:  
    response = ctx.deps.http_client.get(
        'https://example.com', headers={'Authorization': f'Bearer {ctx.deps.api_key}'}
    )
    response.raise_for_status()
    return f'Prompt: {response.text}'


async def main():
    deps = MyDeps('foobar', httpx.Client())
    result = await agent.run(
        'Tell me a joke.',
        deps=deps,
    )
    print(result.data)
    #> Did you hear about the toothpaste scandal? They called it Colgate.
(This example is complete, it can be run "as is" — you'll need to add asyncio.run(main()) to run main)

Full Example
As well as system prompts, dependencies can be used in tools and result validators.

full_example.py

from dataclasses import dataclass

import httpx

from pydantic_ai import Agent, ModelRetry, RunContext


@dataclass
class MyDeps:
    api_key: str
    http_client: httpx.AsyncClient


agent = Agent(
    'openai:gpt-4o',
    deps_type=MyDeps,
)


@agent.system_prompt
async def get_system_prompt(ctx: RunContext[MyDeps]) -> str:
    response = await ctx.deps.http_client.get('https://example.com')
    response.raise_for_status()
    return f'Prompt: {response.text}'


@agent.tool  
async def get_joke_material(ctx: RunContext[MyDeps], subject: str) -> str:
    response = await ctx.deps.http_client.get(
        'https://example.com#jokes',
        params={'subject': subject},
        headers={'Authorization': f'Bearer {ctx.deps.api_key}'},
    )
    response.raise_for_status()
    return response.text


@agent.result_validator  
async def validate_result(ctx: RunContext[MyDeps], final_response: str) -> str:
    response = await ctx.deps.http_client.post(
        'https://example.com#validate',
        headers={'Authorization': f'Bearer {ctx.deps.api_key}'},
        params={'query': final_response},
    )
    if response.status_code == 400:
        raise ModelRetry(f'invalid response: {response.text}')
    response.raise_for_status()
    return final_response


async def main():
    async with httpx.AsyncClient() as client:
        deps = MyDeps('foobar', client)
        result = await agent.run('Tell me a joke.', deps=deps)
        print(result.data)
        #> Did you hear about the toothpaste scandal? They called it Colgate.
(This example is complete, it can be run "as is" — you'll need to add asyncio.run(main()) to run main)

Overriding Dependencies
When testing agents, it's useful to be able to customise dependencies.

While this can sometimes be done by calling the agent directly within unit tests, we can also override dependencies while calling application code which in turn calls the agent.

This is done via the override method on the agent.

joke_app.py

from dataclasses import dataclass

import httpx

from pydantic_ai import Agent, RunContext


@dataclass
class MyDeps:
    api_key: str
    http_client: httpx.AsyncClient

    async def system_prompt_factory(self) -> str:  
        response = await self.http_client.get('https://example.com')
        response.raise_for_status()
        return f'Prompt: {response.text}'


joke_agent = Agent('openai:gpt-4o', deps_type=MyDeps)


@joke_agent.system_prompt
async def get_system_prompt(ctx: RunContext[MyDeps]) -> str:
    return await ctx.deps.system_prompt_factory()  


async def application_code(prompt: str) -> str:  
    ...
    ...
    # now deep within application code we call our agent
    async with httpx.AsyncClient() as client:
        app_deps = MyDeps('foobar', client)
        result = await joke_agent.run(prompt, deps=app_deps)  
    return result.data
(This example is complete, it can be run "as is")

test_joke_app.py

from joke_app import MyDeps, application_code, joke_agent


class TestMyDeps(MyDeps):  
    async def system_prompt_factory(self) -> str:
        return 'test prompt'


async def test_application_code():
    test_deps = TestMyDeps('test_key', None)  
    with joke_agent.override(deps=test_deps):  
        joke = await application_code('Tell me a joke.')  
    assert joke.startswith('Did you hear about the toothpaste scandal?')
Examples
The following examples demonstrate how to use dependencies in PydanticAI:

Weather Agent
SQL Generation
RAG

# Function Tools
Function tools provide a mechanism for models to retrieve extra information to help them generate a response.

They're useful when it is impractical or impossible to put all the context an agent might need into the system prompt, or when you want to make agents' behavior more deterministic or reliable by deferring some of the logic required to generate a response to another (not necessarily AI-powered) tool.

Function tools vs. RAG

Function tools are basically the "R" of RAG (Retrieval-Augmented Generation) — they augment what the model can do by letting it request extra information.

The main semantic difference between PydanticAI Tools and RAG is RAG is synonymous with vector search, while PydanticAI tools are more general-purpose. (Note: we may add support for vector search functionality in the future, particularly an API for generating embeddings. See #58)

There are a number of ways to register tools with an agent:

via the @agent.tool decorator — for tools that need access to the agent context
via the @agent.tool_plain decorator — for tools that do not need access to the agent context
via the tools keyword argument to Agent which can take either plain functions, or instances of Tool
@agent.tool is considered the default decorator since in the majority of cases tools will need access to the agent context.

Here's an example using both:

dice_game.py

import random

from pydantic_ai import Agent, RunContext

agent = Agent(
    'google-gla:gemini-1.5-flash',  
    deps_type=str,  
    system_prompt=(
        "You're a dice game, you should roll the die and see if the number "
        "you get back matches the user's guess. If so, tell them they're a winner. "
        "Use the player's name in the response."
    ),
)


@agent.tool_plain  
def roll_die() -> str:
    """Roll a six-sided die and return the result."""
    return str(random.randint(1, 6))


@agent.tool  
def get_player_name(ctx: RunContext[str]) -> str:
    """Get the player's name."""
    return ctx.deps


dice_result = agent.run_sync('My guess is 4', deps='Anne')  
print(dice_result.data)
#> Congratulations Anne, you guessed correctly! You're a winner!
(This example is complete, it can be run "as is")

Let's print the messages from that game to see what happened:

dice_game_messages.py

from dice_game import dice_result

print(dice_result.all_messages())
"""
[
    ModelRequest(
        parts=[
            SystemPromptPart(
                content="You're a dice game, you should roll the die and see if the number you get back matches the user's guess. If so, tell them they're a winner. Use the player's name in the response.",
                dynamic_ref=None,
                part_kind='system-prompt',
            ),
            UserPromptPart(
                content='My guess is 4',
                timestamp=datetime.datetime(...),
                part_kind='user-prompt',
            ),
        ],
        kind='request',
    ),
    ModelResponse(
        parts=[
            ToolCallPart(
                tool_name='roll_die', args={}, tool_call_id=None, part_kind='tool-call'
            )
        ],
        model_name='function:model_logic',
        timestamp=datetime.datetime(...),
        kind='response',
    ),
    ModelRequest(
        parts=[
            ToolReturnPart(
                tool_name='roll_die',
                content='4',
                tool_call_id=None,
                timestamp=datetime.datetime(...),
                part_kind='tool-return',
            )
        ],
        kind='request',
    ),
    ModelResponse(
        parts=[
            ToolCallPart(
                tool_name='get_player_name',
                args={},
                tool_call_id=None,
                part_kind='tool-call',
            )
        ],
        model_name='function:model_logic',
        timestamp=datetime.datetime(...),
        kind='response',
    ),
    ModelRequest(
        parts=[
            ToolReturnPart(
                tool_name='get_player_name',
                content='Anne',
                tool_call_id=None,
                timestamp=datetime.datetime(...),
                part_kind='tool-return',
            )
        ],
        kind='request',
    ),
    ModelResponse(
        parts=[
            TextPart(
                content="Congratulations Anne, you guessed correctly! You're a winner!",
                part_kind='text',
            )
        ],
        model_name='function:model_logic',
        timestamp=datetime.datetime(...),
        kind='response',
    ),
]
"""
We can represent this with a diagram:

LLM
Agent
LLM
Agent
Send prompts
LLM decides to use
a tool
Rolls a six-sided die
LLM decides to use
another tool
Retrieves player name
LLM constructs final response
Game session complete
System: "You're a dice game..."
User: "My guess is 4"
Call tool
roll_die()
ToolReturn
"4"
Call tool
get_player_name()
ToolReturn
"Anne"
ModelResponse
"Congratulations Anne, ..."
Registering Function Tools via kwarg
As well as using the decorators, we can register tools via the tools argument to the Agent constructor. This is useful when you want to reuse tools, and can also give more fine-grained control over the tools.

dice_game_tool_kwarg.py

import random

from pydantic_ai import Agent, RunContext, Tool


def roll_die() -> str:
    """Roll a six-sided die and return the result."""
    return str(random.randint(1, 6))


def get_player_name(ctx: RunContext[str]) -> str:
    """Get the player's name."""
    return ctx.deps


agent_a = Agent(
    'google-gla:gemini-1.5-flash',
    deps_type=str,
    tools=[roll_die, get_player_name],  
)
agent_b = Agent(
    'google-gla:gemini-1.5-flash',
    deps_type=str,
    tools=[  
        Tool(roll_die, takes_ctx=False),
        Tool(get_player_name, takes_ctx=True),
    ],
)
dice_result = agent_b.run_sync('My guess is 4', deps='Anne')
print(dice_result.data)
#> Congratulations Anne, you guessed correctly! You're a winner!
(This example is complete, it can be run "as is")

Function Tools vs. Structured Results
As the name suggests, function tools use the model's "tools" or "functions" API to let the model know what is available to call. Tools or functions are also used to define the schema(s) for structured responses, thus a model might have access to many tools, some of which call function tools while others end the run and return a result.

Function tools and schema
Function parameters are extracted from the function signature, and all parameters except RunContext are used to build the schema for that tool call.

Even better, PydanticAI extracts the docstring from functions and (thanks to griffe) extracts parameter descriptions from the docstring and adds them to the schema.

Griffe supports extracting parameter descriptions from google, numpy, and sphinx style docstrings. PydanticAI will infer the format to use based on the docstring, but you can explicitly set it using docstring_format. You can also enforce parameter requirements by setting require_parameter_descriptions=True. This will raise a UserError if a parameter description is missing.

To demonstrate a tool's schema, here we use FunctionModel to print the schema a model would receive:

tool_schema.py

from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, ModelResponse, TextPart
from pydantic_ai.models.function import AgentInfo, FunctionModel

agent = Agent()


@agent.tool_plain(docstring_format='google', require_parameter_descriptions=True)
def foobar(a: int, b: str, c: dict[str, list[float]]) -> str:
    """Get me foobar.

    Args:
        a: apple pie
        b: banana cake
        c: carrot smoothie
    """
    return f'{a} {b} {c}'


def print_schema(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
    tool = info.function_tools[0]
    print(tool.description)
    #> Get me foobar.
    print(tool.parameters_json_schema)
    """
    {
        'properties': {
            'a': {'description': 'apple pie', 'title': 'A', 'type': 'integer'},
            'b': {'description': 'banana cake', 'title': 'B', 'type': 'string'},
            'c': {
                'additionalProperties': {'items': {'type': 'number'}, 'type': 'array'},
                'description': 'carrot smoothie',
                'title': 'C',
                'type': 'object',
            },
        },
        'required': ['a', 'b', 'c'],
        'type': 'object',
        'additionalProperties': False,
    }
    """
    return ModelResponse(parts=[TextPart('foobar')])


agent.run_sync('hello', model=FunctionModel(print_schema))
(This example is complete, it can be run "as is")

The return type of tool can be anything which Pydantic can serialize to JSON as some models (e.g. Gemini) support semi-structured return values, some expect text (OpenAI) but seem to be just as good at extracting meaning from the data. If a Python object is returned and the model expects a string, the value will be serialized to JSON.

If a tool has a single parameter that can be represented as an object in JSON schema (e.g. dataclass, TypedDict, pydantic model), the schema for the tool is simplified to be just that object.

Here's an example where we use TestModel.last_model_request_parameters to inspect the tool schema that would be passed to the model.

single_parameter_tool.py

from pydantic import BaseModel

from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel

agent = Agent()


class Foobar(BaseModel):
    """This is a Foobar"""

    x: int
    y: str
    z: float = 3.14


@agent.tool_plain
def foobar(f: Foobar) -> str:
    return str(f)


test_model = TestModel()
result = agent.run_sync('hello', model=test_model)
print(result.data)
#> {"foobar":"x=0 y='a' z=3.14"}
print(test_model.last_model_request_parameters.function_tools)
"""
[
    ToolDefinition(
        name='foobar',
        description='This is a Foobar',
        parameters_json_schema={
            'properties': {
                'x': {'title': 'X', 'type': 'integer'},
                'y': {'title': 'Y', 'type': 'string'},
                'z': {'default': 3.14, 'title': 'Z', 'type': 'number'},
            },
            'required': ['x', 'y'],
            'title': 'Foobar',
            'type': 'object',
        },
        outer_typed_dict_key=None,
    )
]
"""
(This example is complete, it can be run "as is")

Dynamic Function tools
Tools can optionally be defined with another function: prepare, which is called at each step of a run to customize the definition of the tool passed to the model, or omit the tool completely from that step.

A prepare method can be registered via the prepare kwarg to any of the tool registration mechanisms:

@agent.tool decorator
@agent.tool_plain decorator
Tool dataclass
The prepare method, should be of type ToolPrepareFunc, a function which takes RunContext and a pre-built ToolDefinition, and should either return that ToolDefinition with or without modifying it, return a new ToolDefinition, or return None to indicate this tools should not be registered for that step.

Here's a simple prepare method that only includes the tool if the value of the dependency is 42.

As with the previous example, we use TestModel to demonstrate the behavior without calling a real model.

tool_only_if_42.py

from typing import Union

from pydantic_ai import Agent, RunContext
from pydantic_ai.tools import ToolDefinition

agent = Agent('test')


async def only_if_42(
    ctx: RunContext[int], tool_def: ToolDefinition
) -> Union[ToolDefinition, None]:
    if ctx.deps == 42:
        return tool_def


@agent.tool(prepare=only_if_42)
def hitchhiker(ctx: RunContext[int], answer: str) -> str:
    return f'{ctx.deps} {answer}'


result = agent.run_sync('testing...', deps=41)
print(result.data)
#> success (no tool calls)
result = agent.run_sync('testing...', deps=42)
print(result.data)
#> {"hitchhiker":"42 a"}
(This example is complete, it can be run "as is")

Here's a more complex example where we change the description of the name parameter to based on the value of deps

For the sake of variation, we create this tool using the Tool dataclass.

customize_name.py

from __future__ import annotations

from typing import Literal

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.test import TestModel
from pydantic_ai.tools import Tool, ToolDefinition


def greet(name: str) -> str:
    return f'hello {name}'


async def prepare_greet(
    ctx: RunContext[Literal['human', 'machine']], tool_def: ToolDefinition
) -> ToolDefinition | None:
    d = f'Name of the {ctx.deps} to greet.'
    tool_def.parameters_json_schema['properties']['name']['description'] = d
    return tool_def


greet_tool = Tool(greet, prepare=prepare_greet)
test_model = TestModel()
agent = Agent(test_model, tools=[greet_tool], deps_type=Literal['human', 'machine'])

result = agent.run_sync('testing...', deps='human')
print(result.data)
#> {"greet":"hello a"}
print(test_model.last_model_request_parameters.function_tools)
"""
[
    ToolDefinition(
        name='greet',
        description='',
        parameters_json_schema={
            'properties': {
                'name': {
                    'title': 'Name',
                    'type': 'string',
                    'description': 'Name of the human to greet.',
                }
            },
            'required': ['name'],
            'type': 'object',
            'additionalProperties': False,
        },
        outer_typed_dict_key=None,
    )
]
"""
(This example is complete, it can be run "as is")

# Results
Results are the final values returned from running an agent. The result values are wrapped in RunResult and StreamedRunResult so you can access other data like usage of the run and message history

Both RunResult and StreamedRunResult are generic in the data they wrap, so typing information about the data returned by the agent is preserved.

olympics.py

from pydantic import BaseModel

from pydantic_ai import Agent


class CityLocation(BaseModel):
    city: str
    country: str


agent = Agent('google-gla:gemini-1.5-flash', result_type=CityLocation)
result = agent.run_sync('Where were the olympics held in 2012?')
print(result.data)
#> city='London' country='United Kingdom'
print(result.usage())
"""
Usage(requests=1, request_tokens=57, response_tokens=8, total_tokens=65, details=None)
"""
(This example is complete, it can be run "as is")

Runs end when either a plain text response is received or the model calls a tool associated with one of the structured result types. We will add limits to make sure a run doesn't go on indefinitely, see #70.

Result data
When the result type is str, or a union including str, plain text responses are enabled on the model, and the raw text response from the model is used as the response data.

If the result type is a union with multiple members (after remove str from the members), each member is registered as a separate tool with the model in order to reduce the complexity of the tool schemas and maximise the chances a model will respond correctly.

If the result type schema is not of type "object", the result type is wrapped in a single element object, so the schema of all tools registered with the model are object schemas.

Structured results (like tools) use Pydantic to build the JSON schema used for the tool, and to validate the data returned by the model.

Bring on PEP-747

Until PEP-747 "Annotating Type Forms" lands, unions are not valid as types in Python.

When creating the agent we need to # type: ignore the result_type argument, and add a type hint to tell type checkers about the type of the agent.

Here's an example of returning either text or a structured value

box_or_error.py

from typing import Union

from pydantic import BaseModel

from pydantic_ai import Agent


class Box(BaseModel):
    width: int
    height: int
    depth: int
    units: str


agent: Agent[None, Union[Box, str]] = Agent(
    'openai:gpt-4o-mini',
    result_type=Union[Box, str],  # type: ignore
    system_prompt=(
        "Extract me the dimensions of a box, "
        "if you can't extract all data, ask the user to try again."
    ),
)

result = agent.run_sync('The box is 10x20x30')
print(result.data)
#> Please provide the units for the dimensions (e.g., cm, in, m).

result = agent.run_sync('The box is 10x20x30 cm')
print(result.data)
#> width=10 height=20 depth=30 units='cm'
(This example is complete, it can be run "as is")

Here's an example of using a union return type which registered multiple tools, and wraps non-object schemas in an object:

colors_or_sizes.py

from typing import Union

from pydantic_ai import Agent

agent: Agent[None, Union[list[str], list[int]]] = Agent(
    'openai:gpt-4o-mini',
    result_type=Union[list[str], list[int]],  # type: ignore
    system_prompt='Extract either colors or sizes from the shapes provided.',
)

result = agent.run_sync('red square, blue circle, green triangle')
print(result.data)
#> ['red', 'blue', 'green']

result = agent.run_sync('square size 10, circle size 20, triangle size 30')
print(result.data)
#> [10, 20, 30]
(This example is complete, it can be run "as is")

Result validators functions
Some validation is inconvenient or impossible to do in Pydantic validators, in particular when the validation requires IO and is asynchronous. PydanticAI provides a way to add validation functions via the agent.result_validator decorator.

Here's a simplified variant of the SQL Generation example:

sql_gen.py

from typing import Union

from fake_database import DatabaseConn, QueryError
from pydantic import BaseModel

from pydantic_ai import Agent, RunContext, ModelRetry


class Success(BaseModel):
    sql_query: str


class InvalidRequest(BaseModel):
    error_message: str


Response = Union[Success, InvalidRequest]
agent: Agent[DatabaseConn, Response] = Agent(
    'google-gla:gemini-1.5-flash',
    result_type=Response,  # type: ignore
    deps_type=DatabaseConn,
    system_prompt='Generate PostgreSQL flavored SQL queries based on user input.',
)


@agent.result_validator
async def validate_result(ctx: RunContext[DatabaseConn], result: Response) -> Response:
    if isinstance(result, InvalidRequest):
        return result
    try:
        await ctx.deps.execute(f'EXPLAIN {result.sql_query}')
    except QueryError as e:
        raise ModelRetry(f'Invalid query: {e}') from e
    else:
        return result


result = agent.run_sync(
    'get me users who were last active yesterday.', deps=DatabaseConn()
)
print(result.data)
#> sql_query='SELECT * FROM users WHERE last_active::date = today() - interval 1 day'
(This example is complete, it can be run "as is")

Streamed Results
There two main challenges with streamed results:

Validating structured responses before they're complete, this is achieved by "partial validation" which was recently added to Pydantic in pydantic/pydantic#10748.
When receiving a response, we don't know if it's the final response without starting to stream it and peeking at the content. PydanticAI streams just enough of the response to sniff out if it's a tool call or a result, then streams the whole thing and calls tools, or returns the stream as a StreamedRunResult.
Streaming Text
Example of streamed text result:

streamed_hello_world.py

from pydantic_ai import Agent

agent = Agent('google-gla:gemini-1.5-flash')  


async def main():
    async with agent.run_stream('Where does "hello world" come from?') as result:  
        async for message in result.stream_text():  
            print(message)
            #> The first known
            #> The first known use of "hello,
            #> The first known use of "hello, world" was in
            #> The first known use of "hello, world" was in a 1974 textbook
            #> The first known use of "hello, world" was in a 1974 textbook about the C
            #> The first known use of "hello, world" was in a 1974 textbook about the C programming language.
(This example is complete, it can be run "as is" — you'll need to add asyncio.run(main()) to run main)

We can also stream text as deltas rather than the entire text in each item:

streamed_delta_hello_world.py

from pydantic_ai import Agent

agent = Agent('google-gla:gemini-1.5-flash')


async def main():
    async with agent.run_stream('Where does "hello world" come from?') as result:
        async for message in result.stream_text(delta=True):  
            print(message)
            #> The first known
            #> use of "hello,
            #> world" was in
            #> a 1974 textbook
            #> about the C
            #> programming language.
(This example is complete, it can be run "as is" — you'll need to add asyncio.run(main()) to run main)

Result message not included in messages

The final result message will NOT be added to result messages if you use .stream_text(delta=True), see Messages and chat history for more information.

Streaming Structured Responses
Not all types are supported with partial validation in Pydantic, see pydantic/pydantic#10748, generally for model-like structures it's currently best to use TypeDict.

Here's an example of streaming a use profile as it's built:

streamed_user_profile.py

from datetime import date

from typing_extensions import TypedDict

from pydantic_ai import Agent


class UserProfile(TypedDict, total=False):
    name: str
    dob: date
    bio: str


agent = Agent(
    'openai:gpt-4o',
    result_type=UserProfile,
    system_prompt='Extract a user profile from the input',
)


async def main():
    user_input = 'My name is Ben, I was born on January 28th 1990, I like the chain the dog and the pyramid.'
    async with agent.run_stream(user_input) as result:
        async for profile in result.stream():
            print(profile)
            #> {'name': 'Ben'}
            #> {'name': 'Ben'}
            #> {'name': 'Ben', 'dob': date(1990, 1, 28), 'bio': 'Likes'}
            #> {'name': 'Ben', 'dob': date(1990, 1, 28), 'bio': 'Likes the chain the '}
            #> {'name': 'Ben', 'dob': date(1990, 1, 28), 'bio': 'Likes the chain the dog and the pyr'}
            #> {'name': 'Ben', 'dob': date(1990, 1, 28), 'bio': 'Likes the chain the dog and the pyramid'}
            #> {'name': 'Ben', 'dob': date(1990, 1, 28), 'bio': 'Likes the chain the dog and the pyramid'}
(This example is complete, it can be run "as is" — you'll need to add asyncio.run(main()) to run main)

If you want fine-grained control of validation, particularly catching validation errors, you can use the following pattern:

streamed_user_profile.py

from datetime import date

from pydantic import ValidationError
from typing_extensions import TypedDict

from pydantic_ai import Agent


class UserProfile(TypedDict, total=False):
    name: str
    dob: date
    bio: str


agent = Agent('openai:gpt-4o', result_type=UserProfile)


async def main():
    user_input = 'My name is Ben, I was born on January 28th 1990, I like the chain the dog and the pyramid.'
    async with agent.run_stream(user_input) as result:
        async for message, last in result.stream_structured(debounce_by=0.01):  
            try:
                profile = await result.validate_structured_result(  
                    message,
                    allow_partial=not last,
                )
            except ValidationError:
                continue
            print(profile)
            #> {'name': 'Ben'}
            #> {'name': 'Ben'}
            #> {'name': 'Ben', 'dob': date(1990, 1, 28), 'bio': 'Likes'}
            #> {'name': 'Ben', 'dob': date(1990, 1, 28), 'bio': 'Likes the chain the '}
            #> {'name': 'Ben', 'dob': date(1990, 1, 28), 'bio': 'Likes the chain the dog and the pyr'}
            #> {'name': 'Ben', 'dob': date(1990, 1, 28), 'bio': 'Likes the chain the dog and the pyramid'}
            #> {'name': 'Ben', 'dob': date(1990, 1, 28), 'bio': 'Likes the chain the dog and the pyramid'}
(This example is complete, it can be run "as is" — you'll need to add asyncio.run(main()) to run main)

Examples
The following examples demonstrate how to use streamed responses in PydanticAI:

Stream markdown
Stream Whales

# Messages and chat history
PydanticAI provides access to messages exchanged during an agent run. These messages can be used both to continue a coherent conversation, and to understand how an agent performed.

Accessing Messages from Results
After running an agent, you can access the messages exchanged during that run from the result object.

Both RunResult (returned by Agent.run, Agent.run_sync) and StreamedRunResult (returned by Agent.run_stream) have the following methods:

all_messages(): returns all messages, including messages from prior runs. There's also a variant that returns JSON bytes, all_messages_json().
new_messages(): returns only the messages from the current run. There's also a variant that returns JSON bytes, new_messages_json().
StreamedRunResult and complete messages

On StreamedRunResult, the messages returned from these methods will only include the final result message once the stream has finished.

E.g. you've awaited one of the following coroutines:

StreamedRunResult.stream()
StreamedRunResult.stream_text()
StreamedRunResult.stream_structured()
StreamedRunResult.get_data()
Note: The final result message will NOT be added to result messages if you use .stream_text(delta=True) since in this case the result content is never built as one string.

Example of accessing methods on a RunResult :

run_result_messages.py

from pydantic_ai import Agent

agent = Agent('openai:gpt-4o', system_prompt='Be a helpful assistant.')

result = agent.run_sync('Tell me a joke.')
print(result.data)
#> Did you hear about the toothpaste scandal? They called it Colgate.

# all messages from the run
print(result.all_messages())
"""
[
    ModelRequest(
        parts=[
            SystemPromptPart(
                content='Be a helpful assistant.',
                dynamic_ref=None,
                part_kind='system-prompt',
            ),
            UserPromptPart(
                content='Tell me a joke.',
                timestamp=datetime.datetime(...),
                part_kind='user-prompt',
            ),
        ],
        kind='request',
    ),
    ModelResponse(
        parts=[
            TextPart(
                content='Did you hear about the toothpaste scandal? They called it Colgate.',
                part_kind='text',
            )
        ],
        model_name='function:model_logic',
        timestamp=datetime.datetime(...),
        kind='response',
    ),
]
"""
(This example is complete, it can be run "as is")
Example of accessing methods on a StreamedRunResult :

streamed_run_result_messages.py

from pydantic_ai import Agent

agent = Agent('openai:gpt-4o', system_prompt='Be a helpful assistant.')


async def main():
    async with agent.run_stream('Tell me a joke.') as result:
        # incomplete messages before the stream finishes
        print(result.all_messages())
        """
        [
            ModelRequest(
                parts=[
                    SystemPromptPart(
                        content='Be a helpful assistant.',
                        dynamic_ref=None,
                        part_kind='system-prompt',
                    ),
                    UserPromptPart(
                        content='Tell me a joke.',
                        timestamp=datetime.datetime(...),
                        part_kind='user-prompt',
                    ),
                ],
                kind='request',
            )
        ]
        """

        async for text in result.stream_text():
            print(text)
            #> Did you hear
            #> Did you hear about the toothpaste
            #> Did you hear about the toothpaste scandal? They called
            #> Did you hear about the toothpaste scandal? They called it Colgate.

        # complete messages once the stream finishes
        print(result.all_messages())
        """
        [
            ModelRequest(
                parts=[
                    SystemPromptPart(
                        content='Be a helpful assistant.',
                        dynamic_ref=None,
                        part_kind='system-prompt',
                    ),
                    UserPromptPart(
                        content='Tell me a joke.',
                        timestamp=datetime.datetime(...),
                        part_kind='user-prompt',
                    ),
                ],
                kind='request',
            ),
            ModelResponse(
                parts=[
                    TextPart(
                        content='Did you hear about the toothpaste scandal? They called it Colgate.',
                        part_kind='text',
                    )
                ],
                model_name='function:stream_model_logic',
                timestamp=datetime.datetime(...),
                kind='response',
            ),
        ]
        """
(This example is complete, it can be run "as is" — you'll need to add asyncio.run(main()) to run main)
Using Messages as Input for Further Agent Runs
The primary use of message histories in PydanticAI is to maintain context across multiple agent runs.

To use existing messages in a run, pass them to the message_history parameter of Agent.run, Agent.run_sync or Agent.run_stream.

If message_history is set and not empty, a new system prompt is not generated — we assume the existing message history includes a system prompt.

Reusing messages in a conversation

from pydantic_ai import Agent

agent = Agent('openai:gpt-4o', system_prompt='Be a helpful assistant.')

result1 = agent.run_sync('Tell me a joke.')
print(result1.data)
#> Did you hear about the toothpaste scandal? They called it Colgate.

result2 = agent.run_sync('Explain?', message_history=result1.new_messages())
print(result2.data)
#> This is an excellent joke invented by Samuel Colvin, it needs no explanation.

print(result2.all_messages())
"""
[
    ModelRequest(
        parts=[
            SystemPromptPart(
                content='Be a helpful assistant.',
                dynamic_ref=None,
                part_kind='system-prompt',
            ),
            UserPromptPart(
                content='Tell me a joke.',
                timestamp=datetime.datetime(...),
                part_kind='user-prompt',
            ),
        ],
        kind='request',
    ),
    ModelResponse(
        parts=[
            TextPart(
                content='Did you hear about the toothpaste scandal? They called it Colgate.',
                part_kind='text',
            )
        ],
        model_name='function:model_logic',
        timestamp=datetime.datetime(...),
        kind='response',
    ),
    ModelRequest(
        parts=[
            UserPromptPart(
                content='Explain?',
                timestamp=datetime.datetime(...),
                part_kind='user-prompt',
            )
        ],
        kind='request',
    ),
    ModelResponse(
        parts=[
            TextPart(
                content='This is an excellent joke invented by Samuel Colvin, it needs no explanation.',
                part_kind='text',
            )
        ],
        model_name='function:model_logic',
        timestamp=datetime.datetime(...),
        kind='response',
    ),
]
"""
(This example is complete, it can be run "as is")
Other ways of using messages
Since messages are defined by simple dataclasses, you can manually create and manipulate, e.g. for testing.

The message format is independent of the model used, so you can use messages in different agents, or the same agent with different models.

In the example below, we reuse the message from the first agent run, which uses the openai:gpt-4o model, in a second agent run using the google-gla:gemini-1.5-pro model.

Reusing messages with a different model

from pydantic_ai import Agent

agent = Agent('openai:gpt-4o', system_prompt='Be a helpful assistant.')

result1 = agent.run_sync('Tell me a joke.')
print(result1.data)
#> Did you hear about the toothpaste scandal? They called it Colgate.

result2 = agent.run_sync(
    'Explain?',
    model='google-gla:gemini-1.5-pro',
    message_history=result1.new_messages(),
)
print(result2.data)
#> This is an excellent joke invented by Samuel Colvin, it needs no explanation.

print(result2.all_messages())
"""
[
    ModelRequest(
        parts=[
            SystemPromptPart(
                content='Be a helpful assistant.',
                dynamic_ref=None,
                part_kind='system-prompt',
            ),
            UserPromptPart(
                content='Tell me a joke.',
                timestamp=datetime.datetime(...),
                part_kind='user-prompt',
            ),
        ],
        kind='request',
    ),
    ModelResponse(
        parts=[
            TextPart(
                content='Did you hear about the toothpaste scandal? They called it Colgate.',
                part_kind='text',
            )
        ],
        model_name='function:model_logic',
        timestamp=datetime.datetime(...),
        kind='response',
    ),
    ModelRequest(
        parts=[
            UserPromptPart(
                content='Explain?',
                timestamp=datetime.datetime(...),
                part_kind='user-prompt',
            )
        ],
        kind='request',
    ),
    ModelResponse(
        parts=[
            TextPart(
                content='This is an excellent joke invented by Samuel Colvin, it needs no explanation.',
                part_kind='text',
            )
        ],
        model_name='function:model_logic',
        timestamp=datetime.datetime(...),
        kind='response',
    ),
]
"""
Examples
For a more complete example of using messages in conversations, see the chat app example.

# Multi-agent Applications
There are roughly four levels of complexity when building applications with PydanticAI:

Single agent workflows — what most of the pydantic_ai documentation covers
Agent delegation — agents using another agent via tools
Programmatic agent hand-off — one agent runs, then application code calls another agent
Graph based control flow — for the most complex cases, a graph-based state machine can be used to control the execution of multiple agents
Of course, you can combine multiple strategies in a single application.

Agent delegation
"Agent delegation" refers to the scenario where an agent delegates work to another agent, then takes back control when the delegate agent (the agent called from within a tool) finishes.

Since agents are stateless and designed to be global, you do not need to include the agent itself in agent dependencies.

You'll generally want to pass ctx.usage to the usage keyword argument of the delegate agent run so usage within that run counts towards the total usage of the parent agent run.

Multiple models

Agent delegation doesn't need to use the same model for each agent. If you choose to use different models within a run, calculating the monetary cost from the final result.usage() of the run will not be possible, but you can still use UsageLimits to avoid unexpected costs.

agent_delegation_simple.py

from pydantic_ai import Agent, RunContext
from pydantic_ai.usage import UsageLimits

joke_selection_agent = Agent(  
    'openai:gpt-4o',
    system_prompt=(
        'Use the `joke_factory` to generate some jokes, then choose the best. '
        'You must return just a single joke.'
    ),
)
joke_generation_agent = Agent(  
    'google-gla:gemini-1.5-flash', result_type=list[str]
)


@joke_selection_agent.tool
async def joke_factory(ctx: RunContext[None], count: int) -> list[str]:
    r = await joke_generation_agent.run(  
        f'Please generate {count} jokes.',
        usage=ctx.usage,  
    )
    return r.data  


result = joke_selection_agent.run_sync(
    'Tell me a joke.',
    usage_limits=UsageLimits(request_limit=5, total_tokens_limit=300),
)
print(result.data)
#> Did you hear about the toothpaste scandal? They called it Colgate.
print(result.usage())
"""
Usage(
    requests=3, request_tokens=204, response_tokens=24, total_tokens=228, details=None
)
"""
(This example is complete, it can be run "as is")

The control flow for this example is pretty simple and can be summarised as follows:

START
joke_selection_agent
joke_factory (tool)
joke_generation_agent
END
Agent delegation and dependencies
Generally the delegate agent needs to either have the same dependencies as the calling agent, or dependencies which are a subset of the calling agent's dependencies.

Initializing dependencies

We say "generally" above since there's nothing to stop you initializing dependencies within a tool call and therefore using interdependencies in a delegate agent that are not available on the parent, this should often be avoided since it can be significantly slower than reusing connections etc. from the parent agent.

agent_delegation_deps.py

from dataclasses import dataclass

import httpx

from pydantic_ai import Agent, RunContext


@dataclass
class ClientAndKey:  
    http_client: httpx.AsyncClient
    api_key: str


joke_selection_agent = Agent(
    'openai:gpt-4o',
    deps_type=ClientAndKey,  
    system_prompt=(
        'Use the `joke_factory` tool to generate some jokes on the given subject, '
        'then choose the best. You must return just a single joke.'
    ),
)
joke_generation_agent = Agent(
    'gemini-1.5-flash',
    deps_type=ClientAndKey,  
    result_type=list[str],
    system_prompt=(
        'Use the "get_jokes" tool to get some jokes on the given subject, '
        'then extract each joke into a list.'
    ),
)


@joke_selection_agent.tool
async def joke_factory(ctx: RunContext[ClientAndKey], count: int) -> list[str]:
    r = await joke_generation_agent.run(
        f'Please generate {count} jokes.',
        deps=ctx.deps,  
        usage=ctx.usage,
    )
    return r.data


@joke_generation_agent.tool  
async def get_jokes(ctx: RunContext[ClientAndKey], count: int) -> str:
    response = await ctx.deps.http_client.get(
        'https://example.com',
        params={'count': count},
        headers={'Authorization': f'Bearer {ctx.deps.api_key}'},
    )
    response.raise_for_status()
    return response.text


async def main():
    async with httpx.AsyncClient() as client:
        deps = ClientAndKey(client, 'foobar')
        result = await joke_selection_agent.run('Tell me a joke.', deps=deps)
        print(result.data)
        #> Did you hear about the toothpaste scandal? They called it Colgate.
        print(result.usage())  
        """
        Usage(
            requests=4,
            request_tokens=309,
            response_tokens=32,
            total_tokens=341,
            details=None,
        )
        """
(This example is complete, it can be run "as is" — you'll need to add asyncio.run(main()) to run main)

This example shows how even a fairly simple agent delegation can lead to a complex control flow:

START
joke_selection_agent
joke_factory (tool)
joke_generation_agent
get_jokes (tool)
HTTP request
END
Programmatic agent hand-off
"Programmatic agent hand-off" refers to the scenario where multiple agents are called in succession, with application code and/or a human in the loop responsible for deciding which agent to call next.

Here agents don't need to use the same deps.

Here we show two agents used in succession, the first to find a flight and the second to extract the user's seat preference.

programmatic_handoff.py

from typing import Literal, Union

from pydantic import BaseModel, Field
from rich.prompt import Prompt

from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import ModelMessage
from pydantic_ai.usage import Usage, UsageLimits


class FlightDetails(BaseModel):
    flight_number: str


class Failed(BaseModel):
    """Unable to find a satisfactory choice."""


flight_search_agent = Agent[None, Union[FlightDetails, Failed]](  
    'openai:gpt-4o',
    result_type=Union[FlightDetails, Failed],  # type: ignore
    system_prompt=(
        'Use the "flight_search" tool to find a flight '
        'from the given origin to the given destination.'
    ),
)


@flight_search_agent.tool  
async def flight_search(
    ctx: RunContext[None], origin: str, destination: str
) -> Union[FlightDetails, None]:
    # in reality, this would call a flight search API or
    # use a browser to scrape a flight search website
    return FlightDetails(flight_number='AK456')


usage_limits = UsageLimits(request_limit=15)  


async def find_flight(usage: Usage) -> Union[FlightDetails, None]:  
    message_history: Union[list[ModelMessage], None] = None
    for _ in range(3):
        prompt = Prompt.ask(
            'Where would you like to fly from and to?',
        )
        result = await flight_search_agent.run(
            prompt,
            message_history=message_history,
            usage=usage,
            usage_limits=usage_limits,
        )
        if isinstance(result.data, FlightDetails):
            return result.data
        else:
            message_history = result.all_messages(
                result_tool_return_content='Please try again.'
            )


class SeatPreference(BaseModel):
    row: int = Field(ge=1, le=30)
    seat: Literal['A', 'B', 'C', 'D', 'E', 'F']


# This agent is responsible for extracting the user's seat selection
seat_preference_agent = Agent[None, Union[SeatPreference, Failed]](  
    'openai:gpt-4o',
    result_type=Union[SeatPreference, Failed],  # type: ignore
    system_prompt=(
        "Extract the user's seat preference. "
        'Seats A and F are window seats. '
        'Row 1 is the front row and has extra leg room. '
        'Rows 14, and 20 also have extra leg room. '
    ),
)


async def find_seat(usage: Usage) -> SeatPreference:  
    message_history: Union[list[ModelMessage], None] = None
    while True:
        answer = Prompt.ask('What seat would you like?')

        result = await seat_preference_agent.run(
            answer,
            message_history=message_history,
            usage=usage,
            usage_limits=usage_limits,
        )
        if isinstance(result.data, SeatPreference):
            return result.data
        else:
            print('Could not understand seat preference. Please try again.')
            message_history = result.all_messages()


async def main():  
    usage: Usage = Usage()

    opt_flight_details = await find_flight(usage)
    if opt_flight_details is not None:
        print(f'Flight found: {opt_flight_details.flight_number}')
        #> Flight found: AK456
        seat_preference = await find_seat(usage)
        print(f'Seat preference: {seat_preference}')
        #> Seat preference: row=1 seat='A'
(This example is complete, it can be run "as is" — you'll need to add asyncio.run(main()) to run main)

The control flow for this example can be summarised as follows:

find_seat
find_flight
ask user for seat
seat_preference_agent
ask user for flight
flight_search_agent
START
END
Pydantic Graphs
See the graph documentation on when and how to use graphs.


 # Graphs
Don't use a nail gun unless you need a nail gun

If PydanticAI agents are a hammer, and multi-agent workflows are a sledgehammer, then graphs are a nail gun:

sure, nail guns look cooler than hammers
but nail guns take a lot more setup than hammers
and nail guns don't make you a better builder, they make you a builder with a nail gun
Lastly, (and at the risk of torturing this metaphor), if you're a fan of medieval tools like mallets and untyped Python, you probably won't like nail guns or our approach to graphs. (But then again, if you're not a fan of type hints in Python, you've probably already bounced off PydanticAI to use one of the toy agent frameworks — good luck, and feel free to borrow my sledgehammer when you realize you need it)
In short, graphs are a powerful tool, but they're not the right tool for every job. Please consider other multi-agent approaches before proceeding.

If you're not confident a graph-based approach is a good idea, it might be unnecessary.

Graphs and finite state machines (FSMs) are a powerful abstraction to model, execute, control and visualize complex workflows.

Alongside PydanticAI, we've developed pydantic-graph — an async graph and state machine library for Python where nodes and edges are defined using type hints.

While this library is developed as part of PydanticAI; it has no dependency on pydantic-ai and can be considered as a pure graph-based state machine library. You may find it useful whether or not you're using PydanticAI or even building with GenAI.

pydantic-graph is designed for advanced users and makes heavy use of Python generics and types hints. It is not designed to be as beginner-friendly as PydanticAI.

Very Early beta

Graph support was introduced in v0.0.19 and is in very earlier beta. The API is subject to change. The documentation is incomplete. The implementation is incomplete.

Installation
pydantic-graph is a required dependency of pydantic-ai, and an optional dependency of pydantic-ai-slim, see installation instructions for more information. You can also install it directly:


pip
uv

pip install pydantic-graph

Graph Types
pydantic-graph made up of a few key components:

GraphRunContext
GraphRunContext — The context for the graph run, similar to PydanticAI's RunContext. This holds the state of the graph and dependencies and is passed to nodes when they're run.

GraphRunContext is generic in the state type of the graph it's used in, StateT.

End
End — return value to indicate the graph run should end.

End is generic in the graph return type of the graph it's used in, RunEndT.

Nodes
Subclasses of BaseNode define nodes for execution in the graph.

Nodes, which are generally dataclasses, generally consist of:

fields containing any parameters required/optional when calling the node
the business logic to execute the node, in the run method
return annotations of the run method, which are read by pydantic-graph to determine the outgoing edges of the node
Nodes are generic in:

state, which must have the same type as the state of graphs they're included in, StateT has a default of None, so if you're not using state you can omit this generic parameter, see stateful graphs for more information
deps, which must have the same type as the deps of the graph they're included in, DepsT has a default of None, so if you're not using deps you can omit this generic parameter, see dependency injection for more information
graph return type — this only applies if the node returns End. RunEndT has a default of Never so this generic parameter can be omitted if the node doesn't return End, but must be included if it does.
Here's an example of a start or intermediate node in a graph — it can't end the run as it doesn't return End:

intermediate_node.py

from dataclasses import dataclass

from pydantic_graph import BaseNode, GraphRunContext


@dataclass
class MyNode(BaseNode[MyState]):  
    foo: int  

    async def run(
        self,
        ctx: GraphRunContext[MyState],  
    ) -> AnotherNode:  
        ...
        return AnotherNode()
We could extend MyNode to optionally end the run if foo is divisible by 5:

intermediate_or_end_node.py

from dataclasses import dataclass

from pydantic_graph import BaseNode, End, GraphRunContext


@dataclass
class MyNode(BaseNode[MyState, None, int]):  
    foo: int

    async def run(
        self,
        ctx: GraphRunContext[MyState],
    ) -> AnotherNode | End[int]:  
        if self.foo % 5 == 0:
            return End(self.foo)
        else:
            return AnotherNode()
Graph
Graph — this is the execution graph itself, made up of a set of node classes (i.e., BaseNode subclasses).

Graph is generic in:

state the state type of the graph, StateT
deps the deps type of the graph, DepsT
graph return type the return type of the graph run, RunEndT
Here's an example of a simple graph:

graph_example.py

from __future__ import annotations

from dataclasses import dataclass

from pydantic_graph import BaseNode, End, Graph, GraphRunContext


@dataclass
class DivisibleBy5(BaseNode[None, None, int]):  
    foo: int

    async def run(
        self,
        ctx: GraphRunContext,
    ) -> Increment | End[int]:
        if self.foo % 5 == 0:
            return End(self.foo)
        else:
            return Increment(self.foo)


@dataclass
class Increment(BaseNode):  
    foo: int

    async def run(self, ctx: GraphRunContext) -> DivisibleBy5:
        return DivisibleBy5(self.foo + 1)


fives_graph = Graph(nodes=[DivisibleBy5, Increment])  
result, history = fives_graph.run_sync(DivisibleBy5(4))  
print(result)
#> 5
# the full history is quite verbose (see below), so we'll just print the summary
print([item.data_snapshot() for item in history])
#> [DivisibleBy5(foo=4), Increment(foo=4), DivisibleBy5(foo=5), End(data=5)]
(This example is complete, it can be run "as is" with Python 3.10+)

A mermaid diagram for this graph can be generated with the following code:

graph_example_diagram.py

from graph_example import DivisibleBy5, fives_graph

fives_graph.mermaid_code(start_node=DivisibleBy5)
DivisibleBy5
Increment
fives_graph
In order to visualize a graph within a jupyter-notebook, IPython.display needs to be used:

jupyter_display_mermaid.py

from graph_example import DivisibleBy5, fives_graph
from IPython.display import Image, display

display(Image(fives_graph.mermaid_image(start_node=DivisibleBy5)))
Stateful Graphs
The "state" concept in pydantic-graph provides an optional way to access and mutate an object (often a dataclass or Pydantic model) as nodes run in a graph. If you think of Graphs as a production line, then your state is the engine being passed along the line and built up by each node as the graph is run.

In the future, we intend to extend pydantic-graph to provide state persistence with the state recorded after each node is run, see #695.

Here's an example of a graph which represents a vending machine where the user may insert coins and select a product to purchase.

vending_machine.py

from __future__ import annotations

from dataclasses import dataclass

from rich.prompt import Prompt

from pydantic_graph import BaseNode, End, Graph, GraphRunContext


@dataclass
class MachineState:  
    user_balance: float = 0.0
    product: str | None = None


@dataclass
class InsertCoin(BaseNode[MachineState]):  
    async def run(self, ctx: GraphRunContext[MachineState]) -> CoinsInserted:  
        return CoinsInserted(float(Prompt.ask('Insert coins')))  


@dataclass
class CoinsInserted(BaseNode[MachineState]):
    amount: float  

    async def run(
        self, ctx: GraphRunContext[MachineState]
    ) -> SelectProduct | Purchase:  
        ctx.state.user_balance += self.amount  
        if ctx.state.product is not None:  
            return Purchase(ctx.state.product)
        else:
            return SelectProduct()


@dataclass
class SelectProduct(BaseNode[MachineState]):
    async def run(self, ctx: GraphRunContext[MachineState]) -> Purchase:
        return Purchase(Prompt.ask('Select product'))


PRODUCT_PRICES = {  
    'water': 1.25,
    'soda': 1.50,
    'crisps': 1.75,
    'chocolate': 2.00,
}


@dataclass
class Purchase(BaseNode[MachineState, None, None]):  
    product: str

    async def run(
        self, ctx: GraphRunContext[MachineState]
    ) -> End | InsertCoin | SelectProduct:
        if price := PRODUCT_PRICES.get(self.product):  
            ctx.state.product = self.product  
            if ctx.state.user_balance >= price:  
                ctx.state.user_balance -= price
                return End(None)
            else:
                diff = price - ctx.state.user_balance
                print(f'Not enough money for {self.product}, need {diff:0.2f} more')
                #> Not enough money for crisps, need 0.75 more
                return InsertCoin()  
        else:
            print(f'No such product: {self.product}, try again')
            return SelectProduct()  


vending_machine_graph = Graph(  
    nodes=[InsertCoin, CoinsInserted, SelectProduct, Purchase]
)


async def main():
    state = MachineState()  
    await vending_machine_graph.run(InsertCoin(), state=state)  
    print(f'purchase successful item={state.product} change={state.user_balance:0.2f}')
    #> purchase successful item=crisps change=0.25
(This example is complete, it can be run "as is" with Python 3.10+ — you'll need to add asyncio.run(main()) to run main)

A mermaid diagram for this graph can be generated with the following code:

vending_machine_diagram.py

from vending_machine import InsertCoin, vending_machine_graph

vending_machine_graph.mermaid_code(start_node=InsertCoin)
The diagram generated by the above code is:

InsertCoin
CoinsInserted
SelectProduct
Purchase
vending_machine_graph
See below for more information on generating diagrams.

GenAI Example
So far we haven't shown an example of a Graph that actually uses PydanticAI or GenAI at all.

In this example, one agent generates a welcome email to a user and the other agent provides feedback on the email.

This graph has a very simple structure:

WriteEmail
Feedback
feedback_graph
genai_email_feedback.py

from __future__ import annotations as _annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, EmailStr

from pydantic_ai import Agent
from pydantic_ai.format_as_xml import format_as_xml
from pydantic_ai.messages import ModelMessage
from pydantic_graph import BaseNode, End, Graph, GraphRunContext


@dataclass
class User:
    name: str
    email: EmailStr
    interests: list[str]


@dataclass
class Email:
    subject: str
    body: str


@dataclass
class State:
    user: User
    write_agent_messages: list[ModelMessage] = field(default_factory=list)


email_writer_agent = Agent(
    'google-vertex:gemini-1.5-pro',
    result_type=Email,
    system_prompt='Write a welcome email to our tech blog.',
)


@dataclass
class WriteEmail(BaseNode[State]):
    email_feedback: str | None = None

    async def run(self, ctx: GraphRunContext[State]) -> Feedback:
        if self.email_feedback:
            prompt = (
                f'Rewrite the email for the user:\n'
                f'{format_as_xml(ctx.state.user)}\n'
                f'Feedback: {self.email_feedback}'
            )
        else:
            prompt = (
                f'Write a welcome email for the user:\n'
                f'{format_as_xml(ctx.state.user)}'
            )

        result = await email_writer_agent.run(
            prompt,
            message_history=ctx.state.write_agent_messages,
        )
        ctx.state.write_agent_messages += result.all_messages()
        return Feedback(result.data)


class EmailRequiresWrite(BaseModel):
    feedback: str


class EmailOk(BaseModel):
    pass


feedback_agent = Agent[None, EmailRequiresWrite | EmailOk](
    'openai:gpt-4o',
    result_type=EmailRequiresWrite | EmailOk,  # type: ignore
    system_prompt=(
        'Review the email and provide feedback, email must reference the users specific interests.'
    ),
)


@dataclass
class Feedback(BaseNode[State, None, Email]):
    email: Email

    async def run(
        self,
        ctx: GraphRunContext[State],
    ) -> WriteEmail | End[Email]:
        prompt = format_as_xml({'user': ctx.state.user, 'email': self.email})
        result = await feedback_agent.run(prompt)
        if isinstance(result.data, EmailRequiresWrite):
            return WriteEmail(email_feedback=result.data.feedback)
        else:
            return End(self.email)


async def main():
    user = User(
        name='John Doe',
        email='john.joe@example.com',
        interests=['Haskel', 'Lisp', 'Fortran'],
    )
    state = State(user)
    feedback_graph = Graph(nodes=(WriteEmail, Feedback))
    email, _ = await feedback_graph.run(WriteEmail(), state=state)
    print(email)
    """
    Email(
        subject='Welcome to our tech blog!',
        body='Hello John, Welcome to our tech blog! ...',
    )
    """
(This example is complete, it can be run "as is" with Python 3.10+ — you'll need to add asyncio.run(main()) to run main)

Custom Control Flow
In many real-world applications, Graphs cannot run uninterrupted from start to finish — they might require external input, or run over an extended period of time such that a single process cannot execute the entire graph run from start to finish without interruption.

In these scenarios the next method can be used to run the graph one node at a time.

In this example, an AI asks the user a question, the user provides an answer, the AI evaluates the answer and ends if the user got it right or asks another question if they got it wrong.

ai_q_and_a_graph.py — question_graph definition
ai_q_and_a_run.py

from rich.prompt import Prompt

from pydantic_graph import End, HistoryStep

from ai_q_and_a_graph import Ask, question_graph, QuestionState, Answer


async def main():
    state = QuestionState()  
    node = Ask()  
    history: list[HistoryStep[QuestionState]] = []  
    while True:
        node = await question_graph.next(node, history, state=state)  
        if isinstance(node, Answer):
            node.answer = Prompt.ask(node.question)  
        elif isinstance(node, End):  
            print(f'Correct answer! {node.data}')
            #> Correct answer! Well done, 1 + 1 = 2
            print([e.data_snapshot() for e in history])
            """
            [
                Ask(),
                Answer(question='What is the capital of France?', answer='Vichy'),
                Evaluate(answer='Vichy'),
                Reprimand(comment='Vichy is no longer the capital of France.'),
                Ask(),
                Answer(question='what is 1 + 1?', answer='2'),
                Evaluate(answer='2'),
            ]
            """
            return
        # otherwise just continue
(This example is complete, it can be run "as is" with Python 3.10+ — you'll need to add asyncio.run(main()) to run main)

A mermaid diagram for this graph can be generated with the following code:

ai_q_and_a_diagram.py

from ai_q_and_a_graph import Ask, question_graph

question_graph.mermaid_code(start_node=Ask)
Ask
Answer
Evaluate
Reprimand
question_graph
You maybe have noticed that although this examples transfers control flow out of the graph run, we're still using rich's Prompt.ask to get user input, with the process hanging while we wait for the user to enter a response. For an example of genuine out-of-process control flow, see the question graph example.

Dependency Injection
As with PydanticAI, pydantic-graph supports dependency injection via a generic parameter on Graph and BaseNode, and the GraphRunContext.deps fields.

As an example of dependency injection, let's modify the DivisibleBy5 example above to use a ProcessPoolExecutor to run the compute load in a separate process (this is a contrived example, ProcessPoolExecutor wouldn't actually improve performance in this example):

deps_example.py

from __future__ import annotations

import asyncio
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

from pydantic_graph import BaseNode, End, Graph, GraphRunContext


@dataclass
class GraphDeps:
    executor: ProcessPoolExecutor


@dataclass
class DivisibleBy5(BaseNode[None, None, int]):
    foo: int

    async def run(
        self,
        ctx: GraphRunContext,
    ) -> Increment | End[int]:
        if self.foo % 5 == 0:
            return End(self.foo)
        else:
            return Increment(self.foo)


@dataclass
class Increment(BaseNode):
    foo: int

    async def run(self, ctx: GraphRunContext) -> DivisibleBy5:
        loop = asyncio.get_running_loop()
        compute_result = await loop.run_in_executor(
            ctx.deps.executor,
            self.compute,
        )
        return DivisibleBy5(compute_result)

    def compute(self) -> int:
        return self.foo + 1


fives_graph = Graph(nodes=[DivisibleBy5, Increment])


async def main():
    with ProcessPoolExecutor() as executor:
        deps = GraphDeps(executor)
        result, history = await fives_graph.run(DivisibleBy5(3), deps=deps)
    print(result)
    #> 5
    # the full history is quite verbose (see below), so we'll just print the summary
    print([item.data_snapshot() for item in history])
    """
    [
        DivisibleBy5(foo=3),
        Increment(foo=3),
        DivisibleBy5(foo=4),
        Increment(foo=4),
        DivisibleBy5(foo=5),
        End(data=5),
    ]
    """
(This example is complete, it can be run "as is" with Python 3.10+ — you'll need to add asyncio.run(main()) to run main)

Mermaid Diagrams
Pydantic Graph can generate mermaid stateDiagram-v2 diagrams for graphs, as shown above.

These diagrams can be generated with:

Graph.mermaid_code to generate the mermaid code for a graph
Graph.mermaid_image to generate an image of the graph using mermaid.ink
Graph.mermaid_save to generate an image of the graph using mermaid.ink and save it to a file
Beyond the diagrams shown above, you can also customize mermaid diagrams with the following options:

Edge allows you to apply a label to an edge
BaseNode.docstring_notes and BaseNode.get_note allows you to add notes to nodes
The highlighted_nodes parameter allows you to highlight specific node(s) in the diagram
Putting that together, we can edit the last ai_q_and_a_graph.py example to:

add labels to some edges
add a note to the Ask node
highlight the Answer node
save the diagram as a PNG image to file
ai_q_and_a_graph_extra.py

...
from typing import Annotated

from pydantic_graph import BaseNode, End, Graph, GraphRunContext, Edge

...

@dataclass
class Ask(BaseNode[QuestionState]):
    """Generate question using GPT-4o."""
    docstring_notes = True
    async def run(
        self, ctx: GraphRunContext[QuestionState]
    ) -> Annotated[Answer, Edge(label='Ask the question')]:
        ...

...

@dataclass
class Evaluate(BaseNode[QuestionState]):
    answer: str

    async def run(
            self,
            ctx: GraphRunContext[QuestionState],
    ) -> Annotated[End[str], Edge(label='success')] | Reprimand:
        ...

...

question_graph.mermaid_save('image.png', highlighted_nodes=[Answer])
(This example is not complete and cannot be run directly)

Would generate and image that looks like this:

Ask the question
success
Ask
Answer
Judge the answer.
Decide on next step.
Evaluate
Reprimand
question_graph
Setting Direction of the State Diagram
You can specify the direction of the state diagram using one of the following values:

'TB': Top to bottom, the diagram flows vertically from top to bottom.
'LR': Left to right, the diagram flows horizontally from left to right.
'RL': Right to left, the diagram flows horizontally from right to left.
'BT': Bottom to top, the diagram flows vertically from bottom to top.
Here is an example of how to do this using 'Left to Right' (LR) instead of the default 'Top to Bottom' (TB)

vending_machine_diagram.py

from vending_machine import InsertCoin, vending_machine_graph

vending_machine_graph.mermaid_code(start_node=InsertCoin, direction='LR')
InsertCoin
CoinsInserted
SelectProduct
Purchase
vending_machine_graph


