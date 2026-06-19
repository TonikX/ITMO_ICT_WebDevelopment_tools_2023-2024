# Единый образ для всех Python-сервисов (api, parser, worker, beat).
# Сервисы различаются только командой запуска (см. docker-compose.yml).
FROM python:3.11-slim

# Не создавать .pyc и не буферизовать вывод (логи видны сразу).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

# Сначала зависимости — слой кэшируется, если requirements.txt не менялся.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Затем исходный код приложения, парсера и воркера.
COPY app ./app
COPY parser ./parser
COPY worker ./worker

# Порт основного приложения (для сервиса parser переопределяется в compose).
EXPOSE 8000

# Команда по умолчанию — основное приложение (переопределяется для других сервисов).
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
