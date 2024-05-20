from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from pathlib import Path
import os

# Импортируем модели из приложения
from app.backend.models import *

# Путь к папке с миграциями
migration_dir = Path(__file__).parent.parent / "app" / "alembic"

# Загружаем переменные окружения
from dotenv import load_dotenv

load_dotenv()

# Переменные окружения для подключения к бд
DATABASE_URL = os.getenv("DB_ADMIN")

# Конфигурация Alembic
config = context.config

# Загружаем конфигурацию из alembic.ini
config.set_main_option("sqlalchemy.url", DATABASE_URL)
config.set_main_option("script_location", str(migration_dir))

# Подключаемся к базе данных с помощью Alembic
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, render_as_batch=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

# Включаем логирование
fileConfig(config.config_file_name)
