"""Точка входа основного FastAPI-приложения «Система проведения хакатонов».

ЛР1 — базовый функционал, ЛР3 — интеграция парсера (роутер parser).

Запуск:  uvicorn app.main:app --host 0.0.0.0 --port 8000
Документация Swagger:  http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI

from app.init_db import init_db
from app.routers import auth, hackathons, parser, submissions, tasks, teams, users

app = FastAPI(
    title="Hackathon Platform API",
    description=(
        "Серверное приложение для организации и проведения хакатонов. "
        "ЛР1 (API + БД) + ЛР3 (Docker, вызов парсера по HTTP и через очередь Celery)."
    ),
    version="3.0.0",
)


@app.on_event("startup")
def on_startup():
    # Создаём таблицы при старте (ждём готовности БД — актуально для PostgreSQL в Docker).
    init_db()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(hackathons.router)
app.include_router(teams.router)
app.include_router(tasks.router)
app.include_router(submissions.router)
app.include_router(parser.router)


@app.get("/", tags=["Служебные"])
def root():
    return {
        "message": "Hackathon Platform API. Документация доступна по адресу /docs",
        "version": "3.0.0",
    }


@app.get("/health", tags=["Служебные"])
def health():
    return {"status": "ok"}
