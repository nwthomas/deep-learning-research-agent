import os
from datetime import datetime

from IPython.display import Image, display
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langgraph.prebuilt import create_react_agent
from .utils import format_messages, show_prompt, stream_agent

from .file_tools import ls, read_file, write_file
from .prompts import (
    FILE_USAGE_INSTRUCTIONS,
    RESEARCHER_INSTRUCTIONS,
    SUBAGENT_USAGE_INSTRUCTIONS,
    TODO_USAGE_INSTRUCTIONS,
)
from .research_tools import tavily_search, think_tool, get_today_str
from .state import DeepAgentState
from .task_tool import _create_task_tool
from .todo_tools import write_todos

def build_chat_model(model_api_key: str, model_base_url: str, model_name: str, model_provider: str) -> BaseChatModel:
    """Builds a chat model with the given parameters.
    
    Args:
        model_api_key: The API key for the model
        model_base_url: The base URL for the model
        model_name: The name of the model
        model_provider: The provider of the model

    Returns:
        A chat model
    """
    model = init_chat_model(
        model=model_name,
        model_provider=model_provider,
        base_url=model_base_url,
        api_key=model_api_key,
        temperature=0.0
    )
    return model

# Supervisor model used as main agent overseeing sub-agents
SUPERVISOR_MODEL_API_KEY = os.getenv("SUPERVISOR_MODEL_API_KEY", "")
SUPERVISOR_MODEL_BASE_URL = os.getenv("SUPERVISOR_MODEL_BASE_URL", "")
SUPERVISOR_MODEL_NAME = os.getenv("SUPERVISOR_MODEL_NAME", "")
SUPERVISOR_MODEL_PROVIDER = os.getenv("SUPERVISOR_MODEL_PROVIDER", "")
SUPERVISOR_MODEL = build_chat_model(SUPERVISOR_MODEL_API_KEY, SUPERVISOR_MODEL_BASE_URL, SUPERVISOR_MODEL_NAME, SUPERVISOR_MODEL_PROVIDER)

# Researcher model used for conducting research
RESEARCHER_MODEL_API_KEY = os.getenv("RESEARCHER_MODEL_API_KEY", "")
RESEARCHER_MODEL_BASE_URL = os.getenv("RESEARCHER_MODEL_BASE_URL", "")
RESEARCHER_MODEL_NAME = os.getenv("RESEARCHER_MODEL_NAME", "")
RESEARCHER_MODEL_PROVIDER = os.getenv("RESEARCHER_MODEL_PROVIDER", "")
RESEARCHER_MODEL = build_chat_model(RESEARCHER_MODEL_API_KEY, RESEARCHER_MODEL_BASE_URL, RESEARCHER_MODEL_NAME, RESEARCHER_MODEL_PROVIDER)

# Limits on resource usage
MAX_CONCURRENT_RESEARCH_UNITS = os.getenv("MAX_CONCURRENT_RESEARCH_UNITS", 3)
MAX_RESEARCHER_ITERATIONS = os.getenv("MAX_RESEARCHER_ITERATIONS", 3)

# Tools
sub_agent_tools = [tavily_search, think_tool]
built_in_tools = [ls, read_file, write_file, write_todos, think_tool]

# Create research sub-agent
SUB_AGENT_RESEARCHER = {
    "name": "research-agent",
    "description": "Delegate research to the sub-agent researcher. Only give this researcher one topic at a time.",
    "prompt": RESEARCHER_INSTRUCTIONS.format(date=get_today_str()),
    "tools": ["tavily_search", "think_tool"],
}

# Create task tool to delegate tasks to research sub-agent
task_tool = _create_task_tool(
    sub_agent_tools, [SUB_AGENT_RESEARCHER], SUPERVISOR_MODEL, DeepAgentState
)

delegation_tools = [task_tool]
all_tools = sub_agent_tools + built_in_tools + delegation_tools

# Build prompt
SUBAGENT_INSTRUCTIONS = SUBAGENT_USAGE_INSTRUCTIONS.format(
    max_concurrent_research_units=MAX_CONCURRENT_RESEARCH_UNITS,
    max_researcher_iterations=MAX_RESEARCHER_ITERATIONS,
    date=datetime.now().strftime("%a %b %-d, %Y"),
)

def run_agent(user_input, use_local=False):
    """Run the agent with the given user input.
    
    Args:
        user_input (str): The user's input/query
        use_local (bool): If True, use local Ollama model; if False, use Anthropic Claude
    """
    # Get the appropriate model based on the use_local flag
    current_model = SUPERVISOR_MODEL
    
    # Create task tool with the current model
    current_task_tool = _create_task_tool(
        sub_agent_tools, [SUB_AGENT_RESEARCHER], current_model, DeepAgentState
    )   
    
    # Update tools list with the current task tool
    current_delegation_tools = [current_task_tool]
    current_all_tools = sub_agent_tools + built_in_tools + current_delegation_tools
    
    INSTRUCTIONS = (
        "# TODO MANAGEMENT\n"
        + TODO_USAGE_INSTRUCTIONS
        + "\n\n"
        + "=" * 80
        + "\n\n"
        + "# FILE SYSTEM USAGE\n"
        + FILE_USAGE_INSTRUCTIONS
        + "\n\n"
        + "=" * 80
        + "\n\n"
        + "# SUB-AGENT DELEGATION\n"
        + SUBAGENT_INSTRUCTIONS
    )

    agent = create_react_agent(
        current_model, current_all_tools, prompt=INSTRUCTIONS, state_schema=DeepAgentState
    )

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
        }
    )

    format_messages(result["messages"])