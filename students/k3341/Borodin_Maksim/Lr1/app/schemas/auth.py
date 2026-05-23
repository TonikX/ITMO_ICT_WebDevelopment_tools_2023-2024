from sqlmodel import SQLModel


class RegisterRequest(SQLModel):
    email: str
    username: str
    password: str


class LoginRequest(SQLModel):
    email: str
    password: str


class TokenResponse(SQLModel):
    access_token: str
    token_type: str = "bearer"
