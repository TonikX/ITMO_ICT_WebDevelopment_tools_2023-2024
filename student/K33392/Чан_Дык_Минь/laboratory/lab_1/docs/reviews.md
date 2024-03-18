# Reviews Endpoints

## Get User Reviews

**Endpoint:** `GET /reviews`

**Description:** Retrieve all reviews associated with the current authenticated user.

**Headers:**

- `Authorization: Bearer <token>`

**Responses:**

- `200 OK`: Returns a list of the user's reviews.
- `404 Not Found`: If no reviews were found for the current user.
- `401 Unauthorized`: If the user is not authenticated.

## Get Profile Reviews

**Endpoint:** `GET /review/{user_profile_id}`

**Description:** Retrieve all reviews for a specific user profile.

**Path Parameters:**

- `user_profile_id: int`

**Responses:**

- `200 OK`: Returns a list of reviews for the specified user profile.

## Create Review

**Endpoint:** `POST /review/{user_profile_id}`

**Description:** Create a new review for a specific user profile.

**Path Parameters:**

- `user_profile_id: int`

**Headers:**

- `Authorization: Bearer <token>`

**Request Body:**

```json
{
 "review_content": "string"
}
```

**Responses:**

- `200 OK`: Returns the created review data.
- `401 Unauthorized`: If the user is not authenticated.

Delete Review
-------------

**Endpoint:** `DELETE /review/delete{review_id}`

**Description:** Delete a review by ID.

**Path Parameters:**

- `review_id: int`

**Headers:**

- `Authorization: Bearer <token>`

**Responses:**

- `200 OK`: If the review was successfully deleted.
- `404 Not Found`: If the review was not found.
- `401 Unauthorized`: If the user is not authenticated.

Update Review
-------------

**Endpoint:** `PATCH /review{review_id}`

**Description:** Update a review by ID.

**Path Parameters:**

- `review_id: int`

**Headers:**

- `Authorization: Bearer <token>`

**Request Body:**

```json
{
 "review_content": "string"
}
```
**Responses:**

- `200 OK`: Returns the updated review data.
- `404 Not Found`: If the review was not found.
- `401 Unauthorized`: If the user is not authenticated.