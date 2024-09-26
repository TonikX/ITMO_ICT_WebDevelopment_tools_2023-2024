from sqlmodel import Field, SQLModel

class Flat(SQLModel, table=True):
    flat_id: int = Field(primary_key=True)
    size: str
    cost: str