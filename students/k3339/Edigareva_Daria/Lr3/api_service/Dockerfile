FROM python:3.12-slim AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1 \
    DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/app_db \
    REDIS_URL=redis://redis:6379/0 \
    TASK_QUEUE=parser:tasks \
    RESULT_PREFIX=parser:results:
