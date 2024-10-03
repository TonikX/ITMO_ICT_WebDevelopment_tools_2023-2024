# Project Documentation

This project consists of a composition of services, including two web servers, a database, a Celery worker, and a Redis queue. These services are containerized and managed using Docker Compose for seamless orchestration.

## Overview of Services

### 1. **Web Server 1: Web application**

- **Purpose**: Provides parsing functionality for user-submitted tasks, including synchronous and asynchronous task execution.
- **Endpoints**:
  - `POST /parse`: Submits a parsing task and returns a `task_id` for tracking.
  - `GET /parser_results/{task_id}`: Fetches the status and result of a specific parsing task.
  - `GET /async_parser`: Submits a task to the background asynchronously without returning a `task_id`.
- **Dependencies**: 
  - Requires connection to the PostgreSQL database for task storage.
  - Uses Redis for task queuing and Celery for background processing.

For more information, refer to [WebApp](./WebApp.md).

### 2. **Web Server 2: Random User Fetching Service**

- **Purpose**: Fetches user data from an external API (`https://randomuser.me/api/`), stores the user data in the PostgreSQL database, and returns the serialized user data.
- **Endpoints**:
  - `GET /`: Fetches a random user, writes the data to the database, and returns the user in a serialized JSON format.
- **Dependencies**:
  - Requires connection to the PostgreSQL database for storing user data.

For more information, refer to [HttpParser](./HttpParser.md).

### 3. **PostgreSQL Database**

- **Purpose**: 
  - Serves as the main data store for the web services, storing task information and user data.
- **Ports**: 
  - Default: `5432`
- **Configuration**:
  - The database service is initialized with environment variables such as `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB`.

### 4. **Celery Worker**

- **Purpose**: 
  - Processes background tasks submitted by the web servers using Redis as the message broker.
  - The Celery worker listens for new tasks and performs the necessary background computation.
- **Dependencies**:
  - Requires connection to the Redis queue for task queuing and the PostgreSQL database for reading and writing task data.

### 5. **Redis Queue**

- **Purpose**: 
  - Acts as the message broker for Celery, managing task queuing and dispatching background jobs to the Celery worker.
- **Ports**:
  - Default: `6379`

## System Architecture

Here’s how the services interact:

- **Web Servers**: 
  - Web Server 1 interacts with users submitting parsing tasks and background processing (via Celery and Redis).
  - Web Server 2 fetches random user data and stores it in the database.
  
- **Database (PostgreSQL)**: 
  - Both web servers write data to and read from the PostgreSQL database.
  
- **Celery Worker**: 
  - Celery worker is responsible for executing background tasks dispatched from Web Server 1. It fetches tasks from the Redis queue and writes the results to the database.
  
- **Redis**: 
  - Redis serves as a message broker between Web Server 1 and the Celery worker.

## How to Run

The services are managed using Docker Compose. Here’s how to run the entire stack:

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create the environment files**:
   - Define any environment variables needed, such as database credentials (`POSTGRES_USER`, `POSTGRES_PASSWORD`, etc.), in an `.env` file.

3. **Docker Compose**:
   To start all services, use Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. **Access the Services**:
   - Web Server 1 (User Parsing Service) will be available at `http://localhost:8000`.
   - Web Server 2 (Random User Fetching Service) will be available at `http://localhost:8001`.
   - PostgreSQL is accessible at `localhost:5432` (if necessary for direct access).
   - Redis is running at `localhost:6379`.

5. **Shutting Down**:
   To stop the services:
   ```bash
   docker-compose down
   ```

### Docker Compose Configuration

Below is an example `docker-compose.yml` that outlines the structure of the services.

```yaml
version: "3.8"

services:
  db:
    image: postgres:16-bullseye
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
    volumes:
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "127.0.0.1:5433:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 5s
      timeout: 10s
      retries: 3

  parser:
    build:
      context: .
      dockerfile: Dockerfile.parser
    ports:
      - "127.0.0.1:8001:8000"
    depends_on:
      db:
        condition: service_healthy
    environment:
      - DB_URL=${DB_URL_ASYNC}
    healthcheck:
      test: ["CMD", "nc", "-z", "localhost", "8000"]
      interval: 5s
      timeout: 10s
      retries: 3

  redis:
    image: redis:latest
    ports:
      - "127.0.0.1:6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 10s
      retries: 3
  
  worker:
    build:
      context: .
      dockerfile: Dockerfile.worker
    depends_on:
      redis:
        condition: service_healthy
      parser:
        condition: service_healthy
    environment:
      - BROKER_URL=${BROKER_URL}
      - BACKEND_URL=${BACKEND_URL}
      - PARSER_URL=${PARSER_URL}

  web:
    build:
      context: .
      dockerfile: Dockerfile.web
    ports:
      - "127.0.0.1:8000:8000"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      - DB_URL=${DB_URL}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - JWT_ALGORITHM=${JWT_ALGORITHM}
      - DEFAULT_EXP_DELTA_MIN=${DEFAULT_EXP_DELTA_MIN}
      - PARSER_URL=${PARSER_URL}
      - BROKER_URL=${BROKER_URL}
      - BACKEND_URL=${BACKEND_URL}
```

## Environment Variables

| Variable          | Description                                |
|-------------------|--------------------------------------------|
| `POSTGRES_USER`    | PostgreSQL username                        |
| `POSTGRES_PASSWORD`| PostgreSQL password                        |
| `POSTGRES_DB`      | PostgreSQL database name                   |
| `DB_URL`           | Connection string for the PostgreSQL DB    |
| `DB_URL_ASYNC`        | Asynchronous connection string for the Redis queue |
| `JWT_SECRET_KEY`        | JWT Secret key for Web App authorization |
| `DEFAULT_EXP_DELTA_MIN`        | Token expiration time |
| `JWT_ALGORITHM`        | JWT authorization algorithm |
| `BROKER_URL`        | Task Queue Service URL (submission) |
| `BACKEND_URL`        | Task Queue Service URL (extraction) |

## Scaling the Services

You can scale the Celery workers if needed to handle a higher volume of background tasks:

```bash
docker-compose up --scale celery_worker=3
```

This will create 3 instances of the Celery worker to handle tasks in parallel.

## Testing the Endpoints

- **Web Server 1**:
  - Submit a parsing task:
    ```bash
    curl -X POST http://localhost:8000/parse -d '{"data": "test"}'
    ```
  - Check task status:
    ```bash
    curl http://localhost:8000/parser_results/{task_id}
    ```

- **Web Server 2**:
  - Fetch a random user:
    ```bash
    curl http://localhost:8001/
    ```
