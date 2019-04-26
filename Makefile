SHELL := /bin/bash

PIPENV := pipenv
PYTHON := python
YAPF := yapf

.PHONY: run
run: ## Run the script
	@echo "+ $@"
	./generate.py

.PHONY: install
install: Pipfile Pipfile.lock ## Install deps
	$(PIPENV) sync

.PHONY: venv
venv: ## Start a venv using pipenv
	@echo "+ $@"
	$(PIPENV) shell

.PHONY: lint
lint: ## Lint using yapf
	@echo "+ $@"
	yapf --verbose --in-place --recursive .

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | sed 's/^[^:]*://g' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

