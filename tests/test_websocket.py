"""Module: test_websocket.py

Description:
    Test cases for WebSocket functionality including connection management,
    message handling, and research streaming capabilities.

Author: Nathan Thomas
"""

import asyncio
import json
from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from fastapi import WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from app.api.models import ResearchRequest
from app.api.websocket import WebSocketManager


class TestWebSocketManager:
    """Test cases for WebSocketManager class."""

    @pytest.fixture
    def manager(self) -> WebSocketManager:
        """Create a fresh WebSocketManager instance for each test."""

        return WebSocketManager()

    @pytest.fixture
    def mock_websocket(self) -> AsyncMock:
        """Create a mock WebSocket for testing."""

        mock = AsyncMock(spec=WebSocket)
        return mock

    @pytest.fixture
    def client_id(self) -> str:
        """Generate a unique client ID for testing."""

        return str(uuid4())

    @pytest.mark.asyncio
    async def test_init(self, manager: WebSocketManager) -> None:
        """Test WebSocketManager initialization."""

        assert manager.active_connections == {}
        assert manager.max_connections > 0
        assert manager._lock is not None

    @pytest.mark.asyncio
    async def test_connect_success(self, manager: WebSocketManager, mock_websocket: AsyncMock, client_id: str) -> None:
        """Test successful WebSocket connection."""

        result = await manager.connect(mock_websocket, client_id)

        assert result is True
        mock_websocket.accept.assert_called_once()
        assert client_id in manager.active_connections
        assert manager.active_connections[client_id] == mock_websocket

    @pytest.mark.asyncio
    async def test_connect_max_connections_reached(self, manager: WebSocketManager, client_id: str) -> None:
        """Test connection rejection when max connections is reached."""

        # Set max connections to 1 for testing
        manager.max_connections = 1

        # Connect first client successfully
        first_websocket = AsyncMock(spec=WebSocket)
        first_client_id = "client1"
        result1 = await manager.connect(first_websocket, first_client_id)
        assert result1 is True

        # Try to connect second client (should be rejected)
        second_websocket = AsyncMock(spec=WebSocket)
        second_client_id = "client2"
        result2 = await manager.connect(second_websocket, second_client_id)

        assert result2 is False
        second_websocket.close.assert_called_once_with(code=1013, reason="Server overloaded - too many connections")
        assert second_client_id not in manager.active_connections

    @pytest.mark.asyncio
    async def test_disconnect_existing_client(
        self, manager: WebSocketManager, mock_websocket: AsyncMock, client_id: str
    ) -> None:
        """Test disconnecting an existing client."""

        # First connect the client
        await manager.connect(mock_websocket, client_id)
        assert client_id in manager.active_connections

        # Then disconnect
        await manager.disconnect(client_id)

        mock_websocket.close.assert_called_once()
        assert client_id not in manager.active_connections

    @pytest.mark.asyncio
    async def test_disconnect_nonexistent_client(self, manager: WebSocketManager, client_id: str) -> None:
        """Test disconnecting a client that doesn't exist."""

        # Should not raise an exception
        await manager.disconnect(client_id)
        assert client_id not in manager.active_connections

    @pytest.mark.asyncio
    async def test_disconnect_websocket_close_exception(
        self, manager: WebSocketManager, mock_websocket: AsyncMock, client_id: str
    ) -> None:
        """Test disconnect when websocket.close() raises an exception."""

        # Connect first
        await manager.connect(mock_websocket, client_id)

        # Make close() raise an exception
        mock_websocket.close.side_effect = Exception("Connection already closed")

        # Disconnect should still work and remove from active connections
        await manager.disconnect(client_id)
        assert client_id not in manager.active_connections

    @pytest.mark.asyncio
    async def test_send_json_success(
        self, manager: WebSocketManager, mock_websocket: AsyncMock, client_id: str
    ) -> None:
        """Test successful JSON message sending."""

        # Connect first
        await manager.connect(mock_websocket, client_id)

        test_data = {"message": "test", "value": 42}
        await manager.send_json(client_id, test_data)

        mock_websocket.send_text.assert_called_once_with(json.dumps(test_data))

    @pytest.mark.asyncio
    async def test_send_json_nonexistent_client(self, manager: WebSocketManager, client_id: str) -> None:
        """Test sending JSON to a non-existent client."""

        test_data = {"message": "test"}

        # Should not raise an exception
        await manager.send_json(client_id, test_data)

    @pytest.mark.asyncio
    async def test_send_json_websocket_exception(
        self, manager: WebSocketManager, mock_websocket: AsyncMock, client_id: str
    ) -> None:
        """Test send_json when websocket raises an exception."""

        # Connect first
        await manager.connect(mock_websocket, client_id)

        # Make send_text raise an exception
        mock_websocket.send_text.side_effect = Exception("Connection lost")

        test_data = {"message": "test"}
        await manager.send_json(client_id, test_data)

        # Should have triggered disconnect
        assert client_id not in manager.active_connections

    @patch("app.api.websocket.stream_agent_for_websocket")
    @patch("app.api.websocket.create_react_agent")
    @patch("app.api.websocket._create_task_tool")
    @pytest.mark.asyncio
    async def test_handle_websocket_stream_valid_request(
        self,
        mock_create_task_tool: MagicMock,
        mock_create_react_agent: MagicMock,
        mock_stream_agent: AsyncMock,
        manager: WebSocketManager,
        mock_websocket: AsyncMock,
        client_id: str,
    ) -> None:
        """Test handling a valid research request."""

        # Setup mocks
        mock_agent = MagicMock()
        mock_create_react_agent.return_value = mock_agent

        async def mock_stream() -> AsyncGenerator[dict[str, Any], None]:
            yield {"event_type": "test", "data": {"message": "test"}}

        mock_stream_agent.return_value = mock_stream()

        # Setup websocket to receive valid request
        valid_request = {"query": "What is machine learning?"}
        mock_websocket.receive_text.side_effect = [
            json.dumps(valid_request),
            WebSocketDisconnect(),  # End the loop
        ]

        # Connect the websocket first
        await manager.connect(mock_websocket, client_id)

        # Handle the stream
        await manager.handle_websocket_stream(mock_websocket, client_id)

        # Verify the agent was created and called
        mock_create_react_agent.assert_called_once()
        mock_stream_agent.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_websocket_stream_invalid_request(
        self, manager: WebSocketManager, mock_websocket: AsyncMock, client_id: str
    ) -> None:
        """Test handling an invalid research request (missing query)."""

        # Setup websocket to receive invalid request
        invalid_request = {"not_query": "invalid"}
        mock_websocket.receive_text.side_effect = [json.dumps(invalid_request), WebSocketDisconnect()]

        # Connect the websocket first
        await manager.connect(mock_websocket, client_id)

        # Handle the stream
        await manager.handle_websocket_stream(mock_websocket, client_id)

        # Verify error message was sent
        mock_websocket.send_text.assert_called()
        sent_data = json.loads(mock_websocket.send_text.call_args[0][0])
        assert sent_data["event_type"] == "error"
        assert "Invalid researcy request" in sent_data["data"]["message"]

    @pytest.mark.asyncio
    async def test_handle_websocket_stream_empty_request(
        self, manager: WebSocketManager, mock_websocket: AsyncMock, client_id: str
    ) -> None:
        """Test handling an empty request."""

        mock_websocket.receive_text.side_effect = [json.dumps({}), WebSocketDisconnect()]

        await manager.connect(mock_websocket, client_id)
        await manager.handle_websocket_stream(mock_websocket, client_id)

        # Verify error message was sent
        mock_websocket.send_text.assert_called()
        sent_data = json.loads(mock_websocket.send_text.call_args[0][0])
        assert sent_data["event_type"] == "error"

    @pytest.mark.asyncio
    async def test_handle_websocket_stream_json_decode_error(
        self, manager: WebSocketManager, mock_websocket: AsyncMock, client_id: str
    ) -> None:
        """Test handling invalid JSON in request."""

        mock_websocket.receive_text.side_effect = ["invalid json", WebSocketDisconnect()]

        await manager.connect(mock_websocket, client_id)
        await manager.handle_websocket_stream(mock_websocket, client_id)

        # Verify JSON error message was sent
        mock_websocket.send_text.assert_called()
        sent_data = json.loads(mock_websocket.send_text.call_args[0][0])
        assert sent_data["event_type"] == "error"
        assert "Invalid JSON format" in sent_data["data"]["message"]

    @pytest.mark.asyncio
    async def test_handle_websocket_stream_websocket_disconnect(
        self, manager: WebSocketManager, mock_websocket: AsyncMock, client_id: str
    ) -> None:
        """Test handling WebSocket disconnect during stream."""

        mock_websocket.receive_text.side_effect = WebSocketDisconnect()

        await manager.connect(mock_websocket, client_id)
        await manager.handle_websocket_stream(mock_websocket, client_id)

        # Should have removed the client from active connections
        assert client_id not in manager.active_connections

    @patch("app.api.websocket.stream_agent_for_websocket")
    @patch("app.api.websocket.create_react_agent")
    @patch("app.api.websocket._create_task_tool")
    @pytest.mark.asyncio
    async def test_handle_websocket_stream_general_exception(
        self,
        mock_create_task_tool: MagicMock,
        mock_create_react_agent: MagicMock,
        mock_stream_agent: AsyncMock,
        manager: WebSocketManager,
        mock_websocket: AsyncMock,
        client_id: str,
    ) -> None:
        """Test handling general exception during stream processing."""

        # Make agent creation raise an exception
        mock_create_react_agent.side_effect = Exception("Agent creation failed")

        valid_request = {"query": "test query"}
        mock_websocket.receive_text.side_effect = [json.dumps(valid_request), WebSocketDisconnect()]

        await manager.connect(mock_websocket, client_id)
        await manager.handle_websocket_stream(mock_websocket, client_id)

        # Verify error message was sent
        mock_websocket.send_text.assert_called()
        sent_data = json.loads(mock_websocket.send_text.call_args[0][0])
        assert sent_data["event_type"] == "error"
        assert "Error processing request" in sent_data["data"]["message"]

    @pytest.mark.asyncio
    async def test_concurrent_connections(self, manager: WebSocketManager) -> None:
        """Test handling multiple concurrent connections."""

        # Create multiple mock websockets
        websockets = [AsyncMock(spec=WebSocket) for _ in range(3)]
        client_ids = [f"client_{i}" for i in range(3)]

        # Connect all simultaneously
        tasks = [manager.connect(ws, client_id) for ws, client_id in zip(websockets, client_ids, strict=False)]
        results = await asyncio.gather(*tasks)

        # All should connect successfully
        assert all(results)
        assert len(manager.active_connections) == 3

        # All websockets should have accepted
        for ws in websockets:
            ws.accept.assert_called_once()

    def test_research_request_validation(self) -> None:
        """Test ResearchRequest model validation."""

        # Valid request
        valid_data = {"query": "What is AI?"}
        request = ResearchRequest(**valid_data)
        assert request.query == "What is AI?"

        # Invalid request (missing query)
        with pytest.raises(ValidationError):  # Pydantic validation error
            ResearchRequest(**{})

    @pytest.mark.asyncio
    async def test_manager_instance_isolation(self) -> None:
        """Test that different manager instances are isolated."""

        manager1 = WebSocketManager()
        manager2 = WebSocketManager()

        # They should have separate connection dictionaries
        assert manager1.active_connections is not manager2.active_connections

        # Adding to one shouldn't affect the other
        mock_ws = AsyncMock(spec=WebSocket)
        await manager1.connect(mock_ws, "test_client")

        assert len(manager1.active_connections) == 1
        assert len(manager2.active_connections) == 0

    @pytest.mark.asyncio
    async def test_send_json_data_serialization(
        self, manager: WebSocketManager, mock_websocket: AsyncMock, client_id: str
    ) -> None:
        """Test that complex data structures are properly serialized."""

        await manager.connect(mock_websocket, client_id)

        complex_data = {
            "timestamp": datetime.now(UTC).isoformat(),
            "nested": {"key": "value", "number": 42},
            "list": [1, 2, "three"],
            "boolean": True,
        }

        await manager.send_json(client_id, complex_data)

        # Verify the data was serialized correctly
        mock_websocket.send_text.assert_called_once()
        sent_text = mock_websocket.send_text.call_args[0][0]

        # Should be valid JSON
        parsed_data = json.loads(sent_text)
        assert parsed_data == complex_data
