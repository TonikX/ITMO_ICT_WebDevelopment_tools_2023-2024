# Teams API Documentation

## Introduction

This documentation provides details about the API endpoints for managing teams.

## Models

### MemberBase

- **id**: `int`
- **role**: `str`

### Member

- **id**: `int`
- **username**: `str`
- **full_name**: `str | None`
- **email**: `str | None`
- **contact_number**: `str | None`

### Hackathon

- **id**: `int`
- **name**: `str`
- **start_date**: `datetime.datetime`
- **end_date**: `datetime.datetime`

### Team

- **id**: `int`
- **name**: `str`
- **hackathon**: `Hackathon`
- **members**: `list[Member] | None`

### TeamCreateData

- **name**: `str`
- **hackathon_id**: `int`
- **members**: `list[MemberBase] | None`

### TeamUpdateData

- **name**: `str | None`
- **hackathon_id**: `int | None`

## Endpoints

### Get All Teams

- **Method**: `GET`
- **URL**: `/teams/`
- **Response**: `list[Team]`

### Get Team by ID

- **Method**: `GET`
- **URL**: `/teams/{team_id}`
- **Parameter**: `team_id`: `int`
- **Response**: `Team`

### Create Team

- **Method**: `POST`
- **URL**: `/teams/`
- **Request Body**: `TeamCreateData`
- **Response**: `Team`

### Add Member to Team

- **Method**: `POST`
- **URL**: `/teams/{team_id}/add_member`
- **Parameter**: `team_id`: `int`
- **Request Body**: `MemberBase`
- **Response**: `Team`

### Update Team

- **Method**: `PATCH`
- **URL**: `/teams/{team_id}`
- **Parameter**: `team_id`: `int`
- **Request Body**: `TeamUpdateData`
- **Response**: `Team`

### Delete Team

- **Method**: `DELETE`
- **URL**: `/teams/{team_id}`
- **Parameter**: `team_id`: `int`
- **Response**: `str`

### Kick Member from Team

- **Method**: `DELETE`
- **URL**: `/teams/{team_id}/kick_member/{member_id}`
- **Parameters**: 
  - `team_id`: `int`
  - `member_id`: `int`
- **Response**: `str`

## Usage

- Make requests to the provided endpoints using appropriate HTTP methods and request bodies as described.

## Note

- Ensure to provide valid data formats and handle errors appropriately.
