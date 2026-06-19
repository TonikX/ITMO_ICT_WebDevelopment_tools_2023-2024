"""Настройка подключения к базе данных через SQLAlchemy.

Два движка к одной и той же БД:
  - синхронный (engine / SessionLocal) — для CRUD-эндпоинтов ЛР1 и создания таблиц;
  - асинхронный (async_engine / AsyncSessionLocal) — для неблокирующей записи
    результатов парсинга (ЛР3): commit выполняется через await.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

from app.config import settings

# Для SQLite требуется отключить проверку потока, т.к. FastAPI работает
# с несколькими потоками.
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Асинхронный движок (драйвер asyncpg для PostgreSQL или aiosqlite для SQLite).
# NullPool: соединение не кэшируется между задачами — Celery-воркер запускает
# asyncio.run на каждую задачу (новый событийный цикл), а пул мог бы выдать
# соединение, привязанное к уже закрытому циклу.
async_connect_args = {"check_same_thread": False} if settings.ASYNC_DATABASE_URL.startswith("sqlite") else {}
async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL, connect_args=async_connect_args, poolclass=NullPool
)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False)

Base = declarative_base()


def get_db():
    """FastAPI-зависимость: выдаёт сессию БД и гарантированно закрывает её."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
