from sqlmodel import SQLModel, Field

class TransportDefault(SQLModel):
    name: str
    description: str
    avalible_seats: int
    price: int

class Transport(TransportDefault, table=True):
    id: int = Field(default=None, primary_key=True)