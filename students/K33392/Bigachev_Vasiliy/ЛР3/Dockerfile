FROM python:3.12

WORKDIR /code

COPY ./req.txt /code/req.txt

RUN pip install --no-cache-dir --upgrade -r /code/req.txt

COPY . /code

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3001"]