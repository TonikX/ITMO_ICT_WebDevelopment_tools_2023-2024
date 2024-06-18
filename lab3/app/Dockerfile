FROM python:3.9.19-alpine3.20

WORKDIR ./app

COPY . .
RUN pip3 install -r requirements.txt

CMD uvicorn main:app --host localhost --port 8000