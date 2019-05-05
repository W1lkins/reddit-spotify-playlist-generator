SHELL := /bin/bash

PIP := pip
PYTHON := python
TEST := python -m unittest -v
VENV := virtualenv venv
LINT := black

.PHONY: run
run: ## Run the script
	@echo "+ $@"
	./generate.py

.PHONY: install
install: requirements.txt ## Install deps
	$(PIP) install -r requirements.txt

.PHONY: virtual
virtual: ## Start a venv using virtualenv
	@echo "+ $@"
	$(VENV)

.PHONY: lint
lint: ## Lint using yapf
	@echo "+ $@"
	$(LINT) generate.py subreddit_to_playlist

.PHONY: test
test: ## Run the tests
	@echo "+ $@"
	$(TEST) tests/*test.py

.PHONY: help
help:
	@awk -F ':|##' '/^[^\t].+?:.*?##/ { printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF }' $(MAKEFILE_LIST)
