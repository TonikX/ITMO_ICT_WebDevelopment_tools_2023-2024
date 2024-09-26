# Лабораторная 3

## Структура

```plaintext
project/
│
├── lab_1/ (первая лабораторная)
│   └── ...
│
├── lab2/ (парсер из второй лабораторной)
│   └── ...
│
└── docker-compose.yaml
```


## docker 

### docker-compose

```pythonversion: '3.10'
services:

  lab1:
    container_name: lab1
    build:
      context: ./lab_1
    env_file: .env
    depends_on:
      - db
    ports:
      - "8000:8000"
    command: uvicorn main:app --host 0.0.0.0 --port 8000
    networks:
      - backend_3
    restart: always

  lab2:
    container_name: lab2
    build:
      context: ./lab2
    env_file: .env
    restart: always
    ports:
      - "8001:8001"
    command: uvicorn main:app --host 0.0.0.0 --port 8001
    depends_on:
      - redis
      - db
    networks:
      - backend_3

  celery_start:
    build:
      context: ./lab2
    container_name: celery_start
    command: celery -A celery_start worker --loglevel=info
    restart: always
    depends_on:
      - redis
      - lab2
      - db
    networks:
      - backend_3

  redis:
    image: redis
    ports:
      - "6379:6379"
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
      - POSTGRES_DB=labs
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    ports:
      - "5432:5432"
    networks:
      - backend_3


volumes:
  postgres_data:

networks:
  backend_3:
```

### Dockerfile (lab_1)

```python
FROM python:3.9.19-alpine3.20

WORKDIR .

COPY . .
RUN pip3 install -r requirements.txt

CMD uvicorn main:app --host localhost --port 8000
```

### Dockerfile (lab2)
```python
FROM python:3.9.19-alpine3.20

WORKDIR .

COPY . .
RUN pip3 install -r requirements.txt

CMD uvicorn main:app --host localhost --port 8001
```

## Сelery

```python
celery_app = Celery(
    "celery_app",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

celery_app.conf.update(
    task_routes={
        "parse.parse_and_save": "main-queue",
    },
)

```


### Функция таски

```python
@celery_app.task
def parse_and_save(url,  session):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text

    conn = psycopg2.connect(os.getenv('DB_URL'))
    curs = conn.cursor()

    curs.execute("INSERT INTO site (url, title) VALUES (%s, %s)", (url, title))
    conn.commit()

    curs.close()
    conn.close()
```
