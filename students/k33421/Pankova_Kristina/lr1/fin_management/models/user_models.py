from tokenize import String
from typing import List, Optional

from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel
import datetime
from typing import Optional

from pydantic import validator, EmailStr, field_validator
from sqlmodel import SQLModel, Field, Relationship

from models import *

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str
    budgets: List["BudgetTransaction"] = Relationship(back_populates="user")
    transactions: List["FinancialTransaction"] = Relationship(back_populates="user")

class UserInput(SQLModel):
    username: str
    password: str = Field(max_length=256, min_length=6)
    password2: str
    email: EmailStr = Field(sa_column=Column(String, index=True, unique=True))
    is_seller: bool = False

    @field_validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords don\'t match')
        return v


class UserLogin(SQLModel):
    username: str
    password: str