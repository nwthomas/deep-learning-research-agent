"""Utility functions for displaying messages and prompts in Jupyter notebooks."""

import json
from datetime import datetime
from typing import Dict, Any, AsyncGenerator

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def format_message_content(message):
    """Convert message content to displayable string."""
    parts = []
    tool_calls_processed = False

    # Handle main content
    if isinstance(message.content, str):
        parts.append(message.content)
    elif isinstance(message.content, list):
        # Handle complex content like tool calls (Anthropic format)
        for item in message.content:
            if item.get("type") == "text":
                parts.append(item["text"])
            elif item.get("type") == "tool_use":
                parts.append(f"\n🔧 Tool Call: {item['name']}")
                parts.append(f"   Args: {json.dumps(item['input'], indent=2, ensure_ascii=False)}")
                parts.append(f"   ID: {item.get('id', 'N/A')}")
                tool_calls_processed = True
    else:
        parts.append(str(message.content))

    # Handle tool calls attached to the message (OpenAI format) - only if not already processed
    if (
        not tool_calls_processed
        and hasattr(message, "tool_calls")
        and message.tool_calls
    ):
        for tool_call in message.tool_calls:
            parts.append(f"\n🔧 Tool Call: {tool_call['name']}")
            parts.append(f"   Args: {json.dumps(tool_call['args'], indent=2, ensure_ascii=False)}")
            parts.append(f"   ID: {tool_call['id']}")

    return "\n".join(parts)


def format_messages(messages):
    """Format and display a list of messages with Rich formatting."""
    for m in messages:
        msg_type = m.__class__.__name__.replace("Message", "")
        content = format_message_content(m)

        if msg_type == "Human":
            console.print(Panel(content, title="🧑 Human", border_style="blue"))
        elif msg_type == "Ai":
            console.print(Panel(content, title="🤖 Assistant", border_style="green"))
        elif msg_type == "Tool":
            console.print(Panel(content, title="🔧 Tool Output", border_style="yellow"))
        else:
            console.print(Panel(content, title=f"📝 {msg_type}", border_style="white"))


def format_message(messages):
    """Alias for format_messages for backward compatibility."""
    return format_messages(messages)


def show_prompt(prompt_text: str, title: str = "Prompt", border_style: str = "blue"):
    """Display a prompt with rich formatting and XML tag highlighting.

    Args:
        prompt_text: The prompt string to display
        title: Title for the panel (default: "Prompt")
        border_style: Border color style (default: "blue")
    """
    # Create a formatted display of the prompt
    formatted_text = Text(prompt_text)
    formatted_text.highlight_regex(r"<[^>]+>", style="bold blue")  # Highlight XML tags
    formatted_text.highlight_regex(
        r"##[^#\n]+", style="bold magenta"
    )  # Highlight headers
    formatted_text.highlight_regex(
        r"###[^#\n]+", style="bold cyan"
    )  # Highlight sub-headers

    # Display in a panel for better presentation
    console.print(
        Panel(
            formatted_text,
            title=f"[bold green]{title}[/bold green]",
            border_style=border_style,
            padding=(1, 2),
        )
    )

# more expressive runner
async def stream_agent(agent, query, config=None):
    async for graph_name, stream_mode, event in agent.astream(
        query,
        stream_mode=["updates", "values"], 
        subgraphs=True,
        config=config
    ):
        if stream_mode == "updates":
            print(f'Graph: {graph_name if len(graph_name) > 0 else "root"}')
            
            node, result = list(event.items())[0]
            print(f'Node: {node}')
            
            for key in result.keys():
                if "messages" in key:
                    # print(f"Messages key: {key}")
                    format_messages(result[key])
                    break
        elif stream_mode == "values":
            current_state = event

    return current_state


async def stream_agent_for_websocket(agent, query, config=None) -> AsyncGenerator[Dict[str, Any], None]:
    """Stream agent execution and yield WebSocket events."""
    try:
        async for graph_name, stream_mode, event in agent.astream(
            query,
            stream_mode=["updates", "values"],
            subgraphs=True,
            config=config
        ):
            timestamp = datetime.now().isoformat()

            if stream_mode == "updates":
                node, result = list(event.items())[0]

                # Send status update
                yield {
                    "event_type": "status_update",
                    "data": {
                        "graph": graph_name if len(graph_name) > 0 else "root",
                        "node": node,
                        "status": "processing"
                    },
                    "timestamp": timestamp
                }

                # Process messages and tool calls
                for key in result.keys():
                    if "messages" in key:
                        for message in result[key]:
                            # Handle tool calls
                            if hasattr(message, "tool_calls") and message.tool_calls:
                                for tool_call in message.tool_calls:
                                    yield {
                                        "event_type": "tool_call",
                                        "data": {
                                            "tool_name": tool_call.get("name", "unknown"),
                                            "args": tool_call.get("args", {}),
                                            "tool_id": tool_call.get("id", "unknown")
                                        },
                                        "timestamp": timestamp
                                    }

                            # Handle Anthropic-style tool calls in content
                            if isinstance(message.content, list):
                                for item in message.content:
                                    if item.get("type") == "tool_use":
                                        yield {
                                            "event_type": "tool_call",
                                            "data": {
                                                "tool_name": item.get("name", "unknown"),
                                                "args": item.get("input", {}),
                                                "tool_id": item.get("id", "unknown")
                                            },
                                            "timestamp": timestamp
                                        }

                            # Handle text content
                            content = format_message_content(message)
                            if content and content.strip():
                                msg_type = message.__class__.__name__.replace("Message", "")
                                yield {
                                    "event_type": "result_chunk",
                                    "data": {
                                        "content": content,
                                        "message_type": msg_type,
                                        "node": node,
                                        "graph": graph_name if len(graph_name) > 0 else "root"
                                    },
                                    "timestamp": timestamp
                                }
                        break

            elif stream_mode == "values":
                current_state = event

        # Send completion event
        yield {
            "event_type": "completed",
            "data": {
                "message": "Research completed successfully",
                "final_state": "completed"
            },
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        # Send error event
        yield {
            "event_type": "error",
            "data": {
                "message": f"Agent execution failed: {str(e)}",
                "error_type": type(e).__name__
            },
            "timestamp": datetime.now().isoformat()
        }
