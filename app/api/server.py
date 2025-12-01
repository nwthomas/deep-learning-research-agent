"""Module: server.py

Description:
    Main server file for the server application. It initializes a FastAPI app, adds middleware, and handles
    various exceptions.

Author: Nathan Thomas
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import app_config


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Hook into the application lifecycle for logging and custom logic. Run on startup and shutdown.

    Args:
        _app (FastAPI): The FastAPI app

    Returns:
        AsyncGenerator[None, None]: The lifespan generator
    """

    print(f"Starting {app_config.APP_NAME}")
    yield
    print(f"Shutting down {app_config.APP_NAME}")


app = FastAPI(
    title="Deep Learning Research Agent API",
    description="API for conducting deep learning research with streaming capabilities",
    version=app_config.APP_VERSION,
    lifespan=lifespan,
    debug=app_config.APP_DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
