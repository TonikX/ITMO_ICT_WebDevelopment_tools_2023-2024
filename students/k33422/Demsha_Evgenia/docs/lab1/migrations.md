# Миграции

Адрес базы данных в файле `alembic.ini`:

`sqlalchemy.url = postgresql+psycopg2://${DB_USER}:${DB_PASS}@${DB_HOST}/${DB_NAME}`

Файл `env.py`, где "собирается" адрес базы данных из секретных переменных окружения:

```Python
def run_migrations_online() -> None:

--8<-- "laboratory_work_1/finance/migrations/env.py:75:106"
```

Одна из записей изменения базы данных:

```Python
def run_migrations_online() -> None:

--8<-- "laboratory_work_1/finance/migrations/versions/e4029c66847d_alter_admin.py"
```