from pydantic import BaseModel
from pydantic_ai import (
    Agent,
    AgentRunResult,
    ModelSettings,
    RunContext,
    Tool,
    UsageLimitExceeded,
)
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

from app.agents.prompts import SUPERVISOR_INSTRUCTIONS
from app.agents.researcher import ResearchResult, research_agent
from app.agents.state import (
    State,
    add_file,
    add_todo,
    complete_todo,
    get_file,
    get_file_names,
    get_todo,
    get_todo_names,
)
from app.agents.utils import get_today_str
from app.config.config import app_config


class Answer(BaseModel):
    """The final answer to the user's input question"""

    answer: str


@Tool
async def delegate_research(_ctx: RunContext[State], query: str) -> AgentRunResult[ResearchResult]:
    """Delegate research to the researcher agent."""
    result = await research_agent.run(query, state=_ctx.state)
    return result.data


provider = OllamaProvider(base_url=app_config.SUPERVISOR_MODEL_BASE_URL)

supervisor_model = OpenAIChatModel(
    model_name=app_config.SUPERVISOR_MODEL_NAME,
    provider=provider,
    settings=ModelSettings(temperature=app_config.SUPERVISOR_MODEL_TEMPERATURE),
)

supervisor_agent = Agent[str, Answer](
    deps_type=State,
    instructions=SUPERVISOR_INSTRUCTIONS.format(date=get_today_str()),
    model=supervisor_model,
    output_type=Answer,
    retries=app_config.SUPERVISOR_MODEL_RETRIES,
    tools=[
        delegate_research,
        add_file,
        get_file_names,
        get_file,
        add_todo,
        get_todo_names,
        get_todo,
        complete_todo,
    ],
)


def call_supervisor_agent(user_input: str) -> AgentRunResult[Answer]:
    """Call the supervisor agent to begin a research task based on the user's input."""

    print(SUPERVISOR_INSTRUCTIONS.format(date=get_today_str()))

    try:
        return supervisor_agent.run_sync(user_input, deps=State())
    except UsageLimitExceeded as e:
        print(f"Usage limit exceeded: {e}")
        return None
    except Exception as e:
        print(f"Error calling supervisor agent: {e}")
        return None
