# Docker
    Чтобы развернуть приложение FastAPI в контейнере Docker, интегрировать анализатор данных с базой данных и вызвать анализатор через API и очередь, вам необходимо выполнить следующие действия:

    Шаг 1: Создание приложения FastAPI Создайте новое приложение FastAPI с main.pyфайлом и requirements.txtфайлом. main.pyФайл должен содержать код приложения FastAPI, а requirements.txtфайл должен содержать список зависимостей, требуемых приложением.

    Шаг 2: Создайте Dockerfile Создайте новый файл с тем же именем Dockerfileв том же каталоге, что и main.pyфайл. Он Dockerfileдолжен содержать инструкции по созданию образа Docker.

    Вот пример Dockerfile:
=== "Dockerfile"

    ``` py
    FROM python:3.10-alpine3.19

    WORKDIR /lab_1

    COPY . .
    RUN pip3 install --upgrade -r requirements.txt

    CMD uvicorn src.main:app --host localhost --port 8000

    ```
    Описание работы - в Dockerfile пишем образ который будет использоваться в нашем приложении

=== "requirement.txt"

    ``` py
    celery
    redis
    fastapi
    uvicorn
    python-dotenv
    psycopg2-binary
    jwt
    bcrypt
    requests
    bs4
    aiohttp
    asyncio
    sqlmodel

    ```
    Описание работы -  Создаем requirement.txt где перечисляем все используемые нами библеотеки, чтобы далее их 
    автоматически загружать



=== "docker-compose.yml"

    ``` py
    version: '3.10'
services:
  lab_1:
    container_name: lab_1
    build:
      context: ./lab_1
    env_file: .env
    depends_on:
      - db
    ports:
      - '8000:8000'
    command: uvicorn src.main:app --host 0.0.0.0 --port 8000
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
    command: uvicorn src.main:app --host 0.0.0.0 --port 8001
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
    инициализируем приложение


ВЫВОД


Таким образом мы научились упаковывать FastAPI приложение в Docker, интегрировали парсерр данных с базой данных