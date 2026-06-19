"""Конфигурация приложения (значения берутся из переменных окружения).

В docker-compose переменные задаются для каждого сервиса; при локальном запуске
используются значения по умолчанию (SQLite + локальные адреса).
"""
import os


def _to_async_url(url: str) -> str:
    """Преобразует обычную строку подключения в асинхронную (для async-движка)."""
    if url.startswith("postgresql+psycopg2"):
        return url.replace("postgresql+psycopg2", "postgresql+asyncpg", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if url.startswith("sqlite://"):
        return url.replace("sqlite://", "sqlite+aiosqlite://", 1)
    return url


class Settings:
    # Подключение к БД. В Docker — PostgreSQL, локально по умолчанию — SQLite.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./hackathon.db")
    # Та же БД, но через асинхронный драйвер (asyncpg / aiosqlite) — для async-записи.
    ASYNC_DATABASE_URL: str = os.getenv("ASYNC_DATABASE_URL", _to_async_url(DATABASE_URL))

    # Секрет и параметры JWT (см. security.py).
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super-secret-key-for-hackathon-lab-1")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # Адрес отдельного сервиса-парсера (вызывается основным приложением по HTTP).
    PARSER_URL: str = os.getenv("PARSER_URL", "http://localhost:8001")

    # Celery + Redis (очередь фоновых задач).
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")


settings = Settings()
