from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

from app.agents.prompts import SUMMARIZER_INSTRUCTIONS
from app.agents.utils import get_today_str
from app.config.config import app_config


class Summary(BaseModel):
    """Schema for webpage content summarization."""

    filename: str = Field(description="Name of the file to store.")
    summary: str = Field(description="Key learnings from the webpage.")


class SummaryResult(BaseModel):
    summary: Summary = Field(description="Summary of the webpage content.")


provider = OllamaProvider(base_url=app_config.SUMMARIZATION_MODEL_BASE_URL)

summarization_model = OpenAIChatModel(
    model_name=app_config.SUMMARIZATION_MODEL_NAME,
    provider=provider,
)

summarization_agent = Agent[str, SummaryResult](
    summarization_model,
    deps_type=int,
    output_type=SummaryResult,
    system_prompt=SUMMARIZER_INSTRUCTIONS.format(date=get_today_str()),
)
