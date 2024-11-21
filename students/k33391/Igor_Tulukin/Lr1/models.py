from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class BudgetBase(SQLModel):
    amount: float
    date_valid_until: datetime
    user_id: int = Field(foreign_key="user.id")
    category_id: int = Field(foreign_key="category.id")


class PageBase(SQLModel):
    title: str
    url: str


class Page(PageBase, table=True):
    id: int = Field(default=None, primary_key=True)


class BudgetDisplay(BudgetBase):
    user: Optional["User"] = None
    category: Optional["Category"] = None
    incomes: Optional[List["Income"]] = None
    expenses: Optional[List["Expense"]] = None


class Budget(BudgetBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user: Optional["User"] = Relationship(back_populates="budgets")
    category: Optional["Category"] = Relationship(back_populates="budgets")

    incomes: Optional[List["Income"]] = Relationship(back_populates="budget")
    expenses: Optional[List["Expense"]] = Relationship(back_populates="budget")


class UserBase(SQLModel):
    username: str
    email: str
    password: str


class UserDisplay(UserBase):
    categories: List["Category"] = None
    budgets: List["Budget"] = None


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    categories: List["Category"] = Relationship(back_populates="user", link_model=Budget)
    budgets: List["Budget"] = Relationship(back_populates="user")


class CategoryBase(SQLModel):
    name: str
    description: str


class CategoryDisplay(CategoryBase):
    budgets: List["Budget"] = None
    user: List["User"] = None


class Category(CategoryBase, table=True):
    id: int = Field(default=None, primary_key=True)
    budgets: List["Budget"] = Relationship(back_populates="category")
    user: List["User"] = Relationship(back_populates="categories", link_model=Budget)


class IncomeBase(SQLModel):
    amount: float
    description: str
    date: datetime = Field(default=datetime.utcnow)
    budget_id: int = Field(foreign_key="budget.id")


class IncomeDisplay(IncomeBase):
    budget: Budget = None


class Income(IncomeBase, table=True):
    id: int = Field(default=None, primary_key=True)
    budget: Budget = Relationship(back_populates="incomes",
                                          sa_relationship_kwargs={
                                              "cascade": "all, delete",
                                          }
                                          )


class ExpenseBase(SQLModel):
    amount: float
    description: str
    date: datetime = Field(default=datetime.utcnow)
    budget_id: int = Field(foreign_key="budget.id")


class ExpenseDisplay(ExpenseBase):
    budget: Budget = None


class Expense(ExpenseBase, table=True):
    id: int = Field(default=None, primary_key=True)
    budget: Budget = Relationship(back_populates="expenses",
                                          sa_relationship_kwargs={
                                              "cascade": "all, delete",
                                          }
                                          )

