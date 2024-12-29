.PHONY: run-cli run-api

# Cible pour exécuter l'application CLI
run-cli:
	@echo "Running CLI application..."
	cd CLI && uv add ../shared --reinstall && uv run CLI search /

# Cible pour exécuter l'application backend
run-api:
	@echo "Running Backend application..."
	cd API && uv add ../shared --reinstall && uv run backend