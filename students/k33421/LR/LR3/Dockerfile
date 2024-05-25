FROM python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt requirements.txt

RUN python -m venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-multipart

RUN apt update && \
    apt install --no-install-recommends -y libpq-dev && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./my_app .