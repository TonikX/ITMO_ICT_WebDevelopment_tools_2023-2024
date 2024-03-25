import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"
    user_id: int = Field(primary_key=True)
    username: str
    email: str
    password_hash: str


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"
    transaction_id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    amount: float
    transaction_type: str
    category_id: int = Field(foreign_key="categories.category_id")
    timestamp: datetime.datetime

    user: User = Relationship()
    category: "Category" = Relationship(back_populates="transactions")


class BudgetCategoryLink(SQLModel, table=True):
    __tablename__ = "budgets_categories"

    budget_id: int = Field(primary_key=True, foreign_key="budgets.budget_id")
    category_id: int = Field(primary_key=True, foreign_key="categories.category_id")


class Budget(SQLModel, table=True):
    __tablename__ = "budgets"
    budget_id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    amount: float
    period_start: datetime.datetime
    period_end: datetime.datetime


class Category(SQLModel, table=True):
    __tablename__ = "categories"
    category_id: int = Field(primary_key=True)
    category_name: str
    transactions: List[Transaction] = Relationship(back_populates="category")
    budgets: Optional[list[Budget]] = Relationship(link_model=BudgetCategoryLink)


class BudgetExceedNotification(SQLModel, table=True):
    __tablename__ = "budgetexceednotification"
    notification_id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    budget_id: int = Field(foreign_key="budgets.budget_id")
    threshold_amount: float
    timestamp: datetime.datetime


class SpendingAnalysis(SQLModel, table=True):
    __tablename__ = "spendinganalysis"
    analysis_id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    category_id: int = Field(foreign_key="categories.category_id")
    total_spent: float
    timestamp: datetime.datetime


class FinancialGoal(SQLModel, table=True):
    __tablename__ = "financialgoals"
    goal_id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    goal_name: str
    target_amount: float
    current_amount: float
    target_date: datetime.datetime
