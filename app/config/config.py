import os

from dotenv import load_dotenv

load_dotenv()

DEFAULT_MAX_ITERATIONS = 25
DEFAULT_RETRIES = 3


class AppConfig:
    """Application configuration environment variables."""

    # Server settings
    APP_DEBUG: bool
    APP_HOST: str
    APP_LOG_LEVEL: str
    APP_NAME: str
    APP_PORT: int
    APP_RELOAD: bool
    APP_VERSION: str

    # Supervisor model used as main agent overseeing sub-agents
    SUPERVISOR_MODEL_API_KEY: str
    SUPERVISOR_MODEL_BASE_URL: str
    SUPERVISOR_MODEL_MAX_ITERATIONS: int
    SUPERVISOR_MODEL_PROVIDER: str
    SUPERVISOR_MODEL_NAME: str
    SUPERVISOR_MODEL_TEMPERATURE: float
    SUPERVISOR_MODEL_RETRIES: int

    # Summarization model settings
    SUMMARIZATION_MODEL_BASE_URL: str
    SUMMARIZATION_MODEL_NAME: str

    # Researcher model settings
    RESEARCHER_MODEL_API_KEY: str
    RESEARCHER_MODEL_BASE_URL: str
    RESEARCHER_MODEL_NAME: str
    RESEARCHER_MODEL_PROVIDER: str
    RESEARCHER_MODEL_TEMPERATURE: float
    RESEARCHER_MODEL_RETRIES: int

    def __init__(self) -> None:
        """Initializes the application configuration with environment variables."""

        # Server settings
        self.APP_DEBUG = os.getenv("APP_DEBUG", "false").lower() == "true"
        self.APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
        self.APP_LOG_LEVEL = os.getenv("APP_LOG_LEVEL", "info")
        self.APP_NAME = os.getenv("APP_NAME", "deep-learning-research-agent")
        self.APP_PORT = int(os.getenv("APP_PORT", 8000))
        self.APP_RELOAD = os.getenv("APP_RELOAD", "true").lower() == "true"
        self.APP_VERSION = os.getenv("APP_VERSION", "")

        # Supervisor model used as main agent overseeing sub-agents
        self.SUPERVISOR_MODEL_API_KEY = os.getenv("SUPERVISOR_MODEL_API_KEY", "")
        self.SUPERVISOR_MODEL_BASE_URL = os.getenv("SUPERVISOR_MODEL_BASE_URL", "")
        self.SUPERVISOR_MODEL_NAME = os.getenv("SUPERVISOR_MODEL_NAME", "")
        self.SUPERVISOR_MODEL_PROVIDER = os.getenv("SUPERVISOR_MODEL_PROVIDER", "")
        self.SUPERVISOR_MODEL_MAX_ITERATIONS = int(os.getenv("SUPERVISOR_MODEL_MAX_ITERATIONS", DEFAULT_MAX_ITERATIONS))
        self.SUPERVISOR_MODEL_RETRIES = int(os.getenv("SUPERVISOR_MODEL_RETRIES", DEFAULT_RETRIES))
        self.SUPERVISOR_MODEL_TEMPERATURE = float(os.getenv("SUPERVISOR_MODEL_TEMPERATURE", 0.0))

        # Researcher model agent settings
        self.RESEARCHER_MODEL_API_KEY = os.getenv("RESEARCHER_MODEL_API_KEY", "")
        self.RESEARCHER_MODEL_BASE_URL = os.getenv(
            "RESEARCHER_MODEL_BASE_URL", os.getenv("SUPERVISOR_MODEL_BASE_URL", "")
        )
        self.RESEARCHER_MODEL_NAME = os.getenv("RESEARCHER_MODEL_NAME", "")
        self.RESEARCHER_MODEL_PROVIDER = os.getenv("RESEARCHER_MODEL_PROVIDER", "")
        self.RESEARCHER_MODEL_RETRIES = int(os.getenv("RESEARCHER_MODEL_RETRIES", DEFAULT_RETRIES))
        self.RESEARCHER_MODEL_TEMPERATURE = float(
            os.getenv(
                "RESEARCHER_MODEL_TEMPERATURE",
                0.0,
            )
        )


app_config = AppConfig()
