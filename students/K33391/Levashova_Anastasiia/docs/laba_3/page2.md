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
          - POSTGRES_PASSWORD=12345
          - POSTGRES_DB=tasks_db
        ports:
          - "5434:5432"
    
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
