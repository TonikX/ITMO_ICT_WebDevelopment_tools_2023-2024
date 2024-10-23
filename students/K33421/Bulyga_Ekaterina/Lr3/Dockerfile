FROM huecker.io/library/python:3.12-slim

RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /application

COPY requirements.txt .

RUN pip install --no-cache -r requirements.txt
