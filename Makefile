.PHONY: run-update-cli run-update-api run-cli run-api

# Cible pour exécuter l'application CLI
run-cli:
	@echo "Running CLI application..."
	cd CLI && uv run CLI search /

# Cible pour exécuter l'application backend
run-api:
	@echo "Running Backend application..."
	cd API && uv run -- fastapi dev API/main.py

# Cible pour exécuter l'application CLI
run-update-cli:
	@echo "Running CLI application..."
	cd CLI && uv add ../shared --reinstall && uv run CLI search /

# Cible pour exécuter l'application backend
run-update-api:
	@echo "Running Backend application..."
	cd API && uv add ../shared --reinstall && uv run -- fastapi dev API/main.py

