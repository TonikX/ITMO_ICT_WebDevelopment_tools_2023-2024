# Установите базовый образ с Python
FROM python:3.12-slim

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файл зависимостей (если есть)
COPY requirements.txt ./

# Установите необходимые зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте все исходные файлы в контейнер
COPY .. .

# Укажите команду для запуска FastAPI приложения с uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
