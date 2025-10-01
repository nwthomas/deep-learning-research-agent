# Run the project
run:
	uv run python main.py $(if $(QUERY),--query "$(QUERY)")

# Sync the project
sync:
	uv sync