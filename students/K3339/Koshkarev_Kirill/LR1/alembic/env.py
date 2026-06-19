"""Окружение Alembic для проекта «Система проведения хакатонов».

Здесь Alembic подключается к нашим моделям и берёт строку подключения к БД из
настроек приложения (app.config), а не из статического значения в alembic.ini.
Это позволяет одной командой `alembic upgrade head` накатывать схему как на
SQLite (локально), так и на любую другую БД (через переменную DATABASE_URL).
"""
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# Добавляем корень проекта в путь, чтобы импортировался пакет app.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings  # noqa: E402
from app.database import Base  # noqa: E402
from app import models  # noqa: E402,F401  (импорт регистрирует все таблицы в Base.metadata)

config = context.config

# Подставляем реальную строку подключения из настроек приложения.
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные всех моделей — источник истины для autogenerate.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Миграции в offline-режиме (генерация SQL без подключения к БД)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=url.startswith("sqlite"),  # batch-режим нужен SQLite для ALTER
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Миграции в online-режиме (с подключением к БД)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=connection.dialect.name == "sqlite",
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
