# Hackathons API Documentation

## Introduction

This documentation provides details about the API endpoints for managing hackathons.

## Models

### Team

- **id**: `int`
- **name**: `str`

### Task

- **id**: `int`
- **title**: `str`
- **description**: `str`
- **requirements**: `str`
- **evaluation_criteria**: `str`

### Hackathon

- **id**: `int | None`
- **name**: `str`
- **start_date**: `datetime.datetime`
- **end_date**: `datetime.datetime`
- **tasks**: `list[Task]`
- **teams**: `list[Team]`

### HackathonCreateData

- **name**: `str`
- **start_date**: `datetime.datetime`
- **end_date**: `datetime.datetime`

### HackathonUpdateData

- **name**: `str | None`
- **start_date**: `datetime.datetime | None`
- **end_date**: `datetime.datetime | None`

## Endpoints

### Get All Hackathons

- **Method**: `GET`
- **URL**: `/hackathons/`
- **Response**: `list[Hackathon]`

### Get Hackathon by ID

- **Method**: `GET`
- **URL**: `/hackathons/{hackathon_id}`
- **Parameter**: `hackathon_id`: `int`
- **Response**: `Hackathon`

### Create Hackathon

- **Method**: `POST`
- **URL**: `/hackathons/`
- **Request Body**: `HackathonCreateData`
- **Response**: `Hackathon`

### Update Hackathon

- **Method**: `PATCH`
- **URL**: `/hackathons/{hackathon_id}`
- **Parameter**: `hackathon_id`: `int`
- **Request Body**: `HackathonUpdateData`
- **Response**: `Hackathon`

### Delete Hackathon

- **Method**: `DELETE`
- **URL**: `/hackathons/{hackathon_id}`
- **Parameter**: `hackathon_id`: `int`
- **Response**: `str`

## Usage

- Make requests to the provided endpoints using appropriate HTTP methods and request bodies as described.

## Note

- Ensure to provide valid data formats and handle errors appropriately.
