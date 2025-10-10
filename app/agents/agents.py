"""Module: agents.py

Description:
    Contains main agent functionality for the deep learning research agent. This research agent spawns
    off sub-agents for a variety of research tasks.

Author: Nathan Thomas
"""

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

from ..shared.config import app_config
from .prompts import RESEARCHER_INSTRUCTIONS
from .tools import (
    get_today_str,
    ls,
    read_file,
    tavily_search,
    think_tool,
    write_file,
    write_todos,
)
from .tools.task_tool import SubAgent


def build_chat_model(model_api_key: str, model_base_url: str, model_name: str, model_provider: str) -> BaseChatModel:
    """Builds a chat model with the given parameters.

    Args:
        model_api_key (str): The API key for the model
        model_base_url (str): The base URL for the model
        model_name (str): The name of the model
        model_provider (str): The provider of the model

    Returns:
        BaseChatModel: A chat model created based on given parameters
    """

    if model_name == "":
        raise ValueError("Model name cannot be empty")

    return init_chat_model(
        model=model_name,
        model_provider=model_provider if model_provider != "" else None,
        base_url=model_base_url if model_base_url != "" else None,
        api_key=model_api_key if model_api_key != "" else None,
        temperature=0.0,
    )


# Model instances - initialized lazily when first accessed
_supervisor_model: BaseChatModel | None = None
_researcher_model: BaseChatModel | None = None


def get_supervisor_model() -> BaseChatModel:
    """Get the supervisor model, initializing it if necessary.

    Returns:
        BaseChatModel: The supervisor model
    """

    global _supervisor_model
    if _supervisor_model is None:
        _supervisor_model = build_chat_model(
            app_config.SUPERVISOR_MODEL_API_KEY,
            app_config.SUPERVISOR_MODEL_BASE_URL,
            app_config.SUPERVISOR_MODEL_NAME,
            app_config.SUPERVISOR_MODEL_PROVIDER,
        )
    return _supervisor_model


def get_researcher_model() -> BaseChatModel:
    """Get the researcher model, initializing it if necessary.

    Returns:
        BaseChatModel: The researcher model
    """

    global _researcher_model
    if _researcher_model is None:
        _researcher_model = build_chat_model(
            app_config.RESEARCHER_MODEL_API_KEY,
            app_config.RESEARCHER_MODEL_BASE_URL,
            app_config.RESEARCHER_MODEL_NAME,
            app_config.RESEARCHER_MODEL_PROVIDER,
        )
    return _researcher_model


# Tools
SUB_AGENT_RESEARCHER_TOOLS = [tavily_search, think_tool, read_file]
BUILT_IN_TOOLS = [ls, read_file, write_file, write_todos, think_tool]

# Create research sub-agent
SUB_AGENT_RESEARCHER: SubAgent = {
    "name": "research-agent",
    "description": "Delegate research to the sub-agent researcher. Only give this researcher one topic at a time.",
    "prompt": RESEARCHER_INSTRUCTIONS.format(date=get_today_str()),
    "tools": [f.name for f in SUB_AGENT_RESEARCHER_TOOLS],
}
