# Authentication API Documentation

## Introduction

This documentation provides details about the API endpoints for authentication and user management.

## Models

### Token

- **access_token**: `str`
- **token_type**: `str`

### TokenData

- **username**: `str | None`

### Hackathon

- **id**: `int`
- **name**: `str`
- **start_date**: `datetime.datetime`
- **end_date**: `datetime.datetime`

### Team

- **id**: `int`
- **name**: `str`
- **hackathon**: `Hackathon`
- **role**: `str`

### User

- **id**: `int`
- **username**: `str`
- **email**: `str | None`
- **full_name**: `str | None`
- **contact_number**: `str | None`
- **teams**: `list[Team] | None`

### UserCreateData

- **username**: `str`
- **password**: `str`
- **email**: `str | None`
- **full_name**: `str | None`
- **contact_number**: `str | None`

### UserPassword

- **password**: `str`

## Endpoints

### Login for Access Token

- **Method**: `POST`
- **URL**: `/token`
- **Request Body**: `OAuth2Form`
- **Response**: `Token`
- **Note**: Authenticates the user and returns an access token.

### Register User

- **Method**: `POST`
- **URL**: `/users`
- **Request Body**: `UserCreateData`
- **Response**: `User`
- **Note**: Registers a new user.

### Read Users

- **Method**: `GET`
- **URL**: `/users`
- **Response**: `list[User]`
- **Note**: Retrieves all users.

### Read Current User

- **Method**: `GET`
- **URL**: `/users/me/`
- **Response**: `User`
- **Note**: Retrieves the current user.

### Change Password

- **Method**: `POST`
- **URL**: `/users/change_password/`
- **Request Body**: `UserPassword`
- **Response**: `User`
- **Note**: Changes the password for the current user.

## Usage

- Make requests to the provided endpoints using appropriate HTTP methods and request bodies as described.

## Note

- Ensure to provide valid data formats and handle errors appropriately.
