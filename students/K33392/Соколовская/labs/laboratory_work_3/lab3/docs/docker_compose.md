    version: '3.11'
    
    services:
        api:
          build:
            context: .
            dockerfile: app.Dockerfile
          ports:
            - "8080:8080"
          env_file:
            - book-crossing-app/.env
          depends_on:
            - postgres
    
        parser:
          build:
            context: .
            dockerfile: parser.Dockerfile
          ports:
            - "8081:8081"
          env_file:
            - book-crossing-app/.env
          depends_on:
            - postgres
            - api
    
        postgres:
          image: postgres
          environment:
            POSTGRES_USER: book_crossing
            POSTGRES_PASSWORD: book_crossing
            POSTGRES_DB: book_crossing
          ports:
            - "5432:5432"
    
        redis:
          image: redis
          ports:
            - "6379:6379"
    
        celery:
          build:
            context: .
            dockerfile: parser.Dockerfile
          command: ['python', '-m', 'celery', '-A', 'celery_config.celery_app', 'worker']
          depends_on:
            - postgres
            - api
            - redis
          env_file:
            - book-crossing-app/.env
