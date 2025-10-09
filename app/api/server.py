"""Module: server.py

Description:
    Main server file for the server application. It initializes a FastAPI app, adds middleware, and handles
    various exceptions.

Author: Nathan Thomas
"""

import uuid
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, WebSocket
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from ..shared.config import app_config
from ..shared.errors import CustomError
from .websocket import manager


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Hook into the application lifecycle for logging and custom logic. Run on startup and shutdown.

    Args:
        _app (FastAPI): The FastAPI app

    Returns:
        AsyncGenerator[None, None]: The lifespan generator
    """

    # Everything below this is run on startup
    print(f"Starting {app_config.APP_NAME}")
    yield

    # Everything below this is run on shutdown
    print(f"Shutting down {app_config.APP_NAME}")


# Create FastAPI app
app = FastAPI(
    title="Deep Learning Research Agent API",
    description="API for conducting deep learning research with streaming capabilities",
    version=app_config.APP_VERSION,
    lifespan=lifespan,
    debug=app_config.APP_DEBUG,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle Pydantic validation errors with a consistent format.

    Args:
        _request (Request): The request that caused the validation error
        exc (RequestValidationError): The validation error

    Returns:
        JSONResponse: The JSON response with the validation error
    """

    return JSONResponse(
        status_code=422,
        content={
            "detail": [
                {
                    "message": error["msg"],
                    "code": "VALIDATION_ERROR",
                    "field": (".".join(str(loc) for loc in error["loc"]) if error.get("loc") else None),
                }
                for error in exc.errors()
            ]
        },
    )


@app.exception_handler(CustomError)
async def custom_exception_handler(_request: Request, exc: CustomError) -> JSONResponse:
    """Handle custom application errors.

    Args:
        _request (Request): The request that caused the custom error
        exc (CustomError): The custom error

    Returns:
        JSONResponse: The JSON response with the custom error
    """

    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def global_exception_handler(_request: Request, _exc: Exception) -> JSONResponse:
    """Handle unexpected errors with consistent format.

    Args:
        _request (Request): The request that caused the error
        _exc (Exception): The unexpected error

    Returns:
        JSONResponse: The JSON response with the unexpected error
    """

    return JSONResponse(
        status_code=500,
        content={
            "detail": [
                {
                    "message": "An internal server error occurred",
                    "code": "INTERNAL_ERROR",
                    "field": None,
                }
            ]
        },
    )


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        dict[str, str]: The health check response
    """

    return {
        "status": "healthy",
        "service": app_config.APP_NAME,
    }


@app.websocket("/ws")
async def handle_websocket_stream(websocket: WebSocket) -> None:
    """WebSocket endpoint for real-time streaming research

    Args:
        websocket (WebSocket): The websocket connection
    """

    # TODO: This could be upgraded for a production environment to track clients by a real unique ID
    # persisted across sessions. However, this is fine for this server's purposes right now.
    client_id = str(uuid.uuid4())
    connection_accepted = await manager.connect(websocket, client_id)

    # Connection was already closed by manager.connect() due to server overload. Simply return as there's
    # no need to send additional messages or disconnect.
    if not connection_accepted:
        return

    # Handle any further messages in the websocket stream through the established connection. This also
    # handles errors with disconnection, so no need for try/except here.
    await manager.handle_websocket_stream(websocket, client_id)
