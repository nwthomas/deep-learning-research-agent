"""Deep Learning Research Agent FastAPI Server"""

import signal
import sys
from types import FrameType
from typing import Any

import uvicorn

from app.config import app_config


def signal_handler(signum: int, frame: FrameType | None) -> Any:
    """Allow graceful shutdown of the application."""

    print(f"\nReceived signal {signum}, shutting down gracefully...")
    sys.exit(0)


def run_server() -> None:
    """Run the application server via uvicorn with proper signal handling."""

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Run the application server
    uvicorn.run(
        "app.server:app",
        host=app_config.APP_HOST,
        port=app_config.APP_PORT,
        log_level=app_config.APP_LOG_LEVEL,
        reload=app_config.APP_RELOAD,
    )


if __name__ == "__main__":
    run_server()
