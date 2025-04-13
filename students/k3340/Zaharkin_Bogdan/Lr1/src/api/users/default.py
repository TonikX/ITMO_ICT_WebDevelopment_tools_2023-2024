from sqlmodel import SQLModel


# User table
class UserDefault(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    username: str
    email: str
