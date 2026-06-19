"""Инициализация БД: создание таблиц с ожиданием готовности базы.

В Docker база PostgreSQL может быть ещё не готова к моменту старта сервиса,
поэтому create_all выполняется с несколькими повторными попытками.
"""
import time

from sqlalchemy.exc import OperationalError

from app.database import Base, engine
# Импорт моделей обязателен, чтобы они зарегистрировались в Base.metadata.
from app import models  # noqa: F401


def init_db(retries: int = 10, delay: float = 2.0) -> None:
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except OperationalError as e:
            last_error = e
            print(f"[init_db] БД ещё не готова (попытка {attempt}/{retries}), ждём {delay}c...")
            time.sleep(delay)
    raise RuntimeError(f"Не удалось подключиться к БД: {last_error}")
