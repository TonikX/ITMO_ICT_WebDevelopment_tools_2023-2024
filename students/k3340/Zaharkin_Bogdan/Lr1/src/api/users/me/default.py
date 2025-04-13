from pydantic import BaseModel


# User create model
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str

# User login model
class UserLogin(BaseModel):
    username: str
    password: str
