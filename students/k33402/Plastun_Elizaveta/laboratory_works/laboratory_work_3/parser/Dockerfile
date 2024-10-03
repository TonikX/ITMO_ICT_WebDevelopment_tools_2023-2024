FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8002

CMD ["sh", "-c", "uvicorn parser-async:app --host 0.0.0.0 --port 8002"]