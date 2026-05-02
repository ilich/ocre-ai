.PHONY: install run test
.DEFAULT_GOAL := run

install:
	uv sync

run:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	uv run ruff format .
	uv run ruff check --select I --fix .
	uv run ruff check .
	uv run mypy .
	uv run pytest -vv
	