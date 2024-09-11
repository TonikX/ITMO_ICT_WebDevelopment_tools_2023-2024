from pydantic import BaseModel


class Queue(BaseModel):
    id: str
    status: str
    result: int | None
