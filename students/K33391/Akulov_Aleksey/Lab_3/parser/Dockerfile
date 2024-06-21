FROM python:3.11

WORKDIR /parser

COPY requirements.txt .

RUN pip install --root-user-action=ignore -r /parser/requirements.txt

COPY . .

CMD [ "uvicorn", "parser:app", "--host", "0.0.0.0", "--port", "8081"]