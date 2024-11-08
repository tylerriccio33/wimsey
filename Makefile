test: ## Run pytest
	@uv run pytest

cov: ## Run coverage
	@uv run pytest --cov --cov-report term-missing