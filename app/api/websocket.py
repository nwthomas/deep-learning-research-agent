"""Module: websocket.py

Description:
    WebSocket implementation for handling all communication between the server and clients.

Author: Nathan Thomas
"""

import asyncio
import json
from datetime import UTC, datetime
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
    """Wraps the native Websocket connection and offers up an API for managing these connections and streams."""

    def __init__(self) -> None:
        self.active_connections: dict[str, WebSocket] = {}
        self.max_connections = app_config.MAX_CONCURRENT_WEBSOCKET_CONNECTIONS
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, client_id: str) -> bool:
        """Accept a WebSocket connection. Returns True if successful, False if rejected.

        Args:
            websocket (WebSocket): The websocket connection
            client_id (str): The client ID

        Returns:
            bool: True if successful, False if rejected
        """

        async with self._lock:
            if len(self.active_connections) >= self.max_connections:
                await websocket.close(code=1013, reason="Server overloaded - too many connections")
                return False

            await websocket.accept()
            self.active_connections[client_id] = websocket

            return True

    async def disconnect(self, client_id: str) -> None:
        """Remove a WebSocket connection.

        Args:
            client_id (str): The client ID
        """

        async with self._lock:
            if client_id in self.active_connections:
                websocket = self.active_connections[client_id]

                try:
                    await websocket.close()
                except Exception:
                    # Connection might already be closed. Simply pass on and remove from the active conneciton list.
                    pass
                finally:
                    del self.active_connections[client_id]

    async def send_json(self, client_id: str, data: dict[str, Any]) -> None:
        """Send JSON data to a specific client.

        Args:
            client_id (str): The client ID
            data (dict[str, Any]): The data to send
        """

        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_text(json.dumps(data))
            except Exception:
                await self.disconnect(client_id)
        # TODO: Add logging for not found client_id here

    async def handle_websocket_stream(self, websocket: WebSocket, client_id: str) -> None:
        """Handle the research streaming WebSocket connection.

        Args:
            websocket (WebSocket): The websocket connection
            client_id (str): The client ID
        """

        try:
            while True:
                data = await websocket.receive_text()
                request_data = json.loads(data)

                # TODO: This can be modified later to support multiple other request types via the websocket.
                if not request_data or not request_data.get("query"):
                    await self.send_json(
                        client_id,
                        {
                            "event_type": "error",
                            "data": {"message": "Invalid researcy request"},
                            "timestamp": datetime.now(UTC).isoformat(),
                        },
                    )
                    continue
                request = ResearchRequest(**request_data)

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
                        "timestamp": datetime.now(UTC).isoformat(),
                    },
                )

                # TODO: This can be refactored later to its own helper functions surrounding agents
                current_task_tool = _create_task_tool(
                    SUB_AGENT_RESEARCHER_TOOLS, [SUB_AGENT_RESEARCHER], RESEARCHER_MODEL, DeepAgentState
                )
                current_delegation_tools = [current_task_tool]
                current_all_tools = SUB_AGENT_RESEARCHER_TOOLS + BUILT_IN_TOOLS + current_delegation_tools
                supervisor_agent = create_react_agent(
                    SUPERVISOR_MODEL, current_all_tools, prompt=SUPERVISOR_INSTRUCTIONS, state_schema=DeepAgentState
                )

                query = {
                    "messages": [
                        {
                            "role": "user",
                            "content": request.query,
                        }
                    ],
                }

                async for event in stream_agent_for_websocket(supervisor_agent, query):
                    await self.send_json(client_id, event)

        except WebSocketDisconnect:
            await self.disconnect(client_id)
        except json.JSONDecodeError:
            await self.send_json(
                client_id,
                {
                    "event_type": "error",
                    "data": {"message": "Invalid JSON format"},
                    "timestamp": datetime.now(UTC).isoformat(),
                },
            )
        except Exception as e:
            await self.send_json(
                client_id,
                {
                    "event_type": "error",
                    "data": {"message": f"Error processing request: {str(e)}"},
                    "timestamp": datetime.now(UTC).isoformat(),
                },
            )


manager = WebSocketManager()
