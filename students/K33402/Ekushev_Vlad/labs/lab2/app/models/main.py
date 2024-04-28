from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

from app.models.user import User


class CategoryType(str, Enum):
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


class CategoryTransactionLink(SQLModel, table=True):
    category_id: int = Field(foreign_key="category.id", primary_key=True)
    transaction_id: int = Field(foreign_key="transactions.id", primary_key=True)


class CategoryTargetLink(SQLModel, table=True):
    category_id: int = Field(foreign_key="category.id", primary_key=True)
    target_id: int = Field(foreign_key="target.id", primary_key=True)


class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    type: CategoryType = Field(sa_column_kwargs={"unique": True, "nullable": False})
    transactions: List["Transactions"] = Relationship(
        back_populates="categories", link_model=CategoryTransactionLink
    )
    targets: List["Target"] = Relationship(
        back_populates="categories", link_model=CategoryTargetLink
    )


class TargetDeafult(SQLModel):
    value: int = 0
    balance_id: int = Field(foreign_key="balance.id")


class Target(TargetDeafult, table=True):
    id: int = Field(default=None, primary_key=True)
    balance: Optional["Balance"] = Relationship(back_populates="targets")
    categories: List[Category] = Relationship(
        back_populates="targets", link_model=CategoryTargetLink
    )


class Transactions(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    value: int = 0
    type: TransactionsType = TransactionsType.INCOME
    balance_id: int = Field(foreign_key="balance.id")
    balance: Optional["Balance"] = Relationship(back_populates="transactions")
    categories: List[Category] = Relationship(
        back_populates="transactions", link_model=CategoryTransactionLink
    )


class BalanceDeafult(SQLModel):
    balance: int = 0
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Balance(BalanceDeafult, table=True):
    id: int = Field(default=None, primary_key=True)
    user: Optional[User] = Relationship(back_populates="balance")
    transactions: List[Transactions] = Relationship(back_populates="balance")
    targets: List[Target] = Relationship(back_populates="balance")


class UserBalance(BalanceDeafult):
    id: int
    transactions: List[Transactions] = []
    targets: List[Target] = []


class TargetResponse(TargetDeafult):
    balance: Optional[Balance] = None


class TargetCreate(SQLModel):
    category_id: int
    value: int


class TargetUpdate(SQLModel):
    category_id: int
    value: int


class TransactionsCreate(SQLModel):
    category_id: int
    type: TransactionsType
    value: int


class TransactionsUpdate(SQLModel):
    category_id: int
    type: TransactionsType
    value: int


class CategoryCreate(SQLModel):
    type: CategoryType


class CategoryUpdate(SQLModel):
    type: Optional[str] = None


class TransactionResponse(SQLModel):
    id: int
    value: int
    type: TransactionsType


class CategoriesTargetResponse(SQLModel):
    id: int
    value: int


class CategoryResponse(SQLModel):
    id: int
    type: CategoryType
    transactions: List[TransactionResponse] = []
    targets: List[CategoriesTargetResponse] = []
