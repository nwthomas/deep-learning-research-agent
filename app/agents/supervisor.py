from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

from app.config.config import app_config


class CityLocation(BaseModel):
    city: str
    country: str


provider = OllamaProvider(base_url=app_config.SUPERVISOR_MODEL_BASE_URL)

ollama_model = OpenAIChatModel(
    model_name=app_config.SUPERVISOR_MODEL_NAME,
    provider=provider,
)

supervisor_agent = Agent[None, CityLocation](ollama_model, output_type=CityLocation)
