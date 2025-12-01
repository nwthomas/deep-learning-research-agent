"""Module: main.py

Description:
    Entrypoint file for running the FastAPI server that powers a deep learning research agent. It
    allows connection via websocket for real-time streaming of agent actions.

Author: Nathan Thomas
"""

import signal
import sys
from types import FrameType

import uvicorn

from app.config import app_config


def signal_handler(signum: int, _frame: FrameType | None) -> None:
    """Allow graceful shutdown of the application.

    Args:
        signum (int): The signal number.
        _frame (FrameType | None): The frame object.
    """

    print(f"\nReceived signal {signum}, shutting down gracefully...")
    sys.exit(0)


def run_server() -> None:
    """Run the application server via uvicorn with proper signal handling."""

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    uvicorn.run(
        "app.api.server:app",
        host=app_config.APP_HOST,
        port=app_config.APP_PORT,
        log_level=app_config.APP_LOG_LEVEL,
        reload=app_config.APP_RELOAD,
    )


if __name__ == "__main__":
    run_server()
