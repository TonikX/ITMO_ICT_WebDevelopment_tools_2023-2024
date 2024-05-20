   from enum import Enum
# from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class ExpenseType(str, Enum):
    goal = "goal"
    expense = "expense"
    debt = "debt"


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
    expenses: list["Expense"] | None = Relationship(back_populates="user")
    incomes: list["Income"] | None = Relationship(back_populates="user")
    accounts: list["Account"] | None = Relationship(back_populates="user")
    categories: list["ExpenseCategory"] | None = Relationship(back_populates="user")
    sources: list["SourceOfIncome"] | None = Relationship(back_populates="user")


class ExpenseCategory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    type: ExpenseType
    limit_of_expenses: int | None
    user_id: int | None = Field(foreign_key="user.id")

    user: User | None = Relationship(back_populates="categories")
    expenses: list["Expense"] | None = Relationship(back_populates="category")


class SourceOfIncome(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    planning_to_receive: int | None
    user_id: int | None = Field(foreign_key="user.id")

    user: User | None = Relationship(back_populates="sources")
    incomes: list["Income"] | None = Relationship(back_populates="source")


class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    balance: int | None
    user_id: int | None = Field(foreign_key="user.id")

    user: User | None = Relationship(back_populates="accounts")
    expenses: list["Expense"] | None = Relationship(back_populates="account")
    incomes: list["Income"] | None = Relationship(back_populates="account")


class Expense(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    amount: int
    user_id: int | None = Field(default=None, foreign_key="user.id")
    account_id: int | None = Field(foreign_key="account.id")
    category_id: int | None = Field(foreign_key="expensecategory.id")

    user: User | None = Relationship(back_populates="expenses")
    account: Account | None = Relationship(back_populates="expenses")
    category: ExpenseCategory | None = Relationship(back_populates="expenses")


class Income(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    amount: int
    user_id: int | None = Field(foreign_key="user.id")
    source_id: int | None = Field(foreign_key="sourceofincome.id")
    account_id: int | None = Field(foreign_key="account.id")

    user: User | None = Relationship(back_populates="incomes")
    account: Account | None = Relationship(back_populates="incomes")
    source: SourceOfIncome | None = Relationship(back_populates="incomes")
