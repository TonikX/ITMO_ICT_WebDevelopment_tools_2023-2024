from typing import List

from sqlmodel import SQLModel, Field, Relationship

from personal_finance.domain.finance import Currency
from personal_finance.infrastructure.persistance.postgres.users.model import UserModel


class TagModel(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str


class AccountTagModel(SQLModel, table=True):
    id: int = Field(primary_key=True)
    tag_id: int = Field(foreign_key="tagmodel.id")
    tag: TagModel = Relationship()
    account_id: int = Field(foreign_key="useraccountmodel.id")
    account: "UserAccountModel" = Relationship(back_populates="tags")
    order: int


class UserAccountModel(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=50)
    currency: str
    amount: int
    user_id: int = Field(foreign_key="usermodel.id")
    user: UserModel = Relationship(sa_relationship_kwargs={"cascade": "all"})
    tags: List[AccountTagModel] = Relationship(back_populates="account")

