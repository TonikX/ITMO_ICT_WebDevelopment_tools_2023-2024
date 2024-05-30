from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class UserBase(SQLModel):
    username: str
    email: str
    password: str


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    categories: List["Category"] = Relationship(back_populates="user")
    incomes: List["Income"] = Relationship(back_populates="user")
    expenses: List["Expense"] = Relationship(back_populates="user")
    budgets: List["Budget"] = Relationship(back_populates="user")


class CategoryBase(SQLModel):
    name: str
    description: str
    user_id: int = Field(foreign_key="user.id")


class Category(CategoryBase, table=True):
    id: int = Field(default=None, primary_key=True)
    incomes: List["Income"] = Relationship(back_populates="category")
    expenses: List["Expense"] = Relationship(back_populates="category")
    budgets: List["Budget"] = Relationship(back_populates="category")
    user: User = Relationship(back_populates="categories")


class IncomeBase(SQLModel):
    amount: float
    description: str
    date: datetime = Field(default=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    category_id: int = Field(foreign_key="category.id")


class Income(IncomeBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user: User = Relationship(back_populates="incomes")
    category: Category = Relationship(back_populates="incomes")


class ExpenseBase(SQLModel):
    amount: float
    description: str
    date: datetime = Field(default=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    category_id: int = Field(foreign_key="category.id")


class Expense(ExpenseBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user: User = Relationship(back_populates="expenses")
    category: Category = Relationship(back_populates="expenses")


class BudgetBase(SQLModel):
    amount: float
    date_valid_until: datetime
    user_id: int = Field(foreign_key="user.id")
    category_id: int = Field(foreign_key="category.id")


class Budget(BudgetBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user: User = Relationship(back_populates="budgets")
    category: Category = Relationship(back_populates="budgets")
