# Trips Endpoints

## List All Trips

**Endpoint:** `GET /trip`

**Description:** Retrieve a list of all trips.

**Responses:**

- `200 OK`: Returns a list of trips.

## Get Trip Details

**Endpoint:** `GET /trip/{trip_id}`

**Description:** Retrieve details of a specific trip, including associated users.

**Path Parameters:**

- `trip_id: int`

**Responses:**

- `200 OK`: Returns the trip details and associated users.
- `404 Not Found`: If the trip was not found.

## Create Trip

**Endpoint:** `POST /trip`

**Description:** Create a new trip.

**Headers:**

- `Authorization: Bearer <token>`

**Request Body:**

```json
{
 "departure": "string",
 "destination": "string",
 "date_start": "date",
 "date_end": "date",
 "estimated_cost": "float",
 "trip_status": "string",
 "other_details": "string"
}
```

**Responses:**

- `200 OK`: Returns the created trip data.
- `401 Not Found`: If the user is not authenticated.

## Delete Trip

**Endpoint:** `DELETE /trip/delete{trip_id}`

**Description:** Delete a trip by ID.

**Path Parameters:**

- `trip_id: int`

**Headers:**

- `Authorization: Bearer <token>`


**Responses:**

- `200 OK`: If the trip was successfully deleted.
- `404 Not Found`: If the trip was not found.
- `401 Not Found`: If the user is not authenticated.

## Update Trip

**Endpoint:** `PATCH /trip/{trip_id}`

**Description:** Update a trip by ID.

**Path Parameters:**

- `trip_id: int`

**Headers:**

- `Authorization: Bearer <token>`

**Request Body:**

```json
{
 "departure": "string",
 "destination": "string",
 "date_start": "date",
 "date_end": "date",
 "estimated_cost": "float",
 "trip_status": "string",
 "other_details": "string"
}
```

**Responses:**

- `200 OK`: Returns the updated trip data.
- `404 Not Found`: If the trip was not found.
- `401 Not Found`: If the user is not authenticated.


# Trip Requests Endpoints

## Get TRip Requests

**Endpoint:** `GET /trip/{trip_id}/trip-requests`

**Description:** Retrieve all trip requests for a specific trip.

**Path Parameters:**

- `trip_id: int`

**Headers:**

- `Authorization: Bearer <token>`


**Responses:**

- `200 OK`: Returns a list of trip requests.
- `404 Not Found`: If the trip was not found.
- `401 Not Found`: If the user is not authenticated.

## Delete TRip Requests

**Endpoint:** `DELETE /trip/delete{trip_id}/trip-requests`

**Description:** Delete a trip request by ID.

**Path Parameters:**

- `trip_request_id: int`

**Headers:**

- `Authorization: Bearer <token>`


**Responses:**

- `200 OK`: If the trip request was successfully deleted.
- `404 Not Found`: If the trip was not found.
- `401 Not Found`: If the user is not authenticated.

## Create Trip Request

**Endpoint:** `POST /trip/{user_id}/trip-request`

**Description:** Create a new trip request for a specific user.

**Path Parameters:**

- `user_id: int`

**Headers:**

- `Authorization: Bearer <token>`

**Request Body:**

```json
{
  "message": "string",
  "request_status": "string",
  "trip_id": "int"
}
```

**Responses:**

- `200 OK`: Returns the created trip request data.
- `404 Not Found`: If the user has already requested for the specified trip.
- `401 Not Found`: If the user is not authenticated.


## Add User to Trip
**Endpoint:** `POST /trip/{trip_id}/add-user/{user_id}`

**Description:** Add a user to a specific trip.

**Path Parameters:**

`trip_id: int`
`user_id: int`

**Headers:**

`Authorization: Bearer <token>`

**Responses:**

- `200 OK`: If the user was successfully added to the trip.
- `404 Not Found`: If the trip or user was not found.
- `401 Unauthorized`: If the user is not authenticated.
  
## Remove User from Trip

**Endpoint:** `DELETE /trip/{trip_id}/remove-user/{user_id}`

**Description:** Remove a user from a specific trip.

**Path Parameters:**

`trip_id: int`
`user_id: int`

**Headers:**

`Authorization: Bearer <token>`

**Responses:**

`200 OK`: If the user was successfully removed from the trip.
`404 Not Found`: If the trip or user was not found in the trip.
`401 Unauthorized`: If the user is not authenticated.