FROM python:3.10-alpine
WORKDIR /fast_api_lab
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
