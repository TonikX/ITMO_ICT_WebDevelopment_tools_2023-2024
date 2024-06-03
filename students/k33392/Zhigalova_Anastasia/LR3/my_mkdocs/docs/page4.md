#  parser/Dockerfile и parser/Dockerfile.celery

#### Dockerfile
```
FROM python:3.12-slim

WORKDIR /parser

COPY requirements.txt .
RUN mount=type=cache,target=/root/.cache pip3 install -r requirements.txt
COPY . .

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

```

#### Dockerfile.celery
```
FROM python:3.12-slim

WORKDIR /parser

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["celery", "-A", "celery_app", "worker", "--loglevel=info"]

```