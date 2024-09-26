import datetime
from enum import Enum
from typing import Optional, List
from pydantic import validator
from sqlmodel import SQLModel, Field, Relationship



class UserInput(SQLModel):
    username: str
    password: str
    password2: str
    email: str

    @validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords don\'t match')
        return v


class UserLogin(SQLModel):
    username: str
    password: str

