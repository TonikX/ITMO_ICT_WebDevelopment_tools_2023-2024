FROM python:3.8

WORKDIR /app

COPY ./web_api /app/web_api
COPY ./url_parser /app/url_parser
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt 


