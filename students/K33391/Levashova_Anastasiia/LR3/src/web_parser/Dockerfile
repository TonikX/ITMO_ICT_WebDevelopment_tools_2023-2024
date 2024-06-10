FROM python:3.11

WORKDIR /web_parser

COPY requirements.txt .

RUN pip install --root-user-action=ignore -r /web_parser/requirements.txt

COPY . .

CMD [ "uvicorn", "web_parser:app", "--host", "0.0.0.0", "--port", "8081"]
