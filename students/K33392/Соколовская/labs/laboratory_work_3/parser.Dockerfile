FROM python:3.11

WORKDIR /parser

COPY requirements.txt /parser/

RUN pip install --root-user-action=ignore -r /parser/requirements.txt

COPY ./parser /parser

EXPOSE 8081

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081", "--reload"]
