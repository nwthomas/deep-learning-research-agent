"""Module: websocket.py

Description:
    WebSocket implementation for handling all communication between the server and clients.

Author: Nathan Thomas
"""

import asyncio
import json
from typing import Any

from fastapi import WebSocket, WebSocketDisconnect
from langgraph.prebuilt import create_react_agent

from ..agents import (
    BUILT_IN_TOOLS,
    RESEARCHER_MODEL,
    SUB_AGENT_RESEARCHER,
    SUB_AGENT_RESEARCHER_TOOLS,
    SUPERVISOR_INSTRUCTIONS,
    SUPERVISOR_MODEL,
    DeepAgentState,
    _create_task_tool,
    stream_agent_for_websocket,
)
from ..shared.config import app_config
from .models import ResearchRequest


class WebSocketManager:
    """Manages WebSocket connections and research streaming."""

    def __init__(self) -> None:
        self.active_connections: dict[str, WebSocket] = {}
        self.max_connections = app_config.MAX_CONCURRENT_CONNECTIONS
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, client_id: str) -> bool:
        """Accept a WebSocket connection. Returns True if successful, False if rejected."""
        async with self._lock:
            if len(self.active_connections) >= self.max_connections:
                await websocket.close(code=1013, reason="Server overloaded - too many connections")
                return False

            await websocket.accept()
            self.active_connections[client_id] = websocket
            return True

    async def disconnect(self, client_id: str) -> None:
        """Remove a WebSocket connection."""
        async with self._lock:
            if client_id in self.active_connections:
                del self.active_connections[client_id]

    async def get_connection_stats(self) -> dict[str, int]:
        """Get current connection statistics."""
        async with self._lock:
            return {
                "active_connections": len(self.active_connections),
                "max_connections": self.max_connections,
                "available_connections": self.max_connections - len(self.active_connections),
            }

    async def send_json(self, client_id: str, data: dict[str, Any]) -> None:
        """Send JSON data to a specific client."""
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_text(json.dumps(data))
            except Exception:
                # Connection might be closed
                await self.disconnect(client_id)

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
                SUB_AGENT_RESEARCHER_TOOLS, [SUB_AGENT_RESEARCHER], RESEARCHER_MODEL, DeepAgentState
            )
            current_delegation_tools = [current_task_tool]
            current_all_tools = SUB_AGENT_RESEARCHER_TOOLS + BUILT_IN_TOOLS + current_delegation_tools

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
            await self.disconnect(client_id)
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
            await self.disconnect(client_id)


manager = WebSocketManager()
