from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class AccountType(str, Enum):
    goal = "goal"
    expense = "expense"
    debt = "debt"

class User(SQLModel, table=True):
    username: str = Field(primary_key=True)
    email: str
    password: str
    expenses: List["Expense"] = Relationship(back_populates="user")
    incomes: List["Income"] = Relationship(back_populates="user")
    accounts: List["Account"] = Relationship(back_populates="user")

class ExpenseCategory(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    user: str = Field(foreign_key="user.username")
    account_type: AccountType
    limit_of_expenses: int
    expenses: List["Expense"] = Relationship(back_populates="category")
    accounts: List["Account"] = Relationship(back_populates="categories", link_model="Expense")

class SourceOfIncome(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    user: str = Field(foreign_key="user.username")
    planning_to_receive: int
    incomes: List["Income"] = Relationship(back_populates="source")

class Account(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    user: str = Field(foreign_key="user.username")
    balance: int
    expenses: List["Expense"] = Relationship(back_populates="account")
    incomes: List["Income"] = Relationship(back_populates="account")
    categories: List[ExpenseCategory] = Relationship(back_populates="accounts", link_model="Expense")

class Expense(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user: str = Field(foreign_key="user.username")
    account_name: str = Field(foreign_key="account.name")
    category_name: str = Field(foreign_key="expensecategory.name")

class Income(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user: str = Field(foreign_key="user.username")
    source_name: str = Field(foreign_key="sourceofincome.name")
    account_name: str = Field(foreign_key="account.name")
