FROM python:3.12-slim

# COPY wait-for-it.sh /wait-for-it.sh
# RUN chmod +x /wait-for-it.sh

WORKDIR /TeamTinder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
 
COPY requirements.txt /TeamTinder/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /TeamTinder/requirements.txt

COPY ./TeamTinder /TeamTinder

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "81", "--reload"]