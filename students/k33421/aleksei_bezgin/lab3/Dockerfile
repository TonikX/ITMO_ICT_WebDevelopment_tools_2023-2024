FROM python:3.11.6-slim-bookworm as base

WORKDIR /app
COPY requirements.txt /app/

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

FROM base as installer

RUN apt update && apt install --no-install-recommends -y build-essential libpq-dev
RUN pip install uv
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV VIRTUAL_ENV=/opt/venv
RUN uv pip install --no-cache -r requirements.txt

FROM base as runtime

RUN apt update && \
    apt install --no-install-recommends -y libpq-dev && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=installer /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./src/ .
