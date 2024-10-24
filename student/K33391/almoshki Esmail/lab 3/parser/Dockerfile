FROM python:3.12.4

WORKDIR /

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "main:app" , "--host" , "0.0.0.0" , "--port" , "8001" ]





