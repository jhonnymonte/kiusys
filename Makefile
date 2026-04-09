.PHONY: install run mock test up down logs format lint check

install:
	pip install -r requirements-dev.txt

run:
	uvicorn app.main:app --reload

mock:
	uvicorn mock.mock_server:app --port 8001 --reload

test:
	pytest tests/ -v

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

format:
	black .

lint:
	ruff check .

check: format lint

lint-fix:
	ruff check . --fix