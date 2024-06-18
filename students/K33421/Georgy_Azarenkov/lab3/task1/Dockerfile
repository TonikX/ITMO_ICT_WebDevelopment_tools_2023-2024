FROM python:3.11

WORKDIR /app

COPY ../../lab1/requirements.txt .

RUN pip install --root-user-action=ignore -r requirements.txt

COPY ../../lab1 .

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
