# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Server
```bash
# Start the server (builds image automatically)
make run
# or
docker compose up -d

# Start server with logs (development mode)
make dev
# or
docker compose up

# Stop the server
make stop
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
docker compose logs -f research-agent

# Access container shell
make shell
# or
docker compose exec research-agent /bin/bash

# Rebuild after code changes
docker compose up --build
```

### Dependencies
```bash
# Dependencies are managed through Docker
# To add new dependencies:
# 1. Add to pyproject.toml
# 2. Run: uv lock (if working locally)
# 3. Rebuild: docker compose up --build

# Install development dependencies locally
make install-dev
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

# Run all quality checks
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

**Docker Features:**
- Non-root execution (UID 1000) for security
- Health checks and auto-restart policies
- Optimized build with uv package manager and lock file
- Automatic dependency installation
- Ready for Helm/ArgoCD deployment in production

## Architecture Overview

This is a multi-agent deep learning research system built with LangChain and LangGraph. The architecture follows a supervisor-researcher pattern with virtual file system capabilities.

### Core Components

**Agent Architecture:**
- **Supervisor Agent** (`app/agents/agents.py`): Main orchestrating agent that manages task delegation and coordinates research
- **Research Sub-Agent**: Specialized agent for conducting web research and gathering information
- **State Management** (`app/state/state.py`): Extended LangGraph state with TODO tracking and virtual file system

**Key Features:**
- **Multi-Model Support**: Configurable supervisor and researcher models via environment variables
- **Virtual File System**: Research results stored in agent state as files for context offloading
- **TODO Tracking**: Built-in task planning and progress tracking through structured TODO lists
- **Parallel Research**: Ability to run multiple research sub-agents concurrently for complex queries

### Tools and Capabilities

**Research Tools** (`app/tools/research_tools.py`):
- `tavily_search`: Web search with content summarization and file storage
- `think_tool`: Strategic reflection and decision-making tool

**File Management** (`app/tools/file_tools.py`):
- `ls`: List files in virtual filesystem
- `read_file`: Read file content with pagination
- `write_file`: Create/overwrite files in virtual filesystem

**Task Management** (`app/tools/todo_tools.py`):
- `write_todos`: Create and manage structured task lists

### Configuration

**Environment Variables** (see `.env.example`):
- Supervisor model: `SUPERVISOR_MODEL_*` variables
- Researcher model: `RESEARCHER_MODEL_*` variables
- Research limits: `MAX_CONCURRENT_RESEARCH_UNITS`, `MAX_RESEARCHER_ITERATIONS`

**Model Configuration** (`app/constants.py`):
- Supports multiple providers via LangChain's `init_chat_model`
- Configurable API keys, base URLs, and model names
- Temperature set to 0.0 for deterministic responses

### Research Workflow

1. **Task Planning**: Supervisor creates TODO list based on user query
2. **Research Delegation**: Tasks delegated to specialized research sub-agents
3. **Information Gathering**: Sub-agents search web, summarize content, store in virtual files
4. **Strategic Reflection**: Regular use of `think_tool` for decision-making
5. **Result Synthesis**: Supervisor reads collected files and provides comprehensive answer

### Key Design Patterns

- **Context Offloading**: Large research content stored in virtual files to avoid context overflow
- **Structured State**: Custom state schema with TODO and file management
- **Agent Isolation**: Sub-agents operate with isolated context for parallel execution
- **Resource Management**: Built-in limits on concurrent agents and iteration counts
