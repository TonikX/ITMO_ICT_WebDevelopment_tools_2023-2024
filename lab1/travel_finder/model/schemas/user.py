from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr
from typing_extensions import List

from model.models.models import Gender, TravelStyle
from model.schemas.user_interest import UserInterestRead


class UserBase(BaseModel):
    name: str
    email: EmailStr
    bio: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Gender] = None
    country: Optional[str] = None
    languages: Optional[str] = None
    travel_style: Optional[TravelStyle] = None


class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Gender] = None
    country: Optional[str] = None
    languages: Optional[str] = None
    travel_style: Optional[TravelStyle] = None


class UserRead(UserBase):
    id: int
    created_at: datetime
    user_interests: List[UserInterestRead] = []

class UserPasswordChange(BaseModel):
    old_password: str
    new_password: str