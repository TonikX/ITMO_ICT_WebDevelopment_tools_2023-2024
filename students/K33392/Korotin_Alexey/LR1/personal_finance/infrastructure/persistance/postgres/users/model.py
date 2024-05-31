from sqlmodel import SQLModel, Field


class UserModel(SQLModel, table=True):
    id: int = Field(primary_key=True)
    first_name: str
    last_name: str
    login: str
    password: str
