# Лаба №3

Инициализация миграций через `alembic`:

```bash
alembic init migrations
```

Создать начальные миграции:

```bash
alembic revision --autogenerate -m 'initial'
```

Накатить все миграции до актуальной версии:

```bash
alembic upgrade head
```
