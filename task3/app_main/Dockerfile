FROM python:3.12.3-alpine3.19
# requirements
COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# copy app
WORKDIR /app
COPY /app .
EXPOSE 8100
CMD ["fastapi", "run", "/app/endpoints/endpoints.py", "--proxy-headers", "--port", "8100"]

