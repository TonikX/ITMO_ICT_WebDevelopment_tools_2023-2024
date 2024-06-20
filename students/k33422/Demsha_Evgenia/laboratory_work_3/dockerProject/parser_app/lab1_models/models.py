from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from datetime import date

from parser_app.lab1_models.user_repo.user_models import User

class ExpenseType(str, Enum):
    goal = "goal"
    expense = "expense"
    debt = "debt"

class BaseCategory(SQLModel):
    id: int | None
    name: str
    type: ExpenseType
    limit_of_expenses: int | None

class ExpenseCategory(BaseCategory, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    type: ExpenseType
    limit_of_expenses: int | None
    user_id: int = Field(foreign_key="user.id")

    user: User | None = Relationship(back_populates="categories")
    expenses: list["Expense"] | None = Relationship(back_populates="category")


class CategoryWithExpense(BaseCategory):
    expenses: list["Expense"] = []


class SourceOfIncome(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    planning_to_receive: int | None
    user_id: int = Field(foreign_key="user.id")

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
    transaction_date: date = Field(default_factory=date.today)
    user_id: int = Field(default=None, foreign_key="user.id")
    account_id: int | None = Field(foreign_key="account.id")
    category_id: int | None = Field(foreign_key="expensecategory.id")

    user: User | None = Relationship(back_populates="expenses")
    account: Account | None = Relationship(back_populates="expenses")
    category: ExpenseCategory | None = Relationship(back_populates="expenses")


class Income(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    amount: int
    transaction_date: date = Field(default_factory=date.today)
    user_id: int = Field(foreign_key="user.id")
    source_id: int | None = Field(foreign_key="sourceofincome.id")
    account_id: int | None = Field(foreign_key="account.id")

    user: User | None = Relationship(back_populates="incomes")
    account: Account | None = Relationship(back_populates="incomes")
    source: SourceOfIncome | None = Relationship(back_populates="incomes")

