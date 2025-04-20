from typing import Optional

from pydantic import BaseModel


class InterestBase(BaseModel):
    name: str
    description: Optional[str] = None


class InterestCreate(InterestBase):
    pass


class InterestRead(InterestBase):
    id: int
