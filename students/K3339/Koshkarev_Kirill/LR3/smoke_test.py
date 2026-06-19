"""Локальная проверка ЛР3 без Docker (SQLite + Celery eager).

Проверяет:
  1. сервис-парсер POST /parse (реальная загрузка страницы, запись в БД);
  2. основной app: /parser/sync — вызов парсера по HTTP (парсер поднят в фоне);
  3. основной app: /parser/async — постановка задачи в очередь Celery (eager);
  4. /parser/pages — список распарсенных страниц из БД;
  5. базовый функционал ЛР1 (регистрация/логин) всё ещё работает.

Полная схема (PostgreSQL + Redis + воркер) проверяется через docker compose.
"""
import os

os.environ["DATABASE_URL"] = "sqlite:///./smoke_lr3.db"
if os.path.exists("smoke_lr3.db"):
    os.remove("smoke_lr3.db")

import time
import threading

import uvicorn
from fastapi.testclient import TestClient


def check(cond, msg):
    print(f"[{'OK  ' if cond else 'FAIL'}] {msg}")
    assert cond, msg


# --- 1. Сервис-парсер напрямую ---
from parser.main import app as parser_app

parser_client = TestClient(parser_app)
with parser_client:  # триггерит startup -> init_db
    r = parser_client.post("/parse", json={"url": "https://example.com"})
check(r.status_code == 200, "parser /parse вернул 200")
check(r.json()["result"]["title"] == "Example Domain", "parser извлёк заголовок 'Example Domain'")

# --- Поднимаем сервис-парсер на реальном порту для проверки /parser/sync ---
from app.config import settings as _settings
_settings.PARSER_URL = "http://127.0.0.1:8011"  # в Docker задаётся через env PARSER_URL
server = uvicorn.Server(uvicorn.Config(parser_app, host="127.0.0.1", port=8011, log_level="warning"))
t = threading.Thread(target=server.run, daemon=True)
t.start()
for _ in range(50):
    if server.started:
        break
    time.sleep(0.1)
check(server.started, "сервис-парсер запущен на :8011")

# --- 2-5. Основное приложение ---
# Включаем eager-режим Celery, чтобы задача выполнилась без брокера/воркера.
import worker.celery_app as wc
wc.celery.conf.task_always_eager = True
wc.celery.conf.task_eager_propagates = True

from app.main import app

with TestClient(app) as client:
    # ЛР1 жив
    reg = client.post("/auth/register", json={
        "full_name": "Тест", "email": "lr3@itmo.ru", "password": "secret123"})
    check(reg.status_code == 201, "ЛР1: регистрация работает (201)")

    # 2. Синхронный вызов парсера по HTTP
    s = client.post("/parser/sync", params={"url": "https://www.python.org"})
    check(s.status_code == 200, "/parser/sync вернул 200")
    check(s.json()["result"]["source"] == "http", "sync: source='http'")
    check("Python" in s.json()["result"]["title"], "sync: заголовок содержит 'Python'")

    # 3. Асинхронный вызов через очередь Celery (eager)
    a = client.post("/parser/async", params={"url": "https://docs.python.org/3/"})
    check(a.status_code == 200 and "task_id" in a.json(), "/parser/async вернул task_id")

    # 4. Список распарсенных страниц
    pages = client.get("/parser/pages")
    check(pages.status_code == 200, "/parser/pages вернул 200")
    sources = {p["source"] for p in pages.json()}
    check("http" in sources and "celery" in sources,
          f"в БД есть записи и от http, и от celery (sources={sources})")
    print(f"      всего страниц в БД: {len(pages.json())}")

server.should_exit = True
time.sleep(0.3)
print("\nВСЕ ПРОВЕРКИ ЛР3 ПРОЙДЕНЫ УСПЕШНО ✅")

import app.database as _db
_db.engine.dispose()
if os.path.exists("smoke_lr3.db"):
    os.remove("smoke_lr3.db")
