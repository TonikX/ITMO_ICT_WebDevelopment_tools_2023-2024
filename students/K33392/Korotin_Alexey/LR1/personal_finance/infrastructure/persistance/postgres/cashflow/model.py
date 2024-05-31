from sqlmodel import SQLModel, Field, Relationship

from personal_finance.infrastructure.persistance.postgres.users.model import UserModel


class IncomeSourceModel(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    user_id: int = Field(foreign_key="usermodel.id")
    user: UserModel = Relationship()
    amount: int
    currency: str


class ExpenseCategoryModel(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    user_id: int = Field(foreign_key="usermodel.id")
    user: UserModel = Relationship()
    amount: int
    currency: str
