# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
| Command | Purpose |
|---------|---------|
| `pip install -r requirements.txt` or `uv sync` | Install dependencies (ipykernel, langchain, langgraph, etc.) |
| `python main.py` | Launch the REPL‑style agent interactions |
| `uv test` | Run the test suite (if tests are added) |
| `make run` | Run the agent via Makefile |

## Makefile Extras
- `make sync` – Sync the project dependencies (`uv sync`).
- `make add` – Add a package to the project (`uv add ...`).
- `make docker-build` – Build the Docker image.
- `make docker-run` – Run the Docker container.
- `make docker-run-interactive` – Run the Docker container interactively.
- `make docker-compose-up` – Start services defined in docker‑compose.
- `make docker-compose-down` – Stop services.
- `make docker-clean` – Clean up Docker resources.
- `make helm-lint` – Lint Helm charts.
- `make helm-template` – Render Helm templates.
- `make helm-install` – Install the Helm chart.
- `make helm-upgrade` – Upgrade the Helm chart.
- `make helm-uninstall` – Uninstall the Helm chart.
- `make helm-package` – Package the Helm chart.

## High‑Level Architecture
- **main.py** imports `load_dotenv` and calls `run_agent` from `src`.
- **src/agents.py** defines the root react agent using LangGraph and LangChain, providing built‑in tools (`ls`, `read_file`, `write_file`, `write_todos`, `think_tool`) and a research sub‑agent that can execute web search via `tavily_search`.
- **src/state.py** holds the virtual filesystem and TODO list.
- **src/file_tools.py** implements filesystem operations for the virtual FS.
- **src/research_tools.py** wraps Tavily web search and a `think_tool` helper.
- **src/todo_tools.py** exposes `write_todos` for the agent to add tasks.
-
The agent runs in a React‑style loop, delegating research tasks to a sub‑agent or performing file edits directly.

Please keep this file up to date as the project evolves.
