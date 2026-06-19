"""Конфигурация приложения.

Значения берутся из переменных окружения, при их отсутствии используются
значения по умолчанию (удобно для локального запуска и проверки ЛР).
"""
import os


class Settings:
    # Подключение к БД. По умолчанию — локальный файл SQLite.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./hackathon.db")

    # Секрет для подписи JWT. В реальном проекте должен храниться в секрете.
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super-secret-key-for-hackathon-lab-1")

    # Алгоритм подписи (реализован вручную, см. security.py).
    JWT_ALGORITHM: str = "HS256"

    # Время жизни access-токена в минутах.
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


settings = Settings()
