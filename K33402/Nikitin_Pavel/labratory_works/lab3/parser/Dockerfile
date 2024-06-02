FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 9000 & celery -A tasks worker --loglevel=info"]
