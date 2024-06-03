FROM python:3.11

WORKDIR /book_crossing_app

COPY requirements.txt /book_crossing_app/

RUN pip install --root-user-action=ignore -r /book_crossing_app/requirements.txt

COPY ./book-crossing-app /book_crossing_app

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]