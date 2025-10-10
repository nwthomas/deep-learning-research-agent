"""Module: conftest.py

Description:
    Pytest configuration and fixtures for the test suite. Sets up mock environment
    variables and other test configurations needed across all tests.

Author: Nathan Thomas
"""

import os
from collections.abc import Generator
from unittest.mock import patch

import pytest


@pytest.fixture(scope="session", autouse=True)
def mock_environment_variables() -> Generator[None, None, None]:
    """Mock environment variables for testing.

    This fixture automatically runs for all tests and mocks the required
    environment variables to prevent initialization errors during import.
    """

    with patch.dict(
        os.environ,
        {
            # Supervisor model configuration
            "SUPERVISOR_MODEL_API_KEY": "test-supervisor-api-key",
            "SUPERVISOR_MODEL_BASE_URL": "https://test-supervisor-url.com",
            "SUPERVISOR_MODEL_NAME": "test-supervisor-model",
            "SUPERVISOR_MODEL_PROVIDER": "test-provider",
            # Researcher model configuration
            "RESEARCHER_MODEL_API_KEY": "test-researcher-api-key",
            "RESEARCHER_MODEL_BASE_URL": "https://test-researcher-url.com",
            "RESEARCHER_MODEL_NAME": "test-researcher-model",
            "RESEARCHER_MODEL_PROVIDER": "test-provider",
            # Other required environment variables
            "TAVILY_API_KEY": "test-tavily-key",
            "APP_DEBUG": "false",
            "APP_HOST": "0.0.0.0",
            "APP_PORT": "8000",
            "MAX_CONCURRENT_RESEARCH_UNITS": "1",
            "MAX_RESEARCHER_ITERATIONS": "1",
            "MAX_CONCURRENT_WEBSOCKET_CONNECTIONS": "100",
        },
    ):
        yield
