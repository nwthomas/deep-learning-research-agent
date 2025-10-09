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

    def __init__(self, **kwargs: str | int | bool) -> None:
        """Initialize the application configuration.

        Args:
            kwargs (dict): All key-value environment variable names + values
        """
        for key, value in kwargs.items():
            setattr(self, key, value)


def build_app_config() -> AppConfig:
    """Build the application configuration from environment variables.

    Returns:
        AppConfig: The application configuration
    """

    return AppConfig(
        # Server settings
        APP_DEBUG=os.getenv("APP_DEBUG", "false").lower() == "true",
        APP_HOST=os.getenv("APP_HOST", "0.0.0.0"),
        APP_LOG_LEVEL=os.getenv("APP_LOG_LEVEL", "info"),
        APP_NAME=os.getenv("APP_NAME", "deep-learning-research-agent"),
        APP_PORT=int(os.getenv("APP_PORT", 8000)),
        APP_RELOAD=os.getenv("APP_RELOAD", "true").lower() == "true",
        APP_VERSION=os.getenv("APP_VERSION", ""),
        # Limits on WebSocket connections
        MAX_CONCURRENT_WEBSOCKET_CONNECTIONS=int(os.getenv("MAX_CONCURRENT_WEBSOCKET_CONNECTIONS", 100)),
        # Limits on resource usage
        MAX_CONCURRENT_RESEARCH_UNITS=int(os.getenv("MAX_CONCURRENT_RESEARCH_UNITS", 1)),
        MAX_RESEARCHER_ITERATIONS=int(os.getenv("MAX_RESEARCHER_ITERATIONS", 1)),
        # Researcher model used for conducting research
        RESEARCHER_MODEL_API_KEY=os.getenv("RESEARCHER_MODEL_API_KEY", ""),
        RESEARCHER_MODEL_BASE_URL=os.getenv("RESEARCHER_MODEL_BASE_URL", ""),
        RESEARCHER_MODEL_NAME=os.getenv("RESEARCHER_MODEL_NAME", ""),
        RESEARCHER_MODEL_PROVIDER=os.getenv("RESEARCHER_MODEL_PROVIDER", ""),
        # Supervisor model used as main agent overseeing sub-agents
        SUPERVISOR_MODEL_API_KEY=os.getenv("SUPERVISOR_MODEL_API_KEY", ""),
        SUPERVISOR_MODEL_BASE_URL=os.getenv("SUPERVISOR_MODEL_BASE_URL", ""),
        SUPERVISOR_MODEL_NAME=os.getenv("SUPERVISOR_MODEL_NAME", ""),
        SUPERVISOR_MODEL_PROVIDER=os.getenv("SUPERVISOR_MODEL_PROVIDER", ""),
    )


app_config = build_app_config()
