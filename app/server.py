"""FastAPI server for the deep learning research agent."""

import uuid
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket

from app.api import CustomError, manager

from .config import app_config


# Hook into the application lifecycle for logging and custom logic
@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    # Run on startup
    print(f"Starting {app_config.APP_NAME}")
    yield
    # Run on shutdown
    print(f"Shutting down {app_config.APP_NAME}")


# Create FastAPI app
app = FastAPI(
    title="Deep Learning Research Agent API",
    description="API for conducting deep learning research with streaming capabilities",
    version="0.1.0",
    lifespan=lifespan,
    debug=app_config.APP_DEBUG,
)

# Add CORS middleware
# TODO: Configure appropriately for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Handle request validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle Pydantic validation errors with a consistent format."""
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


# Handle custom application errors
@app.exception_handler(CustomError)
async def custom_exception_handler(_request: Request, exc: CustomError) -> JSONResponse:
    """Handle custom application errors."""
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


# Handle unexpected application errors
@app.exception_handler(Exception)
async def global_exception_handler(_request: Request, _exc: Exception) -> JSONResponse:
    """Handle unexpected errors with consistent format."""
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


# Health check endpoint for various cloud providers check
@app.get("/health")
async def health_check() -> dict[str, str | dict[str, int]]:
    """Health check endpoint."""
    connection_stats = await manager.get_connection_stats()
    return {
        "status": "healthy",
        "service": app_config.APP_NAME,
        "connection_stats": connection_stats,
    }


# TODO: Add API endpoints and routers for the /ws application here. Move this into the endpoints file.
@app.websocket("/ws/research")
async def websocket_research_endpoint(websocket: WebSocket) -> None:
    """
    WebSocket endpoint for real-time streaming research.

    Protocol:
    1. Client connects to this endpoint
    2. Client sends a JSON message with the research query: {"query": "your question"}
    3. Server streams back real-time updates as JSON events
    4. Connection closes when research is complete or on error

    Event types:
    - status_update: Progress updates (graph, node, status)
    - tool_call: When the agent calls a tool (tool_name, args, tool_id)
    - result_chunk: Streaming content chunks (content, message_type)
    - completed: Final completion event (final_result, total_messages)
    - error: Error events (message)
    """
    client_id = str(uuid.uuid4())
    connection_accepted = await manager.connect(websocket, client_id)

    if not connection_accepted:
        return  # Connection was rejected due to server overload

    try:
        await manager.handle_research_stream(websocket, client_id)
    except Exception as e:
        await manager.send_json(
            client_id, {"event_type": "error", "data": {"message": f"Unexpected error: {str(e)}"}, "timestamp": None}
        )
    finally:
        await manager.disconnect(client_id)
