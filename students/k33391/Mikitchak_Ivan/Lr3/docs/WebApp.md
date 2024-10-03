# Web Application Documentation

This web server provides functionality to submit parsing tasks and retrieve their results. The server handles parsing both synchronously and asynchronously using Celery for background task management.

## API Endpoints

### 1. `POST /parse`

- **Description**: Submits a user parsing task to the server.
- **Request Type**: `POST`
- **Request Body**: 
  - Should contain data for the task to be parsed. The exact format depends on the task requirements.
- **Response**: 
  - `200 OK`: Task successfully submitted.
  - Response body will contain a `task_id` which can be used to check the status of the task.
  
- **Example Request**:
  ```bash
  curl -X POST http://<server_url>/parse \
       -H "Content-Type: application/json" \
       -d '{"data": "sample parsing data"}'
  ```
  
- **Example Response**:
  ```json
  {
    "task_id": "123e4567-e89b-12d3-a456-426614174000"
  }
  ```

### 2. `GET /parser_results/{task_id}`

- **Description**: Checks the status of a submitted parsing task.
- **Request Type**: `GET`
- **Path Parameter**:
  - `task_id` (string): The ID of the task returned from the `POST /parse` request.
  
- **Response**:
  - `200 OK`: Returns the current status of the task.
  - Possible task statuses:
    - `PENDING`: Task is still being processed.
    - `FAILURE`: Task failed during processing.
    - `SUCCESS`: Task completed successfully. The result of the task will also be included in the response if the status is `SUCCESS`.
    
- **Example Request**:
  ```bash
  curl -X GET http://<server_url>/parser_results/123e4567-e89b-12d3-a456-426614174000
  ```

- **Example Response** (Status: PENDING):
  ```json
  {
    "task_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "PENDING"
  }
  ```

- **Example Response** (Status: SUCCESS):
  ```json
  {
    "task_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "SUCCESS",
    "result": {
      "parsed_data": "parsed output"
    }
  }
  ```

### 3. `GET /async_parser`

- **Description**: Asynchronously submits a parsing task to the background. This does not return a task ID or immediate confirmation of the task being processed.
- **Request Type**: `GET`
- **Response**:
  - `200 OK`: Task was successfully submitted in the background. However, no `task_id` is returned, and the task is run asynchronously without status tracking.

- **Example Request**:
  ```bash
  curl -X GET http://<server_url>/async_parser
  ```

- **Example Response**:
  ```json
  {
    "message": "Task submitted asynchronously"
  }
  ```

## Error Handling

- **400 Bad Request**: Invalid or missing data in request.
- **404 Not Found**: Task ID not found for `GET /parser_results/{task_id}`.
- **500 Internal Server Error**: A server error occurred.

## Background Task Handling

- The server uses Celery to handle background tasks such as parsing asynchronously.
- Tasks submitted through `POST /parse` can be tracked using the task ID, while tasks submitted through `GET /async_parser` cannot be tracked, as they are processed without returning a `task_id`.

## Example Workflow

1. A user submits a task through the `POST /parse` endpoint and receives a `task_id`.
2. The user can check the status of the task using the `GET /parser_results/{task_id}` endpoint.
3. Alternatively, a user can submit an asynchronous task through the `GET /async_parser` endpoint. This task will be processed in the background, but no task status or result tracking is available.