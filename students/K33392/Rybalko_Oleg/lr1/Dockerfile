FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN mount=type=cache,target=/root/.cache pip3 install -r requirements.txt
COPY . .

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
