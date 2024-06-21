FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./parser/parser .

ENTRYPOINT ["celery", "-A", "celery_config", "worker", "--loglevel=DEBUG"]
