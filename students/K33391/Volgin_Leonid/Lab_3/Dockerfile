FROM python:3.11

WORKDIR /lab3

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

CMD gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080
