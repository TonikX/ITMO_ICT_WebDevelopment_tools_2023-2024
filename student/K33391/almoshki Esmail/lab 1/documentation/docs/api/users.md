# User Endpoints

## Get Users List
**GET /users_list**  
Response: Returns a list of users in JSON format.

## Get User by Name
**GET /user/{name}**  
Response: Returns the user data matching the provided name.

## Create User
**POST /user**  
Request Body:  
```json
{
    "name": "Emsa",
    "age": 23
}
```