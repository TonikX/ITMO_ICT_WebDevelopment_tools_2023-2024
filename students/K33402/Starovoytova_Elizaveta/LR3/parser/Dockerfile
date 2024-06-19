# Используем базовый образ с Python 3.10
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /parser

# Копируем файл requirements.txt в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip3 install -r requirements.txt

# Копируем исходный код приложения в контейнер
COPY . .

# Команда для запуска приложения
ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]