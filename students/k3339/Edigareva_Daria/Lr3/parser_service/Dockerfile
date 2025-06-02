FROM python:3.12-slim AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential libxml2-dev libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1 \
    REDIS_URL=redis://redis:6379/0 \
    TASK_QUEUE=parser:tasks \
    RESULT_PREFIX=parser:results:

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]