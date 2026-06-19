"""Интеграция парсера с основным приложением (подзадачи 2 и 3).

- POST /parser/sync   — синхронный вызов: приложение по HTTP обращается к
                        сервису-парсеру (отдельный контейнер) и ждёт результат.
- POST /parser/async  — асинхронный вызов: задача ставится в очередь Celery/Redis
                        и выполняется фоновым воркером.
- GET  /parser/result/{task_id} — статус/результат фоновой задачи.
- GET  /parser/pages  — список распарсенных страниц из БД.
"""
from typing import List

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import ParsedPage

router = APIRouter(prefix="/parser", tags=["Парсер"])


@router.post("/sync")
def parse_sync(url: str = Query(..., description="URL для парсинга")):
    """Синхронный вызов парсера через HTTP (сервис parser в отдельном контейнере)."""
    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(f"{settings.PARSER_URL}/parse", json={"url": url})
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Сервис-парсер недоступен: {e}")


@router.post("/async")
def parse_async(url: str = Query(..., description="URL для парсинга")):
    """Асинхронный вызов: ставит задачу парсинга в очередь Celery и сразу отвечает."""
    # Импорт здесь, чтобы основное приложение не падало без брокера на старте.
    from worker.celery_app import parse_url_task

    task = parse_url_task.delay(url)
    return {
        "message": "Задача поставлена в очередь",
        "task_id": task.id,
        "status_url": f"/parser/result/{task.id}",
    }


@router.get("/result/{task_id}")
def parse_result(task_id: str):
    """Возвращает статус и результат фоновой задачи по её id."""
    from worker.celery_app import celery

    result = celery.AsyncResult(task_id)
    response = {"task_id": task_id, "status": result.status}
    if result.successful():
        response["result"] = result.result
    elif result.failed():
        response["error"] = str(result.result)
    return response


@router.get("/pages", response_model=List[dict])
def list_pages(db: Session = Depends(get_db)):
    """Список распарсенных страниц (из таблицы parsed_pages)."""
    pages = db.query(ParsedPage).order_by(ParsedPage.id.desc()).all()
    return [
        {
            "id": p.id,
            "url": p.url,
            "title": p.title,
            "source": p.source,
            "parsed_at": p.parsed_at.isoformat() if p.parsed_at else None,
        }
        for p in pages
    ]
