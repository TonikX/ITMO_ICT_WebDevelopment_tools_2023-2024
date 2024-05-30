# Dockerfile

# Этап сборки зависимостей
FROM python:3.10 AS builder

WORKDIR /BookCrossing

# Копируем requirements.txt
COPY requirements.txt .

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Установка необходимых для компиляции библиотек
RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get install -y libpq-dev

# Установка uvicorn
RUN pip install uvicorn

# Установка драйверов для работы с БД
RUN pip install asyncpg

# Основной этап
FROM python:3.10 AS final

WORKDIR /BookCrossing

# Копируем все файлы из директории с приложением
COPY . .

# Копируем зависимости из этапа builder
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# Копируем зависимости из этапа builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Определяем команду для запуска приложения
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
