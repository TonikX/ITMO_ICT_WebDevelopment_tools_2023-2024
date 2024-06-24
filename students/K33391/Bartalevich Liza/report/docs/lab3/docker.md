# Докер

Финально упакуем все приложени в Docker и будем использовать для звауска docker compose.

```Dockerfile
FROM python:3.10-alpine3.19

WORKDIR /lab_2

COPY . .
RUN pip3 install -r requirements.txt

CMD uvicorn main:app --host localhost --port 8001
```

```yaml
version: '3.10'
services:
  taskmanager:
    container_name: lab_1
    build:
      context: ./lab_1
    env_file: .env
    depends_on:
      - db
    ports:
      - '8000:8000'
    command: uvicorn main:app --host 0.0.0.0 --port 8000
    networks:
      - backend_3
    restart: always

  lab_2:
    container_name: lab_2
    build:
      context: ./lab_2
    env_file: .env
    restart: always
    ports:
      - '8001:8001'
    command: uvicorn main:app --host 0.0.0.0 --port 8001
    depends_on:
      - redis
      - db
    networks:
      - backend_3

  celery_start:
    build:
      context: ./lab_2
    container_name: celery_start
    command: celery -A celery_start worker --loglevel=info
    restart: always
    depends_on:
      - redis
      - lab_2
      - db
    networks:
      - backend_3

  redis:
    image: redis
    ports:
      - '6379:6379'
    networks:
      - backend_3
    depends_on:
      - db

  db:
    image: postgres
    restart: always
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_DB=web_data
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    ports:
      - '5432:5432'
    networks:
      - backend_3

volumes:
  postgres_data:

networks:
  backend_3:
    driver: bridge
```
