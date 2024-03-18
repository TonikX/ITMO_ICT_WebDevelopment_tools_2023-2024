# Users Endpoints

## Registration

**Endpoint:** `POST /registration`

**Description:** Register a new user with a username, password, and email.

**Request Body:**

```json
{
 "username": "string",
 "password": "string",
 "email": "string"
}
```
**Responses:**

- `200 OK`: Returns the registered user's data.
- `400 Bad Request`: If the username already exists.

## Login

**Endpoint:** `POST /login`

**Description:** Authenticate a user and obtain a JWT token.

**Request Body:**

```json
{
  "username": "string",
  "password": "string"
}
```
**Responses:**

- `200 OK`: Returns a JWT token.
- `401 Unauthorized`: If the username or password is invalid.

## Get Current User

**Endpoint:** `GET /user/me`

**Description:** Retrieve the current authenticated user's profile information.

**Headers:**

- #### Authorization: 
Bearer <token>
  
**Responses:**

- `200 OK`: Returns the user's profile data.
- `401 Unauthorized`:  If the user is not authenticated.

## Delete User

**Endpoint:** `DELETE /user/delete{user_id}`

**Description:** Delete a user by ID.

**Path Parameters:**

- `user_id`: int

**Responses:**

- `200 OK`: If the user was successfully deleted.
- `401 Not found`: If the user was not found.