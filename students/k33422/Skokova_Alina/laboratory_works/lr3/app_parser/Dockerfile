FROM python:3.12.3-alpine3.19

WORKDIR /src

COPY requirements.txt requirements.txt

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./parser /src/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8010"]