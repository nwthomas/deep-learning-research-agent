from pydantic import BaseModel
from pydantic_ai import Agent, AgentRunResult
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

from app.config.config import app_config


class Answer(BaseModel):
    answer: str


provider = OllamaProvider(base_url=app_config.SUPERVISOR_MODEL_BASE_URL)

ollama_model = OpenAIChatModel(
    model_name=app_config.SUPERVISOR_MODEL_NAME,
    provider=provider,
)

supervisor_agent = Agent[str, Answer](
    ollama_model,
    deps_type=int,
    output_type=Answer,
    system_prompt="You are a helpful assistant that responds to the user with short 1 sentence answers.",
)


def call_supervisor_agent() -> AgentRunResult[Answer]:
    """Call the supervisor agent to get the city location."""

    return supervisor_agent.run_sync(
        "What do you think about taking a career sabbatical when you have money saved up?",
        deps=10,
    )
