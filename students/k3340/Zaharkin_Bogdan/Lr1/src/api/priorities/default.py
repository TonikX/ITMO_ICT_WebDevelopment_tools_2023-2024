from sqlmodel import SQLModel


# Priority table
class PriorityDefault(SQLModel):
    name: str
