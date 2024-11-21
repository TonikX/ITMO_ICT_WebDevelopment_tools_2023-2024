# Упаковка в Docker

Для FastAPI приложения и папсера были написаны отдельные Docker-файлы. 
Заданы рабочие директории, установка зависимостей и команды входа.

## Docker для FastAPI приложения

    FROM python:3.11
    
    WORKDIR /app
    
    COPY requirements.txt .
    
    RUN pip install --root-user-action=ignore -r /app/requirements.txt
    
    COPY . .
    
    CMD  [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]

## Docker для парсера данных

    FROM python:3.11
    
    WORKDIR /web_parser
    
    COPY requirements.txt .
    
    RUN pip install --root-user-action=ignore -r /web_parser/requirements.txt
    
    COPY . .
    
    CMD [ "uvicorn", "web_parser:app", "--host", "0.0.0.0", "--port", "8081", "--reload"]

# Создание Docker Compose файла

Далее написан Docker Compose файл со всеми сервисами и их связями. 

    version: '3.11'
    
    services:
      app:
        build:
          context: ./app
          dockerfile: Dockerfile
        env_file:
          - app/.env
        ports:
          - "8080:8080"
        depends_on:
          - postgres
    
      web_parser:
        build:
          context: ./web_parser
          dockerfile: Dockerfile
        ports:
          - "8081:8081"
        depends_on:
          - postgres
          - app
    
      postgres:
        image: postgres
        container_name: postgres_db
        environment:
          - POSTGRES_USER=postgres
          - POSTGRES_PASSWORD=password
          - POSTGRES_DB=timetable
        ports:
          - "5432:5432"
    
      redis:
        image: redis:latest
        container_name: redis
        ports:
          - "6379:6379"
    
      celery_worker:
          build: ./web_parser
          command: celery -A web_parser.celery_app worker --loglevel=info
          depends_on:
            - redis
            - app
            - postgres
          environment:
            - REDIS_URL=redis://redis:6379/0

# Вызов парсера из FastAPI

В приложении FastAPI вызывается парсер через заданный путь, далее в методе parse он добавляется в очередь. 

    app = FastAPI()
    
    
    class ParseRequest(BaseModel):
        url: str
    
    
    @app.get("/")
    async def read_root():
        return {"message": "Привет"}
    
    
    @app.post("/parse/")
    async def parse(request: ParseRequest):
        try:
            parse_and_save.delay(request.url)
            return {"message": f"Tasks were successfully saved!"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# Код парсера

Здесь задается конфигурация Celery и определятся задача для парсинга, которая будет выполняться в фоновом режиме.
Также представлен сам код парсера.

    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    import config
    import requests
    
    from connection import DataBaseConnection
    from bs4 import BeautifulSoup
    from datetime import date, timedelta
    from sqlalchemy.orm import sessionmaker
    from celery import Celery
    
    celery_app = Celery(
        "web_parser",
        broker=f"redis://redis:6379/0",
        backend="redis://redis:6379/0",
    )
    
    app = FastAPI()
    
    
    class ParseRequest(BaseModel):
        url: str
    
    
    @app.get("/")
    async def read_root():
        return {"message": "Привет"}
    
    
    @app.post("/parse/")
    async def parse(request: ParseRequest):
        try:
            parse_and_save.delay(request.url)
            return {"message": f"Tasks were successfully saved!"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    
    @celery_app.task
    def parse_and_save(url):
        try:
            engine = DataBaseConnection.connect_to_database()
            session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            tasks = soup.find_all(config.HTML_TAG, class_=config.HTML_CLASS)
            task = tasks[0].text.strip().replace('\xa0', ' ')
    
            with session_local() as session:
                task_data = {
                    'title': task,
                    'description': '',
                    'deadline': str(date.today() + timedelta(7)),
                    'created_date': str(date.today()),
                    'priority': 'high',
                    'status': 'to_do',
                    'category_id': 1,
                    'user_id': 1
                }
                session.execute(DataBaseConnection.INSERT_SQL, task_data)
                session.commit()
        except Exception as e:
            print(f"Error in parse_and_save: {e}")

