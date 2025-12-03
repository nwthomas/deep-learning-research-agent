from pydantic import BaseModel
from pydantic_ai import Agent, RunContext, Tool

from app.agents.state import State


class ResearchResult(BaseModel):
    query: str
    summary: str
    files_created: list[str]


@Tool
async def research_web(_ctx: RunContext[State], _query: str) -> ResearchResult:
    """Search web, summarize, and store results in state."""

    result = "This is a test research result. If you're reading this, you're inside of a test research call. Summarize this and return it to the user."

    return ResearchResult(query=_query, summary=result, files_created=[])


research_agent = Agent[str, ResearchResult](
    instructions="You perform research: web search, summarize, and store results as files in state.",
    tools=[research_web],
)
