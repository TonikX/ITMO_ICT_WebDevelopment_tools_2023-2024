# FastAPI Application with Docker, PostgreSQL, and Data Parsing

Welcome to the documentation for the FastAPI application. This project integrates a FastAPI web service, a data parser, and a PostgreSQL database, all containerized using Docker. The goal of this project is to demonstrate how to package a web application, integrate data parsing functionality, and connect it to a database, while also allowing the application to be scalable and portable across different environments.

## Project Overview

This project is divided into three main services:

1. **Bookcrossing Service**:
   - A FastAPI application that serves as the main web API for the project.
   - It interacts with a PostgreSQL database and handles requests for book-related data.
   - Built as part of the earlier laboratory exercises, it is now containerized for deployment.

2. **Parser Service**:
   - A separate FastAPI service responsible for parsing data from external sources.
   - This service accepts URLs via an API endpoint, fetches the content, and processes the data as required.
   - It can be called independently or by the Bookcrossing service.

3. **URL Getter**:
   - A utility service responsible for fetching and returning content from specified URLs.
   - Acts as a supporting service for the parser to retrieve data from external APIs or websites.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
- **Docker**: A containerization platform used to package the application, parser, and database into isolated, portable containers.
- **PostgreSQL**: A powerful, open-source object-relational database used for storing application data.
- **Uvicorn**: ASGI server for running the FastAPI application.
- **SQLAlchemy**: ORM for interacting with the PostgreSQL database in Python.
- **Docker Compose**: Tool for defining and running multi-container Docker applications.

## Key Features

- **Modular Architecture**: Each service (API, parser, database) is independent, making the system flexible and scalable.
- **API Integration**: The application provides HTTP endpoints to interact with the parser and fetch parsed data.
- **Containerization**: Using Docker, all services are isolated in their own containers, ensuring consistent behavior across environments.
- **Queue-based Parser Calls**: The parser service can be invoked via HTTP calls, and all services are orchestrated with Docker Compose for seamless management.


