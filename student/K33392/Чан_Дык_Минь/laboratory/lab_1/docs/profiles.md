# Profiles Endpoints

## Get Profile

**Endpoint:** `GET /profile/{profile_id}`

**Description:** Retrieve a user profile by ID.

**Path Parameters:**

- `profile_id: int`

**Responses:**

- `200 OK`: Returns the profile data and associated reviews.
- `404 Not Found`: If the profile was not found.

## Create Profile

**Endpoint:** `POST /profile`

**Description:** Create a new user profile.

**Headers:**

- `Authorization: Bearer <token>`

**Request Body:**

```json
{
    "full_name": "string",
    "age": "int",
    "gender": "Gender",
    "address": "string",
    "skills": "string",
    "travel_experience": "string",
    "hobby": "string"
}
```

**Responses:**

- `200 OK`: Returns the created profile data.
- `401 Unauthorized`: If the user is not authenticated.

## Delete Profile

**Endpoint:** `DELETE /profile/delete`

**Description:** Delete the current authenticated user's profile.
**Headers:**

- `Authorization: Bearer <token>`

**Responses:**

- `200 OK`: If the profile was successfully deleted.
- `401 Unauthorized`: If the user is not authenticated.
- `404 Not Found`: If the user's profile was not found.

## Update Profile

**Endpoint:** `PATCH /profile`

**Description:** Update the current authenticated user's profile.
**Headers:**

- `Authorization: Bearer <token>`

**Request body:**
```json
{
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "image_url": "string"
}
```

**Responses:**

- `200 OK`: Returns the updated profile data.
- `401 Unauthorized`: If the user is not authenticated.
- `404 Not Found`: If the user's profile was not found.