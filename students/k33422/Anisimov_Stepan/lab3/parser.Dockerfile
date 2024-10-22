FROM python:3.11.9

WORKDIR /code

COPY ./parser/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./parser /code/parser

EXPOSE 8000

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "parser.main:parser"]