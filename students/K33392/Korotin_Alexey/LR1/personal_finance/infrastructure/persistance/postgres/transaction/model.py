from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship

from personal_finance.domain.transaction.transaction import TransactionType, TransactionStatus
from personal_finance.infrastructure.persistance.postgres.account.model import UserAccountModel
from personal_finance.infrastructure.persistance.postgres.cashflow.model import ExpenseCategoryModel, IncomeSourceModel
from personal_finance.infrastructure.persistance.postgres.users.model import UserModel


class _TransactionModel(SQLModel):
    id: int = Field(primary_key=True)

    transaction_type: TransactionType
    status: TransactionStatus
    comment: str
    timestamp: datetime
    currency: str
    amount: int


class ExpenseTransactionModel(_TransactionModel, table=True):
    category_id: int = Field(foreign_key='expensecategorymodel.id')
    source_id: int = Field(foreign_key='useraccountmodel.id')
    user_id: int = Field(foreign_key="usermodel.id")
    user: "UserModel" = Relationship()
    category: ExpenseCategoryModel = Relationship(sa_relationship_kwargs={"cascade": "all"})
    source: UserAccountModel = Relationship(sa_relationship_kwargs={"cascade": "all"})


class TransferTransactionModel(_TransactionModel, table=True):
    source_id: int = Field(foreign_key='useraccountmodel.id')
    destination_id: int = Field(foreign_key='useraccountmodel.id')
    user_id: int = Field(foreign_key="usermodel.id")
    user: "UserModel" = Relationship()
    source: "UserAccountModel" = Relationship(sa_relationship_kwargs=dict(foreign_keys="[TransferTransactionModel.source_id]"))
    destination: "UserAccountModel" = Relationship(sa_relationship_kwargs=dict(foreign_keys="[TransferTransactionModel.destination_id]"))


class IncomeTransactionModel(_TransactionModel, table=True):
    source_id: int = Field(foreign_key='incomesourcemodel.id')
    destination_id: int = Field(foreign_key='useraccountmodel.id')
    user_id: int = Field(foreign_key="usermodel.id")
    user: "UserModel" = Relationship()
    source: IncomeSourceModel = Relationship(sa_relationship_kwargs={"cascade": "all"})
    destination: UserAccountModel = Relationship(sa_relationship_kwargs={"cascade": "all"})
