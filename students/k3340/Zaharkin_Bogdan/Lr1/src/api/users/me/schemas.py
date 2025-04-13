from pydantic import BaseModel


# User response with JWT model
class UserJWTResponse(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    access_token: str | None

# User response model
class UserResponse(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
