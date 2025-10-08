# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Server
```bash
# Start the server (builds image automatically)
make up-d
# or
docker compose up -d

# Start server with logs (development mode)
make up
# or
docker compose up

# Stop the server
make down
# or
docker compose down
```

**Server Endpoints:**
- Health check: `GET http://localhost:8000/health`
- WebSocket research: `ws://localhost:8000/ws/research`

### Development Workflow
```bash
# View logs
make logs
# or
docker compose logs -f app

# Access container shell
make shell
# or
docker compose exec app /bin/bash

# Rebuild after code changes
docker compose up --build
```

### Dependencies
```bash
# Dependencies are managed through Docker and uv
# To add new dependencies:
# 1. Add to pyproject.toml
# 2. Run: uv lock (if working locally)
# 3. Rebuild: docker compose up --build

# Install development dependencies locally
make sync-dev
# or
uv sync --extra dev
```

### Code Quality and Development Tools
```bash
# Format code
make format
# or
uv run ruff format .

# Lint code
make lint
# or
uv run ruff check .

# Type check
make typecheck
# or
uv run mypy .

# Run tests
make test
# or
uv run pytest tests/ -v

# Run all quality checks (includes tests)
make check

# Format and lint (fix issues)
make fix

# Install pre-commit hooks
make install-hooks
# or
uv run pre-commit install

# Run pre-commit hooks manually
make run-hooks
# or
uv run pre-commit run --all-files

# Clean cache files
make clean
```

**Docker Configuration:**
- Service name: `app` (container: `deep-learning-research-agent`)
- Exposes port 8000 for API access
- Health checks with auto-restart policies
- Volume mounts for live development
- Environment variable configuration via `.env` file

## Architecture Overview

This is a multi-agent deep learning research system built with LangChain and LangGraph. The architecture follows a supervisor-researcher pattern with virtual file system capabilities and real-time WebSocket streaming.

### Core Components

**Agent Architecture:**
- **Supervisor Agent** (`app/agents/agents.py`): Main orchestrating agent that manages task delegation and coordinates research
- **Research Sub-Agent**: Specialized agent for conducting web research and gathering information
- **State Management** (`app/agents/state.py`): Extended LangGraph state with TODO tracking and virtual file system
- **WebSocket Server** (`app/api/server.py`, `app/api/websocket.py`): Real-time streaming API for research interactions

**Key Features:**
- **Multi-Model Support**: Configurable supervisor and researcher models via environment variables
- **Virtual File System**: Research results stored in agent state as files for context offloading
- **TODO Tracking**: Built-in task planning and progress tracking through structured TODO lists
- **Real-time Streaming**: WebSocket-based streaming of research progress and results
- **Parallel Research**: Ability to run multiple research sub-agents concurrently for complex queries

### Tools and Capabilities

**Research Tools** (`app/agents/tools/research_tools.py`):
- `tavily_search`: Web search with content summarization and file storage
- `think_tool`: Strategic reflection and decision-making tool

**File Management** (`app/agents/tools/file_tools.py`):
- `ls`: List files in virtual filesystem
- `read_file`: Read file content with pagination
- `write_file`: Create/overwrite files in virtual filesystem

**Task Management** (`app/agents/tools/todo_tools.py`):
- `write_todos`: Create and manage structured task lists

**Task Delegation** (`app/agents/tools/task_tool.py`):
- Dynamic sub-agent creation and management
- Parallel task execution capabilities

### Configuration

**Environment Variables** (see `.env.example`):
- Server settings: `APP_*` variables (host, port, debug mode)
- Supervisor model: `SUPERVISOR_MODEL_*` variables
- Researcher model: `RESEARCHER_MODEL_*` variables
- Research limits: `MAX_CONCURRENT_RESEARCH_UNITS`, `MAX_RESEARCHER_ITERATIONS`
- WebSocket limits: `MAX_CONCURRENT_CONNECTIONS`
- External APIs: `TAVILY_API_KEY`, `LANGSMITH_*` variables

**Model Configuration** (`app/agents/agents.py:build_chat_model`):
- Supports multiple providers via LangChain's `init_chat_model`
- Configurable API keys, base URLs, and model names
- Temperature set to 0.0 for deterministic responses
- Supports Anthropic, OpenAI, Ollama, and other providers

### Research Workflow

1. **WebSocket Connection**: Client connects to `/ws/research` endpoint
2. **Query Processing**: User sends research query via WebSocket
3. **Task Planning**: Supervisor creates TODO list based on user query
4. **Research Delegation**: Tasks delegated to specialized research sub-agents
5. **Information Gathering**: Sub-agents search web, summarize content, store in virtual files
6. **Strategic Reflection**: Regular use of `think_tool` for decision-making
7. **Real-time Updates**: Progress streamed back to client via WebSocket events
8. **Result Synthesis**: Supervisor reads collected files and provides comprehensive answer

### WebSocket API Events

- `status_update`: Progress updates (graph, node, status)
- `tool_call`: When agents call tools (tool_name, args, tool_id)
- `result_chunk`: Streaming content chunks (content, message_type)
- `completed`: Final completion event (final_result, total_messages)
- `error`: Error events (message)

### Key Design Patterns

- **Context Offloading**: Large research content stored in virtual files to avoid context overflow
- **Structured State**: Custom state schema with TODO and file management
- **Agent Isolation**: Sub-agents operate with isolated context for parallel execution
- **Resource Management**: Built-in limits on concurrent agents and iteration counts
- **Streaming Architecture**: Real-time progress updates via WebSocket connections
