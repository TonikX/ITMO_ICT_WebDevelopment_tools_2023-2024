from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from .user_models import *

class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    budgets: List["BudgetTransaction"] = Relationship(back_populates="category")
    transactions: List["FinancialTransaction"] = Relationship(back_populates="category")

class BudgetTransaction(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    category_id: int = Field(default=None, foreign_key="category.id")
    amount: float
    user: Optional[User] = Relationship(back_populates="budgets")
    category: Optional[Category] = Relationship(back_populates="budgets")

class FinancialTransaction(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    category_id: int = Field(default=None, foreign_key="category.id")
    amount: float
    date: str
    user: Optional[User] = Relationship(back_populates="transactions")
    category: Optional[Category] = Relationship(back_populates="transactions")

class Goal(SQLModel):
    id: int = Field(default=None, primary_key=True)
    description: str
    target_amount: float
    user_id: int

