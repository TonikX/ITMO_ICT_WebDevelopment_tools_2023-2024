from sqlmodel import SQLModel, Field


class LocationDefault(SQLModel):
    name: str
    description: str
    country: str

class Location(LocationDefault, table=True):
    id: int = Field(default=None, primary_key=True)
