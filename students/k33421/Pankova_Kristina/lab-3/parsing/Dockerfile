FROM python:3.12-slim

WORKDIR /app_parse

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install celery
ENV PATH="/usr/local/bin:${PATH}"


COPY ./main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
