from datetime import datetime
from enum import Enum
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class CategoryEnum(Enum):
    salary = 'salary'
    home = 'home'
    health = 'health'
    sports = 'sports'
    food = 'food'
    technology = 'technology'
    cashback = 'cashback'
    gifts = 'gifts'
    other = 'other'


class OperationEnum(Enum):
    income = 'income'  # revenue
    outcome = 'outcome'  # expense


class CategoryOperationLink(SQLModel, table=True):  # many-many
    id: Optional[int] = Field(default=None, primary_key=True, unique=True)
    category_id: Optional[int] = Field(
        default=None, foreign_key="category.id", primary_key=True
    )
    operation_id: Optional[int] = Field(
        default=None, foreign_key="operation.id", primary_key=True
    )
    amount: Optional[float] = Field(default=None)


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category: CategoryEnum = Field(unique=True)
    limit: float = Field(default=0.0)
    current: float = Field(default=0.0)
    operations: Optional[List["Operation"]] = Relationship(back_populates="categories",
                                                           link_model=CategoryOperationLink)  # many-many
    favourite_category: List["Customer"] = Relationship(back_populates="favourite_category")  # 1-many # *


class Operation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    operation: OperationEnum = Field(unique=True)
    limit: float = Field(default=0.0)
    alias: Optional[str] = Field(default=None, nullable=True)
    categories: Optional[List[Category]] = Relationship(back_populates="operations",
                                                        link_model=CategoryOperationLink)  # many-many


class User(SQLModel):
    username: str = Field(unique=True, index=True, nullable=False)
    password: str = Field(nullable=False)
    favourite_category_id: Optional[int] = Field(default=None, foreign_key="category.id")  # 1-many


class Customer(User, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    balance: float = Field(default=0.0, nullable=False)
    favourite_category: Optional[Category] = Relationship(back_populates="favourite_category")  # 1-many # *


class CustomerCategory(User):
    favourite_category: Optional[Category] = None  # *


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(default=None, nullable=False)
    amount: float = Field(default=None, nullable=False)
    customer_id: Optional[int] = Field(default=None, foreign_key="customer.id")  # 1-many
    category_operation_link_id: Optional[int] = Field(default=None, foreign_key="categoryoperationlink.id")  # 1-many
