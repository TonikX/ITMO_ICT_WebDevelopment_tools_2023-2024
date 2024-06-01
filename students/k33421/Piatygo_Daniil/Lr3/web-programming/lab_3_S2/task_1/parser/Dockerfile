FROM python:3.12-slim

WORKDIR /parser
COPY /web-programming/lab_3_S2/task_1/requirements.txt .
COPY /web-programming/lab_3_S2/task_1/parser/creds.json .
COPY /web-programming/lab_3_S2/task_1/parser/parser_naive.py .
COPY /web-programming/lab_3_S2/task_1/parser/parser_threading.py .

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache -r requirements.txt

COPY /web-programming/lab_3_S2/task_1/parser/call_parser.py .