from typing import Optional

from pydantic import BaseModel


class UserInterestCreate(BaseModel):
    user_id: int
    interest_id: int
    level: Optional[int] = None


class InterestShort(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class UserInterestRead(BaseModel):
    user_id: int
    interest: InterestShort
    level: Optional[int]