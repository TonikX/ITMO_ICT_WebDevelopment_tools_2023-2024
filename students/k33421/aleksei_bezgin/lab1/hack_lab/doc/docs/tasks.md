# Tasks API Documentation

## Introduction

This documentation provides details about the API endpoints for managing tasks.

## Models

### TaskCreateData

- **title**: `str`
- **description**: `str`
- **requirements**: `str`
- **evaluation_criteria**: `str`
- **hackathon_id**: `int`

### TaskUpdateData

- **title**: `str | None`
- **description**: `str | None`
- **requirements**: `str | None`
- **evaluation_criteria**: `str | None`
- **hackathon_id**: `int | None`

## Endpoints

### Get All Tasks

- **Method**: `GET`
- **URL**: `/tasks/`
- **Response**: `list[Task]`

### Get Task by ID

- **Method**: `GET`
- **URL**: `/tasks/{task_id}`
- **Parameter**: `task_id`: `int`
- **Response**: `Task`

### Create Task

- **Method**: `POST`
- **URL**: `/tasks/`
- **Request Body**: `TaskCreateData`
- **Response**: `Task`

### Update Task

- **Method**: `PATCH`
- **URL**: `/tasks/{task_id}`
- **Parameter**: `task_id`: `int`
- **Request Body**: `TaskUpdateData`
- **Response**: `Task`

### Delete Task

- **Method**: `DELETE`
- **URL**: `/tasks/{task_id}`
- **Parameter**: `task_id`: `int`
- **Response**: `str`

## Usage

- Make requests to the provided endpoints using appropriate HTTP methods and request bodies as described.

## Note

- Ensure to provide valid data formats and handle errors appropriately.
