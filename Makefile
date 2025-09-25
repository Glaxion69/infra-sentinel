
.PHONY: init lint test demo

init:
	python -m venv .venv && . .venv/bin/activate && pip install -e .[dev]

lint:
	flake8 src tests

test:
	pytest

demo:
	infra-sentinel run --config config/sentinel.yaml --events demo/events.jsonl --dry-run
