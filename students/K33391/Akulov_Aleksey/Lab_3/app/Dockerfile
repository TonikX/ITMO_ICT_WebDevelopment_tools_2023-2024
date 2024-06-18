FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --root-user-action=ignore -r /app/requirements.txt

COPY . .

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]