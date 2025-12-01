"""Module: config.py

Description:
    This file initializes the application configuration from environment variables. While it does allow
    some fallback default values, it's recommended to not rely on them (and certainly not for a production
    environment).

Author: Nathan Thomas
"""

import os

from dotenv import load_dotenv

load_dotenv()


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
    # Limits on WebSocket connections
    MAX_CONCURRENT_WEBSOCKET_CONNECTIONS: int
    # Limits on resource usage
    MAX_CONCURRENT_RESEARCH_UNITS: int
    MAX_RESEARCHER_ITERATIONS: int
    # Researcher model used for conducting research
    RESEARCHER_MODEL_API_KEY: str
    RESEARCHER_MODEL_BASE_URL: str
    RESEARCHER_MODEL_NAME: str
    RESEARCHER_MODEL_PROVIDER: str
    # Supervisor model used as main agent overseeing sub-agents
    SUPERVISOR_MODEL_API_KEY: str
    SUPERVISOR_MODEL_BASE_URL: str
    SUPERVISOR_MODEL_NAME: str
    SUPERVISOR_MODEL_PROVIDER: str

    def __init__(self) -> None:
        """Initializes the application configuration with environment variables."""

        self.APP_DEBUG = os.getenv("APP_DEBUG", "false").lower() == "true"
        self.APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
        self.APP_LOG_LEVEL = os.getenv("APP_LOG_LEVEL", "info")
        self.APP_NAME = os.getenv("APP_NAME", "deep-learning-research-agent")
        self.APP_PORT = int(os.getenv("APP_PORT", 8000))
        self.APP_RELOAD = os.getenv("APP_RELOAD", "true").lower() == "true"
        self.APP_VERSION = os.getenv("APP_VERSION", "")
        # Limits on WebSocket connections
        self.MAX_CONCURRENT_WEBSOCKET_CONNECTIONS = int(
            int(os.getenv("MAX_CONCURRENT_WEBSOCKET_CONNECTIONS", 100)),
        )
        # Limits on resource usage
        self.MAX_CONCURRENT_RESEARCH_UNITS = int(os.getenv("MAX_CONCURRENT_RESEARCH_UNITS", 1))
        self.MAX_RESEARCHER_ITERATIONS = int(os.getenv("MAX_RESEARCHER_ITERATIONS", 1))
        # Researcher model used for conducting research
        self.RESEARCHER_MODEL_API_KEY = os.getenv("RESEARCHER_MODEL_API_KEY", "")
        self.RESEARCHER_MODEL_BASE_URL = os.getenv("RESEARCHER_MODEL_BASE_URL", "")
        self.RESEARCHER_MODEL_NAME = os.getenv("RESEARCHER_MODEL_NAME", "")
        self.RESEARCHER_MODEL_PROVIDER = os.getenv("RESEARCHER_MODEL_PROVIDER", "")
        # Supervisor model used as main agent overseeing sub-agents
        self.SUPERVISOR_MODEL_API_KEY = os.getenv("SUPERVISOR_MODEL_API_KEY", "")
        self.SUPERVISOR_MODEL_BASE_URL = os.getenv("SUPERVISOR_MODEL_BASE_URL", "")
        self.SUPERVISOR_MODEL_NAME = os.getenv("SUPERVISOR_MODEL_NAME", "")
        self.SUPERVISOR_MODEL_PROVIDER = os.getenv("SUPERVISOR_MODEL_PROVIDER", "")


app_config = AppConfig()
