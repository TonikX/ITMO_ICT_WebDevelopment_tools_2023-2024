FROM golang:1.22-alpine3.19 AS builder
WORKDIR /app
COPY . .
RUN go build -o main cmd/worker/main.go

EXPOSE 8080
CMD ["/app/main"]