"""Pydantic models for FastAPI request/response validation."""

from typing import Dict, Any, Optional
from pydantic import BaseModel
from enum import Enum

class EventType(str, Enum):
    """Types of WebSocket events sent during research streaming."""
    STATUS_UPDATE = "status_update"
    TOOL_CALL = "tool_call"
    RESEARCH_PROGRESS = "research_progress"
    RESULT_CHUNK = "result_chunk"
    COMPLETED = "completed"
    ERROR = "error"

class ResearchRequest(BaseModel):
    """Request model for research queries."""
    query: str

class ResearchResponse(BaseModel):
    """Response model for completed research."""
    query: str
    result: str
    status: str = "completed"

class WebSocketEvent(BaseModel):
    """Base model for WebSocket events during streaming."""
    event_type: EventType
    data: Dict[str, Any]
    timestamp: Optional[str] = None

class ToolCallEvent(BaseModel):
    """Model for tool call events."""
    tool_name: str
    args: Dict[str, Any]
    tool_id: str

class StatusUpdateEvent(BaseModel):
    """Model for status update events."""
    graph: str
    node: str
    status: str

class ResultChunkEvent(BaseModel):
    """Model for streaming result chunks."""
    content: str
    message_type: str

class CompletedEvent(BaseModel):
    """Model for completion events."""
    final_result: str
    total_messages: int
