FROM python:3.12.3-alpine3.19
# install requirements
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./parser_threading ./parser_threading
RUN pip install -e ./parser_threading

COPY ./main.py .
COPY ./tasks.py .
# set ENV variable for backend
ENV BACKEND_URL="http://app_main:8100"
# run parser fastapi app
EXPOSE 8200
CMD ["fastapi", "run", "main.py", "--proxy-headers", "--port", "8200"]

