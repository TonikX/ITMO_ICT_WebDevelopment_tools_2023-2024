"""Точка входа FastAPI-приложения «Система проведения хакатонов» (ЛР1).

Запуск:  uvicorn app.main:app --reload
Документация Swagger:  http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI

from app.routers import auth, hackathons, submissions, tasks, teams, users

# Схема БД создаётся и версионируется через миграции Alembic:
#     alembic upgrade head
# (см. папку alembic/). Поэтому Base.metadata.create_all здесь больше не вызываем.

app = FastAPI(
    title="Hackathon Platform API",
    description=(
        "Серверное приложение для организации и проведения хакатонов. "
        "Лабораторная работа №1 по дисциплине «Web-разработка»."
    ),
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(hackathons.router)
app.include_router(teams.router)
app.include_router(tasks.router)
app.include_router(submissions.router)


@app.get("/", tags=["Служебные"])
def root():
    return {
        "message": "Hackathon Platform API. Документация доступна по адресу /docs",
        "version": "1.0.0",
    }


@app.get("/health", tags=["Служебные"])
def health():
    return {"status": "ok"}
