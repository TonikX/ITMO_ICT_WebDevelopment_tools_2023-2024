FROM python:3.11

WORKDIR /app_books

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "entrypoint.sh"]