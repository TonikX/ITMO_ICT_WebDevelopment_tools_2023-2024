from enum import Enum

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

from models.user_models import User


class Category(str, Enum):
    FOOD = "Food"
    TRANSPORTATION = "Transportation"
    ENTERTAINMENT = "Entertainment"
    SHOPPING = "Shopping"
    BILLS = "Bills"
    SALARY = "Salary"
    SAVINGS = "Savings"
    OTHER = "Other"


class TransactionsType(str, Enum):
    INCOME = "income"
    EXPENSES = "expenses"


class TargetDeafult(SQLModel):
    category: Category = Category.OTHER
    value: int = 0
    balance_id: int = Field(foreign_key="balance.id")
class Target(TargetDeafult, table=True):
    id: int = Field(primary_key=True)
    balance: Optional["Balance"] = Relationship(back_populates="targets")

class Transactions(SQLModel, table=True):
    id: int = Field(primary_key=True)
    category: Category = Category.OTHER
    value: int = 0
    type: TransactionsType = TransactionsType.INCOME
    balance_id: int = Field(foreign_key="balance.id")
    balance: Optional["Balance"] = Relationship(back_populates="transactions")

class BalanceDeafult(SQLModel):
    balance: int = 0
    user_id: Optional[int] = Field(foreign_key="user.id")

class Balance(BalanceDeafult, table=True):
    id: int = Field(primary_key=True)
    user: Optional[User] = Relationship(back_populates="balance")
    transactions: List[Transactions] = Relationship(back_populates="balance")
    targets: List[Target] = Relationship(back_populates="balance")


class UserBalance(BalanceDeafult):
    transactions: List[Transactions] = None
    targets: List[Target] = None


class TargetResponse(TargetDeafult):
    balance: Optional[Balance] = None

class TargetCreate(SQLModel):
    category: Category
    value: int


class TargetUpdate(SQLModel):
    category: Category
    value: int


class TransactionsCreate(SQLModel):
    category: Category
    type: TransactionsType
    value: int


class TransactionsUpdate(SQLModel):
    category: Category
    type: TransactionsType
    value: int


