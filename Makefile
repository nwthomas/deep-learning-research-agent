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

# Sync dependencies (for local development)
sync:
	uv sync