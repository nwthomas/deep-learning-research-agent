import os
from datetime import datetime

from IPython.display import Image, display
from langchain.chat_models import init_chat_model
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

def get_model(use_local=False):
    """Initialize the chat model based on configuration."""
    if use_local:
        # Use local Ollama model
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "")
        ollama_model = os.getenv("MODEL_NAME", "")
        
        # Create model configuration for Ollama using OpenAI-compatible API
        model = init_chat_model(
            model=ollama_model if not None else "openai/chat",
            model_provider="ollama",
            base_url=ollama_base_url,
            api_key="ollama",  # Required but ignored by Ollama
            temperature=0.0
        )
    else:
        # Use Anthropic Claude
        model = init_chat_model(model="anthropic:claude-sonnet-4-20250514", temperature=0.0)
    
    return model

# Default model (will be overridden in run_agent if needed)
model = get_model()

# Limits
max_concurrent_research_units = 3
max_researcher_iterations = 3

# Tools
sub_agent_tools = [tavily_search, think_tool]
built_in_tools = [ls, read_file, write_file, write_todos, think_tool]

# Create research sub-agent
research_sub_agent = {
    "name": "research-agent",
    "description": "Delegate research to the sub-agent researcher. Only give this researcher one topic at a time.",
    "prompt": RESEARCHER_INSTRUCTIONS.format(date=get_today_str()),
    "tools": ["tavily_search", "think_tool"],
}

# Create task tool to delegate tasks to sub-agents
task_tool = _create_task_tool(
    sub_agent_tools, [research_sub_agent], model, DeepAgentState
)

delegation_tools = [task_tool]
all_tools = sub_agent_tools + built_in_tools + delegation_tools

# Build prompt
SUBAGENT_INSTRUCTIONS = SUBAGENT_USAGE_INSTRUCTIONS.format(
    max_concurrent_research_units=max_concurrent_research_units,
    max_researcher_iterations=max_researcher_iterations,
    date=datetime.now().strftime("%a %b %-d, %Y"),
)

def run_agent(user_input, use_local=False):
    """Run the agent with the given user input.
    
    Args:
        user_input (str): The user's input/query
        use_local (bool): If True, use local Ollama model; if False, use Anthropic Claude
    """
    # Get the appropriate model based on the use_local flag
    current_model = get_model(use_local=use_local)
    
    # Create task tool with the current model
    current_task_tool = _create_task_tool(
        sub_agent_tools, [research_sub_agent], current_model, DeepAgentState
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