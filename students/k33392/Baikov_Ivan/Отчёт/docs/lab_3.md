
# Лабораторная работа №3

В результате выполнения этой работы был создан асинхронный парсер, который вызывался по определенному запросу через Fast-Api приложение.
После чего с помощью Celery и Redis был настроен вызов данного парсера через очередь.

## Код docker-compose.yml
    version: "3.9"
    
    services:
      db:
        image: postgres:15
        container_name: db_4
        command: -p 1221
        expose:
          - 1221
        env_file:
          - .env
      redis:
        image: redis:7
        container_name: redis_4
        command: --port 5370
        expose:
          - 5370
      app:
        build:
          context: .
        env_file:
          - .env
        container_name: api_4
        depends_on:
          - db
          - redis
        ports:
          - 8080:8080
      celery:
        build:
          context: .
        container_name: celery_4
        env_file:
          - .env
        command: ["/lab3/docker/celery.sh"]
        depends_on:
          - app
          - redis
          - db
      flower:
        build:
          context: .
        container_name: flower_4
        env_file:
          - .env
        command: ["/lab3/docker/flower.sh"]
        depends_on:
          - app
          - celery
          - redis
          - db
        ports:
          - 5555:5555


## Код Dockerfile
    FROM python:3.11
    
    WORKDIR /lab3
    
    COPY requirements.txt .
    
    RUN pip3 install -r requirements.txt
    
    COPY . .
    
    RUN chmod a+x docker/*.sh
    
    CMD gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080

## Код эедпоинта
    prod_names = ('uglovye-kukhni',
                   'kukhni',
                   'elementy-kukhni',
                   'obedennye-gruppy',
                   'khity-prodazh-kukhni',
                   'kukhonnye-ugolki',
                   'mojki',
                   )
    
    @app.get("/parse/{prod_name}")
    async def parse_radio(prod_name: str):
        if prod_name not in prod_names:
            raise HTTPException(status_code=404, detail="Product did not found")
        else:
            product_parse.delay(f'https://yourroom.ru/{prod_name}')
            return {"ok": True}

## Код worker.py

    import asyncio
    
    from sqlalchemy.dialects.postgresql import asyncpg
    
    from config import *
    from celery import Celery
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from product_parser import parse_and_save
    
    broker = f'redis://{REDIS_HOST}:{REDIS_PORT}'
    worker = Celery('tasks', broker=broker)
    
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    db_session = Session()
    
    
    @worker.task(name='Parse')
    def product_parse(url: str):
        asyncio.run(parse_and_save(url,DATABASE_URL))



### Результат
![Результат](images/lab_3/a.jpg)
![Результат](images/lab_3/b.jpg)


