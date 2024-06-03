## Подзадача 1: Упаковка FastAPI приложения, базы данных и парсера данных в Docker 
Структура проектов 
У меня есть следующая структура каталогов: 
 
    my_project/
    ├── fastapi-app/
    │   ├── app/ 
    │   │   ├── main.py 
    │   │   └── requirements.txt 
    │   └── Dockerfile 
    ├── parser-app/ 
    │   ├── parser.py 
    │   ├── requirements.txt 
    │   └── Dockerfile
    └── docker-compose.yml 

1. Создание FastAPI приложения: Было реализовано в рамках лабораторной работы номер 1

2. Создание базы данных: Было реализовано в рамках лабораторной работы номер 1

3. Создание парсера данных: Было реализовано в рамках лабораторной работы номер 2

4. В данной лабораторной работе была реализована возможность вызова парсера по http(плюс добавлен endpoint):

    
        @app.post("/parse")
        def run_parser(url: str):
            try:
                response = requests.post("http://parser:8004/parse", json={"url": url})
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                raise HTTPException(status_code=500, detail=str(e))

Далее были созданы Dockerfile: со следующим содержимым для двух приложений: 
1. fastapi-app/Dockerfile

   
    FROM python:3.10
    
    WORKDIR app/fastapi-app
    
    COPY requirements.txt .
    
    RUN pip install --no-cache-dir -r requirements.txt
    
    COPY . .
    
    # Устанавливаем команду ENTRYPOINT для запуска Uvicorn
    ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

2. parser-app/Dockerfile:

    
    FROM python:3.10
    
    WORKDIR app/parser-app
    
    COPY requirements.txt .
    
    RUN pip install --no-cache-dir -r requirements.txt
    
    COPY . .
    
    ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004"]

3. docker-compose.yml:

     
    version: '3.8'  
     services:
          fastapi-app:
            build: ./fastapi-app
            ports:
              - "8000:8000"
            depends_on:
              - parser-app
            environment:
              - DATABASE_URL=postgresql+psycopg2://postgres:1234@localhost:5432/db
        
      parser-app:
        build: ./parser-app
        ports:
          - "8004:8004"
        environment:
          - DATABASE_URL=postgresql+psycopg2://postgres:1234@localhost:5432/db
    
![img.png](img.png)

### Запуск контейнеров
Перешла в корневую директорию  и запустите контейнеры с помощью Docker Compose:

    docker-compose up --build

Проверка работы:

![img_1.png](img_1.png)

## Подзадача 3

![img_2.png](img_2.png)

![img_5.png](img_5.png)

Давайте рассмотрим полный набор файлов и их содержимое для директории celery_worker/.

Структура celery_worker

    celery_worker/
    │   ├── __init__.py
    │   ├── celery_app.py
    │   ├── tasks.py
    │   └── Dockerfile

celery_worker/__init__.py

    # пустой файл

celery_worker/celery_app.py
Этот файл содержит конфигурацию для Celery.


    from celery import Celery
    
    celery_app = Celery(
        "worker",
        broker="redis://redis:6379/0",
        backend="redis://redis:6379/0"
    )
    
    celery_app.conf.update(
        task_routes={
            'celery_worker.tasks.parse_task': 'main-queue',
        },
    )


celery_worker/tasks.py
Этот файл содержит задачи, которые будут выполняться Celery.


        from celery_app import celery_app
        from parser_app.parsers import parse_data
        
        @celery_app.task
        def parse_task(url: str, method: str):
            return parse_data(url, method)

celery_worker/Dockerfile

Этот файл содержит инструкции для создания Docker-образа для Celery worker.

Dockerfile:

        FROM python:3.10
        
        WORKDIR /app
        
        COPY requirements.txt .
        
        RUN pip install --no-cache-dir -r requirements.txt
        
        COPY . .
        
        CMD ["celery", "-A", "celery_worker.celery_app", "worker", "--loglevel=info"]

### Дополнительные шаги:
requirements.txt для Celery Worker
Файл requirements.txt должен быть в корне директории celery_worker.


Убедимся, что docker-compose.yml настроен правильно для использования всех сервисов:
    
    version: '3.8'
    
    services:
      db:
        image: postgres:13
        environment:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: 1234
          POSTGRES_DB: db
        ports:
          - "5432:5432"
        volumes:
          - postgres_data:/var/lib/postgresql/data
    
      redis:
        image: redis:6-alpine
        ports:
          - "6379:6379"
    
      parser_app:
        build: ./parser_app
        ports:
          - "8004:8004"
        environment:
          - DATABASE_URL=postgresql+psycopg2://postgres:1234@db:5432/db
        depends_on:
          - db
    
      fastapi_app:
        build: ./fastapi_app
        ports:
          - "8000:8000"
        depends_on:
          - parser_app
          - db
        environment:
          - DATABASE_URL=postgresql+psycopg2://postgres:1234@db:5432/db
        volumes:
          - fastapi_app_data:/app
    
      celery_worker:
        build: ./fastapi_app
        command: celery -A app.celery_worker worker --loglevel=info
        depends_on:
          - redis
          - fastapi_app
        volumes:
          - celery_worker_data:/app
    
    volumes:
      postgres_data:
      fastapi_app_data:
      celery_worker_data:
    

Убедимся, что зависимости включены:

    fastapi
    pydantic
    uvicorn
    requests
    sqlalchemy
    psycopg2
    celery
    redis
    beautifulsoup4
    aiohttp

### Запуск проекта
Запустим проект с помощью Docker Compose:

    docker-compose up --build
![img_4.png](img_4.png)


![img_6.png](img_6.png)