FROM python:3.11-slim

WORKDIR /parser

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.parser_app:app", "--host", "0.0.0.0", "--port", "8001"]
