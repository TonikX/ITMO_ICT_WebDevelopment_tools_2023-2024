# Submissions API Documentation

## Introduction

This documentation provides details about the API endpoints for managing submissions.

## Models

### Submission

- **id**: `int`
- **submission_data**: `str`
- **evaluation**: `int | None`

### SubmissionCreateData

- **submission_data**: `str`
- **evaluation**: `int | None`
- **team_id**: `int`
- **task_id**: `int`

### SubmissionUpdateData

- **submission_data**: `str | None`
- **evaluation**: `int | None`
- **team_id**: `int | None`
- **task_id**: `int | None`

## Endpoints

### Get All Submissions

- **Method**: `GET`
- **URL**: `/submissions/`
- **Response**: `list[Submission]`

### Get Submission by ID

- **Method**: `GET`
- **URL**: `/submissions/{submission_id}`
- **Parameter**: `submission_id`: `int`
- **Response**: `Submission`

### Create Submission

- **Method**: `POST`
- **URL**: `/submissions/`
- **Request Body**: `SubmissionCreateData`
- **Response**: `Submission`

### Update Submission

- **Method**: `PATCH`
- **URL**: `/submissions/{submission_id}`
- **Parameter**: `submission_id`: `int`
- **Request Body**: `SubmissionUpdateData`
- **Response**: `Submission`

### Delete Submission

- **Method**: `DELETE`
- **URL**: `/submissions/{submission_id}`
- **Parameter**: `submission_id`: `int`
- **Response**: `str`

## Usage

- Make requests to the provided endpoints using appropriate HTTP methods and request bodies as described.

## Note

- Ensure to provide valid data formats and handle errors appropriately.
