from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class TripBase(BaseModel):
    destination: str
    start_date: str
    end_date: str

class TripCreate(TripBase):
    user_id: int

class Trip(TripBase):
    id: int

    class Config:
        orm_mode = True
class UserPasswordChange(BaseModel):
    old_password: str
    new_password: str