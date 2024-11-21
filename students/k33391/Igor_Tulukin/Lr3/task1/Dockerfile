# образ с Python
FROM python:3.12-slim

# рабочая директорию
WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Скопировать все исходные файлы в контейнер
COPY .. .

# Укажите команду для запуска FastAPI приложения с uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
