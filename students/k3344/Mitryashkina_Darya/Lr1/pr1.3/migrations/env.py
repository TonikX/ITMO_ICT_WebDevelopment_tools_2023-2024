from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from models import *  # импортируй свои модели (SQLModel.metadata)
from sqlmodel import SQLModel  # если используешь SQLModel
from dotenv import load_dotenv
import os

load_dotenv()

# Конфигурация Alembic
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

database_url = os.getenv("SYNC_DB_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)
else:
    raise ValueError("SYNC_DB_URL не найден в переменных окружения!")

# Для автогенерации миграций используем metadata из SQLModel (или своего Base)
target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    """Запуск миграций в offline-режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Запуск миграций в online-режиме."""
    url = config.get_main_option("sqlalchemy.url")
    # Создаем синхронный движок. Обратите внимание на использование pool.NullPool.
    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
