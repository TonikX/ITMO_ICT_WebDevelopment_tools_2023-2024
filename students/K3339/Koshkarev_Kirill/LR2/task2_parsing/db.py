"""Слой доступа к БД для задачи 2.

По условию данные парсинга сохраняются в базу данных из ЛР1. Мы подключаемся
к тому же файлу SQLite (LR1/hackathon.db) и добавляем в него таблицу
`parsed_pages`, куда складываем результаты парсинга (URL и заголовок страницы).
Доменные таблицы ЛР1 при этом не затрагиваются.

Каждый поток/процесс создаёт собственную сессию, поэтому модуль безопасно
переиспользуется и в threading, и в multiprocessing (при spawn дочерний
процесс заново импортирует модуль и получает свой engine).
"""
import os
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

# Путь к базе данных из ЛР1 (тот же файл SQLite).
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_LR1_DB = os.path.abspath(os.path.join(_THIS_DIR, "..", "..", "LR1", "hackathon.db"))
DATABASE_URL = os.getenv("LR2_DATABASE_URL", f"sqlite:///{_LR1_DB}")
# Асинхронная версия той же строки подключения (драйвер aiosqlite).
ASYNC_DATABASE_URL = DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://", 1)

# --- Синхронный движок (для threading / multiprocessing) ---
# timeout — чтобы при одновременной записи из нескольких процессов SQLite ждал
# освобождения блокировки, а не падал с "database is locked".
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False, "timeout": 30})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# --- Асинхронный движок (для подхода async) ---
# Запись в БД выполняется неблокирующе (await), не занимая событийный цикл.
async_engine = create_async_engine(
    ASYNC_DATABASE_URL, connect_args={"timeout": 30}, poolclass=NullPool
)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False)

Base = declarative_base()


class ParsedPage(Base):
    """Результат парсинга одной веб-страницы."""
    __tablename__ = "parsed_pages"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False)
    title = Column(Text, nullable=True)
    approach = Column(String(30), nullable=True)  # каким подходом получено
    parsed_at = Column(DateTime, default=datetime.utcnow, nullable=False)


def init_db():
    """Создаёт таблицу parsed_pages, если её ещё нет."""
    Base.metadata.create_all(bind=engine)


def save_page(url: str, title: str, approach: str) -> int:
    """Сохраняет одну запись о распарсенной странице. Возвращает id записи."""
    session = SessionLocal()
    try:
        page = ParsedPage(url=url, title=title, approach=approach)
        session.add(page)
        session.commit()
        session.refresh(page)
        return page.id
    finally:
        session.close()


async def async_save_page(url: str, title: str, approach: str) -> int:
    """Асинхронно сохраняет запись о странице (await, без блокировки цикла)."""
    async with AsyncSessionLocal() as session:
        page = ParsedPage(url=url, title=title, approach=approach)
        session.add(page)
        await session.commit()
        await session.refresh(page)
        return page.id


def count_pages() -> int:
    session = SessionLocal()
    try:
        return session.query(ParsedPage).count()
    finally:
        session.close()
