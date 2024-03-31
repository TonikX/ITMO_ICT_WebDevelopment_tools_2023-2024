from sqlmodel import Field, SQLModel
from pydantic import BaseModel


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


class Healthcheck(BaseModel):
    ok: str
