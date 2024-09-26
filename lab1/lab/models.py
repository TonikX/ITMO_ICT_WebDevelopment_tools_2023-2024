from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    password: Optional[str] = None
    hashed_password: str
    email: str
    goals: List["Goal"] = Relationship(back_populates="user")
    budgets: List["Budget"] = Relationship(back_populates="user")
    categories: List["Category"] = Relationship(back_populates="user")
    transactions: List["Transaction"] = Relationship(back_populates="user")

class Goal(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    goal_name: str
    target_amount: int
    current_amount: int
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="goals")

class Budget(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    budget_amount: int
    start_date: datetime
    end_date: datetime
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="budgets")
    categories: List["Category"] = Relationship(back_populates="budget")

class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    category_name: str
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="categories")
    budget_id: int = Field(foreign_key="budget.id", nullable=True)
    budget: Budget = Relationship(back_populates="categories")
    transactions: List["TransactionCategory"] = Relationship(back_populates="category")

class Transaction(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    transaction_amount: int
    transaction_date: datetime
    transaction_type: str
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="transactions")
    transaction_categories: List["TransactionCategory"] = Relationship(back_populates="transaction")
    notifications: List["Notification"] = Relationship(back_populates="transaction")

class Notification(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    notification_message: str
    notification_date: datetime
    transaction_id: int = Field(foreign_key="transaction.id")
    transaction: Transaction = Relationship(back_populates="notifications")

class TransactionCategory(SQLModel, table=True):
    category_id: int = Field(foreign_key="category.id", primary_key=True)
    transaction_id: int = Field(foreign_key="transaction.id", primary_key=True)
    note: Optional[str] = None
    need_declaration: str
    category: Category = Relationship(back_populates="transactions")
    transaction: Transaction = Relationship(back_populates="transaction_categories")
