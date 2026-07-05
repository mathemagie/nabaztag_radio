WEB  ?= web
PORT ?= 8000
URL  := http://localhost:$(PORT)/

.DEFAULT_GOAL := help

.PHONY: help view open

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN{FS=":.*## "}{printf "  \033[36m%-8s\033[0m %s\n", $$1, $$2}'

view: ## Serve web/ locally and open it in the browser (Ctrl-C to stop)
	@echo "→ Serving $(WEB)/ at $(URL)  (Ctrl-C to stop)"
	@( sleep 1 && open "$(URL)" ) &
	@python3 -m http.server $(PORT) --directory $(WEB)

open: ## Just open web/index.html directly (no server)
	@open "$(WEB)/index.html"
