from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: str | None = None
    full_name: str | None = None


class UserCreateData(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    password: str


class UserPassword(BaseModel):
    password: str
