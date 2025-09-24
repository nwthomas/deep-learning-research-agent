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