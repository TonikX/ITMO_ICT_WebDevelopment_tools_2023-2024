from enum import Enum
from typing import List, Any
from datetime import datetime

from personal_finance.domain.account.account import UserAccount
from personal_finance.domain.base import Entity, ValueObject, AggregateRoot
from abc import ABCMeta, abstractmethod

from personal_finance.domain.cashflow.cashflow import IncomeSource, ExpenseCategory
from personal_finance.domain.finance import Money
from personal_finance.domain.transaction.exception import TransactionCommentException, TransactionExecutionException
from personal_finance.domain.users.user import User


class TransactionType(Enum):
    EXPENSE = "EXPENSE",
    INCOME = "INCOME",
    TRANSFER = "TRANSFER"


class TransactionStatus(Enum):
    DRAFT = "DRAFT",
    EXECUTED = "EXECUTED",
    CANCELLED = "CANCELLED"


class TransactionComment(ValueObject):
    __value: str

    def __init__(self, value: str) -> None:
        if len(value) > 255:
            raise TransactionCommentException("Comment should not exceed 255 characters")
        self.__value = value

    @property
    def value(self) -> str:
        return self.__value

    @property
    def _equality_attributes(self) -> List[Any]:
        return [self.value]


class Transaction(AggregateRoot, metaclass=ABCMeta):
    transaction_type: TransactionType
    status: TransactionStatus
    comment: TransactionComment
    user: User
    timestamp: datetime
    money: Money

    def __init__(self, id: int, transaction_type: TransactionType, status: TransactionStatus,
                 comment: TransactionComment, user: User, money: Money) -> None:
        super().__init__(id)
        self.transaction_type = transaction_type
        self.status = status
        self.comment = comment
        self.user = user
        self.money = money

    @abstractmethod
    def execute(self, at: datetime) -> None:
        raise NotImplementedError

    @abstractmethod
    def revert(self) -> None:
        raise NotImplementedError


class TransferTransaction(Transaction):
    source: UserAccount
    destination: UserAccount
    timestamp: datetime

    def __init__(self, id: int, status: TransactionStatus, comment: TransactionComment, user: User, money: Money,
                 source: UserAccount, destination: UserAccount) -> None:
        super().__init__(id, TransactionType.TRANSFER, status, comment, user, money)
        self.source = source
        self.destination = destination

    def execute(self, at: datetime) -> None:
        if self.status != TransactionStatus.DRAFT:
            raise TransactionExecutionException("Transaction could not be executed")
        self.source.withdraw(self.money)
        self.destination.refill(self.money)
        self.timestamp = at
        self.status = TransactionStatus.EXECUTED

    def revert(self) -> None:
        if self.status != TransactionStatus.EXECUTED:
            raise TransactionExecutionException("Transaction could not be reverted")
        self.destination.withdraw(self.money)
        self.source.refill(self.money)


class IncomeTransaction(Transaction):
    source: IncomeSource
    destination: UserAccount

    def __init__(self, id: int, status: TransactionStatus, comment: TransactionComment, user: User, money: Money,
                 source: IncomeSource, destination: UserAccount) -> None:
        super().__init__(id, TransactionType.INCOME, status, comment, user, money)
        self.source = source
        self.destination = destination

    def execute(self, at: datetime) -> None:
        if self.status != TransactionStatus.DRAFT:
            raise TransactionExecutionException("Transaction could not be executed")

        self.destination.refill(self.money)
        self.status = TransactionStatus.EXECUTED
        self.timestamp = at

    def revert(self) -> None:
        if self.status != TransactionStatus.EXECUTED:
            raise TransactionExecutionException("Transaction could not be reverted")

        self.destination.withdraw(self.money)


class ExpenseTransaction(Transaction):
    source: UserAccount
    category: ExpenseCategory

    def __init__(self, id: int, status: TransactionStatus, comment: TransactionComment, user: User, money: Money,
                 source: UserAccount, category: ExpenseCategory) -> None:
        super().__init__(id, TransactionType.EXPENSE, status, comment, user, money)
        self.source = source
        self.destination = category

    def execute(self, at: datetime) -> None:
        if self.status != TransactionStatus.DRAFT:
            raise TransactionExecutionException("Transaction could not be executed")

        self.source.withdraw(self.money)
        self.status = TransactionStatus.EXECUTED
        self.timestamp = at

    def revert(self) -> None:
        if self.status != TransactionStatus.EXECUTED:
            raise TransactionExecutionException("Transaction could not be reverted")

        self.source.refill(self.money)
