"""Отдельный микросервис-парсер (подзадача 1, пункт 4).

Запускается в собственном контейнере и предоставляет HTTP-эндпоинт POST /parse,
который загружает страницу по URL, извлекает заголовок и сохраняет его в БД.
Основное приложение вызывает этот сервис по HTTP.

Запуск: uvicorn parser.main:app --host 0.0.0.0 --port 8001
"""
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.init_db import init_db
from app.parsing import parse_and_save_async

app = FastAPI(title="Parser Service", version="1.0.0")


class ParseRequest(BaseModel):
    url: str


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health", tags=["Служебные"])
def health():
    return {"status": "ok", "service": "parser"}


@app.post("/parse", tags=["Парсер"])
async def parse(req: ParseRequest):
    """Парсит страницу по URL и асинхронно сохраняет заголовок в БД."""
    try:
        result = await parse_and_save_async(req.url, source="http")
        return {"message": "Parsing completed", "result": result}
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Ошибка загрузки страницы: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
