from sqlmodel import Field, SQLModel

class Product(SQLModel, table=True):
    prod_id: int = Field(primary_key=True)
    title: str
    name: str
    cost: str