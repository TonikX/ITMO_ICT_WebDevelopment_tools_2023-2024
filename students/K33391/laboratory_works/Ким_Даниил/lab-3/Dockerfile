FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Добавьте .env файл в контейнер
COPY .env .env

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
