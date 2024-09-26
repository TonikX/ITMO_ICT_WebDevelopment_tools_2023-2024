!!! example "Задание"
    Научиться упаковывать FastAPI приложение в Docker, интегрировать парсер данных с 
    базой данных и вызывать парсер через API и очередь.

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
    
=== "Dockerfile"

    ``` py
    FROM python:3.9-slim

    WORKDIR /second_task    
    
    COPY requirements.txt .
    
    RUN pip install -r requirements.txt
    
    COPY . .
    
    EXPOSE 8000
    
    CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "8000"]

    ```
    Описание работы - в Dockerfile пишем образ который будет использоваться в нашем приложении

=== "docker-compose.yml"

    ``` py
    services:
      db:
        image: postgres
        container_name: db
        restart: always
        environment:
          - POSTGRES_PASSWORD=1216
          - POSTGRES_USER=postgres
          - POSTGRES_DB=db_lab3
          - POSTGRES_PORT=5432
        volumes:
          - db-data:/var/lib/postgresql/data
        ports:
          - "5432:5432"
        networks:
          - my_network
    
      app:
        container_name: app
        build:
          context: .
        env_file: .env
        depends_on:
          - db
          - redis
        ports:
          - "8000:8000"
        command: uvicorn main:app --host 0.0.0.0 --port 8000
        restart: always
        networks:
          - my_network
    
      celery_task:
        container_name: celery_task
        build:
          context: ./second_task
        env_file: .env
        depends_on:
          - db
          - redis
        ports:
          - "8001:8001"
        command: uvicorn main:app --host 0.0.0.0 --port 8001
        restart: always
        networks:
          - my_network
        dns:
          - 8.8.8.8
          - 8.8.4.4
    
      celery:
        build:
          context: ./second_task
        container_name: celery
        command: celery -A parse worker --loglevel=info
        restart: always
        depends_on:
          - redis
          - db
        environment:
          - CELERY_BROKER_URL=redis://redis:6379/0
          - CELERY_RESULT_BACKEND=redis://redis:6379/0
        networks:
          - my_network
    
      redis:
        image: redis
        ports:
          - "6379:6379"
        networks:
          - my_network
    
    volumes:
      db-data:
    networks:
      my_network:

    ```
    docker-compose описывает контейнер который будет создаваться на основе ранее созданного нами отзыва, также контейнер для бд
    контейнер celery для выполнения фоновых задач

=== "celery_app"

    ``` py
    from celery import Celery
    
    celery_app = Celery("tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0")
    
    
    celery_app.autodiscover_tasks(['parse'])

    ```
    инициализируем приложение, celery_app.autodiscover_tasks указывает автоматически искать и загружать задачи в переданном списке


ВЫВОД

![](http://ung1n.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/img/lab1_and_practics/lab_3_pars.png) 
    парсим домен

![](http://ung1n.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/img/lab1_and_practics/lab_2_get.png) 
    смотрим что домен запарсился

Таким образом мы научились упаковывать FastAPI приложение в Docker, интегрировали парсерр данных с базой данных