# Run the project
run:
	uv run python main.py $(if $(QUERY),--query "$(QUERY)") $(if $(LOCAL),--local)

# Sync the project
sync:
	uv sync