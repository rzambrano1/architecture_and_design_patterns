.PHONY: help install test lint format tox coverage run up down rebuild logs shell clean db psql

help:
	@echo "Available commands:"
	@echo "  make install     Install dependencies"
	@echo "  make test        Run pytest"
	@echo "  make tox         Run tox environments"
	@echo "  make lint        Run lint checks"
	@echo "  make fast_lint   Run lint checks but skips ruff"
	@echo "  make format      Auto-format code"
	@echo "  make coverage    Run tests with coverage"
	@echo "  make run         Run Flask app locally"
	@echo "  make up          Start docker services"
	@echo "  make down        Stop docker services"
	@echo "  make rebuild     Rebuild docker images"
	@echo "  make logs        View docker logs"
	@echo "  make shell       Open shell in app container"
	@echo "  make db          Connect to Postgres shell"
	@echo "  make clean       Cleanup caches"

install:
	pip install -e ".[dev]"

test:
	pytest

tox:
	tox

lint:
	black --check src test
	ruff check src test
	mypy src

fast_lint:
    black --check src test
	mypy src

format:
	black src test
	ruff check --fix src test

coverage:
	pytest --cov=src --cov-report=term-missing --cov-report=html

run:
	flask run --host=0.0.0.0 --port=5000

up:
	docker compose up -d

down:
	docker compose down

rebuild:
	docker compose build --no-cache

logs:
	docker compose logs -f

shell:
	docker compose exec app bash

db:
	docker compose exec postgres psql -U batch_allocation -d batch_allocation

psql:
	psql -h localhost -p 54321 -U batch_allocation batch_allocation

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache .tox htmlcov **/__pycache__
