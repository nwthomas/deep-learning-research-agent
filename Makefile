# Catch-all rule to prevent make from using the package name as a target
%:
	@:

# Add a package to the project
add:
	uv add $(filter-out $@,$(MAKECMDGOALS))

# Run the project
run:
	uv run python main.py

# Sync the project
sync:
	uv sync

# Docker commands
docker-build:
	docker build -t deep-learning-research-agent .

docker-run:
	docker run --rm -it --env-file .env deep-learning-research-agent

docker-run-interactive:
	docker run --rm -it --env-file .env deep-learning-research-agent bash

docker-compose-up:
	docker-compose up --build

docker-compose-down:
	docker-compose down

docker-compose-logs:
	docker-compose logs -f

# Development with Docker
docker-dev:
	docker-compose up --build research-agent

# Clean up Docker resources
docker-clean:
	docker system prune -f
	docker image prune -f

# Helm commands
helm-lint:
	helm lint helm/deep-learning-research-agent

helm-template:
	helm template deep-learning-research-agent helm/deep-learning-research-agent

helm-dry-run:
	helm install deep-learning-research-agent helm/deep-learning-research-agent --dry-run --debug

helm-install:
	helm install deep-learning-research-agent helm/deep-learning-research-agent

helm-upgrade:
	helm upgrade deep-learning-research-agent helm/deep-learning-research-agent

helm-uninstall:
	helm uninstall deep-learning-research-agent

# Package Helm chart
helm-package:
	helm package helm/deep-learning-research-agent