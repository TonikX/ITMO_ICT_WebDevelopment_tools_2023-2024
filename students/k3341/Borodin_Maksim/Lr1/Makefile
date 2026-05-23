PYTHON=.venv/bin/python
PIP=.venv/bin/pip
ALEMBIC=.venv/bin/alembic
UVICORN=.venv/bin/uvicorn

.PHONY: install up-db down-db migrate run up openapi

install:
	python3 -m venv .venv
	$(PIP) install -r requirements.txt
	cp -n .env.example .env || true

up-db:
	docker compose up -d db
	docker compose exec -T db sh -c "until pg_isready -U postgres -d time_manager_db; do sleep 1; done"

down-db:
	docker compose down

migrate:
	$(ALEMBIC) upgrade head

run:
	$(UVICORN) app.main:app --reload

up: up-db migrate run

openapi:
	mkdir -p docs
	curl -s http://127.0.0.1:8000/openapi.json > docs/openapi.json
	python3 -c "import json; json.load(open('docs/openapi.json')); print('openapi saved')"
