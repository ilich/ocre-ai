.PHONY: install run test
.DEFAULT_GOAL := run

install:
	uv sync

run:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

seed:
	uv run python -m app.cli seed "../../datasets/ocre20251021.json"

embed:
	uv run python -m app.cli embed-coins

test:
	uv run ruff format .
	uv run ruff check --select I --fix .
	uv run ruff check .
	uv run mypy .
	uv run pytest -vv
	