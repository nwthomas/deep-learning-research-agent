from pydantic import BaseModel
from pydantic_ai import Agent, ModelSettings, RunContext, Tool
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

from app.agents.state import State
from app.config.config import app_config


class ResearchResult(BaseModel):
    query: str
    summary: str
    files_created: list[str]


@Tool
async def research_web(_ctx: RunContext[State], _query: str) -> ResearchResult:
    """Search web, summarize, and store results in state."""

    result = "This is a test research result. If you're reading this, you're inside of a test research call. Summarize this and return it to the user."

    return ResearchResult(query=_query, summary=result, files_created=[])


provider = OllamaProvider(base_url=app_config.RESEARCHER_MODEL_BASE_URL)

researcher_model = OpenAIChatModel(
    model_name=app_config.RESEARCHER_MODEL_NAME,
    provider=provider,
    settings=ModelSettings(temperature=app_config.RESEARCHER_MODEL_TEMPERATURE),
)

research_agent = Agent[str, ResearchResult](
    instructions="You perform research: web search, summarize, and store results as files in state.",
    model=researcher_model,
    retries=app_config.RESEARCHER_MODEL_RETRIES,
    tools=[research_web],
)
