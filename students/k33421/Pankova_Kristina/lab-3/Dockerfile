FROM python:3.12-slim

WORKDIR /task1
COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache -r requirements.txt

COPY /fin_management/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

