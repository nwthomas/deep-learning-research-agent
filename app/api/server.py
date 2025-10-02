"""FastAPI server for the deep learning research agent."""

import uuid

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from .websocket import manager

# Create FastAPI app
app = FastAPI(
    title="Deep Learning Research Agent API",
    description="API for conducting deep learning research with streaming capabilities",
    version="0.1.0",
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


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Deep Learning Research Agent API is running"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "deep-learning-research-agent"}


@app.websocket("/ws/research")
async def websocket_research_endpoint(websocket: WebSocket):
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
    await manager.connect(websocket, client_id)

    try:
        await manager.handle_research_stream(websocket, client_id)
    except Exception as e:
        await manager.send_json(
            client_id, {"event_type": "error", "data": {"message": f"Unexpected error: {str(e)}"}, "timestamp": None}
        )
    finally:
        manager.disconnect(client_id)
