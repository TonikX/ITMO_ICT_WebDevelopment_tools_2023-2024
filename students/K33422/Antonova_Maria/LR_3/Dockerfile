FROM python:3.10-slim-buster as builder

RUN apt-get update

RUN pip install poetry
COPY poetry.lock pyproject.toml /
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-dev \
    && poetry add bcrypt \
    && rm -rf pyproject.toml poetry.lock

WORKDIR /qr_test
COPY . /qr_test

CMD uvicorn src.main:app --host 0.0.0.0 --port 8001