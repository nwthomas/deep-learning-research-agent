import os
from unittest.mock import patch

import pytest

from app.config import AppConfig, build_app_config


class TestAppConfig:
    """Test cases for AppConfig class."""

    def test_init_with_kwargs(self) -> None:
        """Test AppConfig initialization with keyword arguments."""
        config = AppConfig(
            APP_NAME="test-app",
            APP_PORT=9000,
            APP_DEBUG=True,
        )

        assert config.APP_NAME == "test-app"
        assert config.APP_PORT == 9000
        assert config.APP_DEBUG is True

    def test_init_empty(self) -> None:
        """Test AppConfig initialization with no arguments."""
        config = AppConfig()
        # Should not have any attributes set
        assert not hasattr(config, "APP_NAME")


class TestBuildAppConfig:
    """Test cases for build_app_config function."""

    def test_default_values(self) -> None:
        """Test build_app_config with default environment values."""
        with patch.dict(os.environ, {}, clear=True):
            config = build_app_config()

            # Server settings defaults
            assert config.APP_DEBUG is False
            assert config.APP_HOST == "0.0.0.0"
            assert config.APP_LOG_LEVEL == "info"
            assert config.APP_NAME == "deep-learning-research-agent"
            assert config.APP_PORT == 8000
            assert config.APP_RELOAD is True

            # Connection limits defaults
            assert config.MAX_CONCURRENT_CONNECTIONS == 50

            # Resource limits defaults
            assert config.MAX_CONCURRENT_RESEARCH_UNITS == 3
            assert config.MAX_RESEARCHER_ITERATIONS == 3

            # Model settings defaults (empty strings)
            assert config.RESEARCHER_MODEL_API_KEY == ""
            assert config.RESEARCHER_MODEL_BASE_URL == ""
            assert config.RESEARCHER_MODEL_NAME == ""
            assert config.RESEARCHER_MODEL_PROVIDER == ""
            assert config.SUPERVISOR_MODEL_API_KEY == ""
            assert config.SUPERVISOR_MODEL_BASE_URL == ""
            assert config.SUPERVISOR_MODEL_NAME == ""
            assert config.SUPERVISOR_MODEL_PROVIDER == ""

    def test_custom_environment_values(self) -> None:
        """Test build_app_config with custom environment values."""
        env_vars = {
            "APP_DEBUG": "true",
            "APP_HOST": "localhost",
            "APP_LOG_LEVEL": "debug",
            "APP_NAME": "custom-app",
            "APP_PORT": "9999",
            "APP_RELOAD": "false",
            "MAX_CONCURRENT_CONNECTIONS": "100",
            "MAX_CONCURRENT_RESEARCH_UNITS": "5",
            "MAX_RESEARCHER_ITERATIONS": "10",
            "RESEARCHER_MODEL_API_KEY": "researcher-key",
            "RESEARCHER_MODEL_BASE_URL": "https://researcher.api.com",
            "RESEARCHER_MODEL_NAME": "researcher-model",
            "RESEARCHER_MODEL_PROVIDER": "researcher-provider",
            "SUPERVISOR_MODEL_API_KEY": "supervisor-key",
            "SUPERVISOR_MODEL_BASE_URL": "https://supervisor.api.com",
            "SUPERVISOR_MODEL_NAME": "supervisor-model",
            "SUPERVISOR_MODEL_PROVIDER": "supervisor-provider",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = build_app_config()

            # Server settings
            assert config.APP_DEBUG is True
            assert config.APP_HOST == "localhost"
            assert config.APP_LOG_LEVEL == "debug"
            assert config.APP_NAME == "custom-app"
            assert config.APP_PORT == 9999
            assert config.APP_RELOAD is False

            # Connection limits
            assert config.MAX_CONCURRENT_CONNECTIONS == 100

            # Resource limits
            assert config.MAX_CONCURRENT_RESEARCH_UNITS == 5
            assert config.MAX_RESEARCHER_ITERATIONS == 10

            # Researcher model settings
            assert config.RESEARCHER_MODEL_API_KEY == "researcher-key"
            assert config.RESEARCHER_MODEL_BASE_URL == "https://researcher.api.com"
            assert config.RESEARCHER_MODEL_NAME == "researcher-model"
            assert config.RESEARCHER_MODEL_PROVIDER == "researcher-provider"

            # Supervisor model settings
            assert config.SUPERVISOR_MODEL_API_KEY == "supervisor-key"
            assert config.SUPERVISOR_MODEL_BASE_URL == "https://supervisor.api.com"
            assert config.SUPERVISOR_MODEL_NAME == "supervisor-model"
            assert config.SUPERVISOR_MODEL_PROVIDER == "supervisor-provider"

    def test_boolean_parsing(self) -> None:
        """Test boolean environment variable parsing."""
        test_cases = [
            ("true", True),
            ("True", True),
            ("TRUE", True),
            ("false", False),
            ("False", False),
            ("FALSE", False),
            ("yes", False),  # Only "true" (case-insensitive) should be True
            ("1", False),
            ("", False),
        ]

        for env_value, expected in test_cases:
            with patch.dict(os.environ, {"APP_DEBUG": env_value}, clear=True):
                config = build_app_config()
                assert config.APP_DEBUG is expected, f"Failed for value: {env_value}"

    def test_integer_parsing(self) -> None:
        """Test integer environment variable parsing."""
        with patch.dict(os.environ, {"APP_PORT": "5000"}, clear=True):
            config = build_app_config()
            assert config.APP_PORT == 5000
            assert isinstance(config.APP_PORT, int)

    def test_integer_parsing_invalid(self) -> None:
        """Test integer parsing with invalid values."""
        with patch.dict(os.environ, {"APP_PORT": "invalid"}, clear=True):
            with pytest.raises(ValueError):
                build_app_config()

    def test_returns_app_config_instance(self) -> None:
        """Test that build_app_config returns an AppConfig instance."""
        config = build_app_config()
        assert isinstance(config, AppConfig)

    def test_all_required_attributes_present(self) -> None:
        """Test that all required attributes are present in the config."""
        config = build_app_config()

        required_attributes = [
            "APP_DEBUG",
            "APP_HOST",
            "APP_LOG_LEVEL",
            "APP_NAME",
            "APP_PORT",
            "APP_RELOAD",
            "MAX_CONCURRENT_CONNECTIONS",
            "MAX_CONCURRENT_RESEARCH_UNITS",
            "MAX_RESEARCHER_ITERATIONS",
            "RESEARCHER_MODEL_API_KEY",
            "RESEARCHER_MODEL_BASE_URL",
            "RESEARCHER_MODEL_NAME",
            "RESEARCHER_MODEL_PROVIDER",
            "SUPERVISOR_MODEL_API_KEY",
            "SUPERVISOR_MODEL_BASE_URL",
            "SUPERVISOR_MODEL_NAME",
            "SUPERVISOR_MODEL_PROVIDER",
        ]

        for attr in required_attributes:
            assert hasattr(config, attr), f"Missing attribute: {attr}"
