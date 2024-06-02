# Структура проекта

В рамках лабораторной работы проект из 1 и 2 лабораторных работ были пренесены внутрь одного poetry проекта и разделены какждый по своим папкам. Получилась следующая структура:

```bash
lab-4/
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── migrations
│   ├── env.py
│   ├── __pycache__
│   ├── README
│   ├── script.py.mako
│   └── versions
├── poetry.lock
├── postgres  [error opening dir]
├── pyproject.toml
├── README.md
└── src
    ├── __init__.py
    ├── __pycache__
    ├── url_parser
    └── web_api
```
