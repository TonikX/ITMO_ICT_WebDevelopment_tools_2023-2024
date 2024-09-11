from sqlmodel import Field, SQLModel

class Vinil(SQLModel, table=True):
    id: int = Field(primary_key=True)
    author: str
    name: str
    cost: str