from typing import Optional

from pydantic import BaseModel


class PriorityBase(BaseModel):
    level: str
    description: Optional[str]


class PriorityCreate(PriorityBase):
    pass


class Priority(PriorityBase):
    id: int

    class Config:
        from_attributes = True
