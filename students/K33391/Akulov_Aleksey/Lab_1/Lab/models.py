import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import validator


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(index=True)
    password: str
    balance: Optional["Balance"] = Relationship(back_populates="user")
    created_at: datetime.datetime = Field(default=datetime.datetime.now())


class UserInput(SQLModel):
    username: str
    password: str
    password2: str

    @validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords don\'t match')
        return v


class UserLogin(SQLModel):
    username: str
    password: str


class Balance(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="balance")
    total_budget: int = Field(default=0)
    saving_target: int = Field(default=0)
    categories: List["Category"] = Relationship(back_populates="balance")


class Category(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    limit: Optional[int] = None
    balance_id: int = Field(foreign_key="balance.id")
    balance: Balance = Relationship(back_populates="categories")
    transactions: List["Transaction"] = Relationship(back_populates="category")


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Transaction(SQLModel, table=True):
    id: int = Field(primary_key=True)
    category_id: int = Field(foreign_key="category.id")
    category: Category = Relationship(back_populates="transactions")
    type: TransactionType
    value: int
    created_at: datetime.datetime = Field(default=datetime.datetime.now())


class TransactionsCreate(SQLModel):
    category_id: int
    type: TransactionType
    value: int


class TransactionsUpdate(SQLModel):
    category_id: int
    type: TransactionType
    value: int


class TransactionRead(SQLModel):
    id: int
    category_id: int
    type: TransactionType
    value: int
    created_at: datetime.datetime


class CategoryRead(SQLModel):
    id: int
    name: str
    limit: Optional[int]
    transactions: List[TransactionRead]


class BalanceRead(SQLModel):
    id: int
    total_budget: int
    saving_target: int
    categories: List[CategoryRead]


class UserRead(SQLModel):
    id: int
    username: str
    balance: BalanceRead
    created_at: datetime.datetime