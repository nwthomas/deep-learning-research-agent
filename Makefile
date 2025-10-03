# Start the server in detached mode
run:
	docker compose up -d

# Start the server with logs (development mode)
dev:
	docker compose up

# Stop the server
stop:
	docker compose down

# View logs
logs:
	docker compose logs -f research-agent

# Access container shell
shell:
	docker compose exec research-agent /bin/bash

# Rebuild and start
rebuild:
	docker compose up --build

# Sync dependencies
sync:
	uv sync

# Sync dependencies (for local development)
sync-dev:
	uv sync --extra dev

# Lint check the codebase
lint:
	uv run ruff check .

# Format check the codebase
format:
	uv run ruff format .

# Format check the codebase
format-check:
	uv run ruff format --check .

# Type check the codebase
typecheck:
	uv run mypy .

# Combined quality checks
check: lint format-check typecheck
	@echo "All quality checks passed!"

fix: format lint
	@echo "Code formatted and linted!"

# Install pre-commit hooks
install-hooks:
	uv run pre-commit install

# Run pre-commit hooks
run-hooks:
	uv run pre-commit run --all-files

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

.PHONY: run dev stop logs shell rebuild sync sync-dev lint format format-check typecheck check fix install-hooks run-hooks clean
