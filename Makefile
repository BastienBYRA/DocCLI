.PHONY: run-cli run-backend build-shared

# Cible pour construire le module partagé
build-shared:
	@echo "Building shared module..."
	cd shared && uv build

# Cible pour exécuter l'application CLI
run-cli: build-shared
	@echo "Running CLI application..."
	cd CLI && uv add -U ../shared && uv run -- ./doccli

# Cible pour exécuter l'application backend (si nécessaire)
run-backend: build-shared
	@echo "Running Backend application..."
	cd backend && uv add -U ../shared && uv run -- ./backend
