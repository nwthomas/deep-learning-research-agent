# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Agent
```bash
# Run with query (required)
make run QUERY="your research question here"

# Direct execution
uv run python main.py --query "your research question here"
```

### Dependencies
```bash
# Sync dependencies
make sync
# or
uv sync

# Add new dependencies
uv add package-name
```

## Architecture Overview

This is a multi-agent deep learning research system built with LangChain and LangGraph. The architecture follows a supervisor-researcher pattern with virtual file system capabilities.

### Core Components

**Agent Architecture:**
- **Supervisor Agent** (`src/agents/agents.py`): Main orchestrating agent that manages task delegation and coordinates research
- **Research Sub-Agent**: Specialized agent for conducting web research and gathering information
- **State Management** (`src/state/state.py`): Extended LangGraph state with TODO tracking and virtual file system

**Key Features:**
- **Multi-Model Support**: Configurable supervisor and researcher models via environment variables
- **Virtual File System**: Research results stored in agent state as files for context offloading
- **TODO Tracking**: Built-in task planning and progress tracking through structured TODO lists
- **Parallel Research**: Ability to run multiple research sub-agents concurrently for complex queries

### Tools and Capabilities

**Research Tools** (`src/tools/research_tools.py`):
- `tavily_search`: Web search with content summarization and file storage
- `think_tool`: Strategic reflection and decision-making tool

**File Management** (`src/tools/file_tools.py`):
- `ls`: List files in virtual filesystem
- `read_file`: Read file content with pagination
- `write_file`: Create/overwrite files in virtual filesystem

**Task Management** (`src/tools/todo_tools.py`):
- `write_todos`: Create and manage structured task lists

### Configuration

**Environment Variables** (see `.env.example`):
- Supervisor model: `SUPERVISOR_MODEL_*` variables
- Researcher model: `RESEARCHER_MODEL_*` variables
- Research limits: `MAX_CONCURRENT_RESEARCH_UNITS`, `MAX_RESEARCHER_ITERATIONS`

**Model Configuration** (`src/constants.py`):
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