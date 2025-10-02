# Run the FastAPI server
run:
	uv run python main.py

# Run the FastAPI server in development mode with reload
dev:
	uv run uvicorn app.api.server:app --host 0.0.0.0 --port 8000 --reload

# Sync the project
sync:
	uv sync