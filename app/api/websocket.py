"""WebSocket handler for streaming research results."""

import json
from typing import Any

from fastapi import WebSocket, WebSocketDisconnect
from langgraph.prebuilt import create_react_agent

from ..agents.agents import (
    BUILT_IN_TOOLS,
    RESEARCHER_MODEL,
    SUB_AGENT_RESEARCHER,
    SUB_AGENT_TOOLS,
    SUPERVISOR_MODEL,
)
from ..agents.utils import stream_agent_for_websocket
from ..prompts import SUPERVISOR_INSTRUCTIONS
from ..state import DeepAgentState
from ..tools import _create_task_tool
from .models import ResearchRequest


class WebSocketManager:
    """Manages WebSocket connections and research streaming."""

    def __init__(self) -> None:
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str) -> None:
        """Accept a WebSocket connection."""
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str) -> None:
        """Remove a WebSocket connection."""
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_json(self, client_id: str, data: dict[str, Any]) -> None:
        """Send JSON data to a specific client."""
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_text(json.dumps(data))
            except Exception:
                # Connection might be closed
                self.disconnect(client_id)

    async def handle_research_stream(self, websocket: WebSocket, client_id: str) -> None:
        """Handle the research streaming WebSocket connection."""
        try:
            # Wait for research request
            data = await websocket.receive_text()
            request_data = json.loads(data)
            request = ResearchRequest(**request_data)

            # Send acknowledgment
            await self.send_json(
                client_id,
                {
                    "event_type": "status_update",
                    "data": {
                        "graph": "system",
                        "node": "connection",
                        "status": "connected",
                        "message": f"Starting research for: {request.query}",
                    },
                },
            )

            # Create the agent
            current_task_tool = _create_task_tool(
                SUB_AGENT_TOOLS, [SUB_AGENT_RESEARCHER], RESEARCHER_MODEL, DeepAgentState
            )
            current_delegation_tools = [current_task_tool]
            current_all_tools = SUB_AGENT_TOOLS + BUILT_IN_TOOLS + current_delegation_tools

            agent = create_react_agent(
                SUPERVISOR_MODEL, current_all_tools, prompt=SUPERVISOR_INSTRUCTIONS, state_schema=DeepAgentState
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

            # Stream the research
            async for event in stream_agent_for_websocket(agent, query):
                await self.send_json(client_id, event)

        except WebSocketDisconnect:
            self.disconnect(client_id)
        except json.JSONDecodeError:
            await self.send_json(
                client_id, {"event_type": "error", "data": {"message": "Invalid JSON format"}, "timestamp": None}
            )
        except Exception as e:
            await self.send_json(
                client_id,
                {"event_type": "error", "data": {"message": f"Error processing request: {str(e)}"}, "timestamp": None},
            )
        finally:
            self.disconnect(client_id)


manager = WebSocketManager()
