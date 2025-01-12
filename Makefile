PLATFORM := $(shell uname)

.PHONY: help
help: ## show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


.PHONY: run-client rc
run-client rc: ## Run the application in CLIENT mode
	@echo "Run the application with the CLIENT mode default parameter"
ifdef PLATFORM
	cd doccli && DOCCLI_MODE=client DOCCLI_ENDPOINT=http://localhost:8000 uv run main.py search
else
	SET "DOCCLI_MODE=client" && SET "DOCCLI_ENDPOINT=http://localhost:8000" && cd doccli && uv run doccli\main.py search /
endif


.PHONY: run-client-server rcs
run-client-server rcs: ## Run the application in CLIENT-SERVER mode
ifdef PLATFORM
	cd doccli && DOCCLI_MODE=client DOCCLI_SOURCE=os DOCCLI_BASE_DIR=/ uv run doccli/main.py search /
else
	SET "DOCCLI_MODE=client" && SET "DOCCLI_SOURCE=os" && SET "DOCCLI_BASE_DIR=C:/" && cd doccli && uv run doccli\main.py search /
endif


.PHONY: run-api ra
run-api ra: ## Run the application in SERVER mode
ifdef PLATFORM
	cd doccli && DOCCLI_MODE=client DOCCLI_SOURCE=os DOCCLI_BASE_DIR=/ uv run doccli/main.py
else
	SET "DOCCLI_MODE=client" && SET "DOCCLI_SOURCE=os" && SET "DOCCLI_BASE_DIR=C:/" && cd doccli && uv run doccli\main.py
endif