.PHONY: run dev stop logs shell rebuild sync sync-dev lint format format-check typecheck test check fix install-hooks run-hooks clean

up-d: # Start the server in detached mode
	docker compose up -d

up: # Start the server with logs (development mode)
	docker compose up --build

down: # Stop the server
	docker compose down

logs: # View logs
	docker compose logs -f deep-learning-research-agent

shell: # Access container shell
	docker compose exec deep-learning-research-agent /bin/bash

rebuild: # Rebuild and start
	docker compose up --build

sync: # Sync dependencies
	uv sync

sync-dev: # Sync dependencies (for local development)
	uv sync --extra dev

lint: # Lint check the codebase
	uv run ruff check .

format: # Format check the codebase
	uv run ruff format .

format-check: # Format check the codebase
	uv run ruff format --check .

typecheck: # Type check the codebase
	uv run mypy .

test: # Run tests
	uv run pytest tests/ -v

check: lint format-check typecheck test # Combined quality checks
	@echo "All quality checks passed!"

fix: format lint # Format and lint code
	@echo "Code formatted and linted!"

install-hooks: # Install pre-commit hooks
	uv run pre-commit install

run-hooks: # Run pre-commit hooks
	uv run pre-commit run --all-files

clean: # Clean up
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
