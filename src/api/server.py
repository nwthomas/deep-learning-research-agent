"""FastAPI server for the deep learning research agent."""

import uuid
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent

from ..agents.agents import (
    SUPERVISOR_MODEL,
    RESEARCHER_MODEL,
    SUB_AGENT_TOOLS,
    SUB_AGENT_RESEARCHER,
    BUILT_IN_TOOLS,
)
from ..tools import _create_task_tool
from ..prompts import SUPERVISOR_INSTRUCTIONS
from ..state import DeepAgentState
from .models import ResearchRequest, ResearchResponse
from .websocket import manager

# Create FastAPI app
app = FastAPI(
    title="Deep Learning Research Agent API",
    description="API for conducting deep learning research with streaming capabilities",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
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

@app.post("/research", response_model=ResearchResponse)
async def research_endpoint(request: ResearchRequest):
    """
    Non-streaming research endpoint for clients that don't support WebSockets.

    This endpoint runs the complete research process and returns the final result.
    For real-time streaming, use the WebSocket endpoint at /ws/research.
    """
    try:
        # Create the agent
        current_task_tool = _create_task_tool(
            SUB_AGENT_TOOLS, [SUB_AGENT_RESEARCHER], RESEARCHER_MODEL, DeepAgentState
        )
        current_delegation_tools = [current_task_tool]
        current_all_tools = SUB_AGENT_TOOLS + BUILT_IN_TOOLS + current_delegation_tools

        agent = create_react_agent(
            SUPERVISOR_MODEL,
            current_all_tools,
            prompt=SUPERVISOR_INSTRUCTIONS,
            state_schema=DeepAgentState
        )

        # Prepare query
        query = {
            "messages": [
                {
                    "role": "user",
                    "content": request.query,
                }
            ],
        }

        # Run the agent and collect all results
        result_parts = []
        async for graph_name, stream_mode, event in agent.astream(
            query,
            stream_mode=["updates", "values"],
            subgraphs=True
        ):
            if stream_mode == "updates":
                node, result = list(event.items())[0]
                for key in result.keys():
                    if "messages" in key:
                        for message in result[key]:
                            # Extract content from messages
                            if hasattr(message, 'content') and isinstance(message.content, str):
                                if message.content.strip():
                                    result_parts.append(message.content)

        # Combine all results
        final_result = "\n\n".join(result_parts) if result_parts else "Research completed with no textual output."

        return ResearchResponse(
            query=request.query,
            result=final_result,
            status="completed"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research failed: {str(e)}")

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
        await manager.send_json(client_id, {
            "event_type": "error",
            "data": {"message": f"Unexpected error: {str(e)}"},
            "timestamp": None
        })
    finally:
        manager.disconnect(client_id)
