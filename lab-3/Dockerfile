FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY .env .env

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
