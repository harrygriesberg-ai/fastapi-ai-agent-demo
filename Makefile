.PHONY: install run test lint check
install:
	pip install -e ".[dev]"
run:
	uvicorn app.main:app --reload
test:
	pytest --cov=app --cov-report=term-missing
lint:
	ruff check .
check: lint test
