FROM python:3.12-slim

WORKDIR /app
COPY /web-programming/lab_3_S2/task_1/requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache -r requirements.txt

COPY /HackathonsManagementSystem/ .