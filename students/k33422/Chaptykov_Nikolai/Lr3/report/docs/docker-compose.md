# Docker-compose
Соберем два сервиса под базу данных на PostgreSQL и под проект на FastAPI, обозначим их в рамках единого приложения как db и lab3 соответственно. Инициализируем окружение из которого будет создаваться БД и супер-пользователь, укажем директорию для сохранения данных из контейнера PostgreSQL. Обозначим внешние и внутренние порты: 6969 внешний, а 8000 порт для контейнера с FastAPI, 5432 оставим одинаковыми для хоста и контейнера с PostgreSQL, чтобы осуществлять доступ к БД из DBeaver:
```Python
version: '3'
services:
  db:
    image: postgres:14.1
    environment:
      - POSTGRES_DB=TimeManager
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=123
      - PGDATA=/var/lib/postgresql/data/pgdata
    ports:
      - "5432:5432"

  lab3:
    restart: always
    build: .
    depends_on:
      - db
    command: uvicorn main:app --host 0.0.0.0 --port 8000
    ports:
      - "6969:8000"

```