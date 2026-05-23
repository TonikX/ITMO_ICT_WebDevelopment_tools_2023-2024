from sqlmodel import SQLModel


class PriorityCreate(SQLModel):
    name: str
    weight: int = 1
    description: str | None = None


class PriorityUpdate(SQLModel):
    name: str | None = None
    weight: int | None = None
    description: str | None = None


class PriorityRead(SQLModel):
    id: int
    name: str
    weight: int
    description: str | None = None
