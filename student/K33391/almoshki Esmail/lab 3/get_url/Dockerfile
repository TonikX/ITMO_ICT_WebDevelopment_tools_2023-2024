FROM python:3.12.4

WORKDIR /get_url

COPY  ./requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt 

COPY . .

EXPOSE 8002

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002" ]