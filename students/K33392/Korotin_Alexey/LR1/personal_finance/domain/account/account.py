from typing import List, Any

from personal_finance.domain.account.exceptions import InvalidAccountException
from personal_finance.domain.base import ValueObject, Entity
from personal_finance.domain.finance import Currency, Money
from personal_finance.domain.users.user import User


class AccountBalance(ValueObject):
    __amount: int
    __currency: Currency

    def __init__(self, amount: int, currency: Currency):
        self.__amount = amount
        self.__currency = currency

    @property
    def amount(self) -> int:
        return self.__amount

    @property
    def currency(self) -> Currency:
        return self.__currency

    def refill(self, money: Money) -> "AccountBalance":
        return AccountBalance(self.__amount + money.amount, self.__currency)

    def withdraw(self, money: Money) -> "AccountBalance":
        return AccountBalance(self.__amount - money.amount, self.__currency)

    @property
    def _equality_attributes(self) -> List[Any]:
        return [self.amount, self.currency]


class AccountName(ValueObject):
    __name: str

    def __init__(self, name: str) -> None:
        if len(name) < 2 or len(name) > 50:
            raise InvalidAccountException("Account name must be between 2 and 50 characters")
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    @property
    def _equality_attributes(self) -> List[Any]:
        return [self.__name]


class Tag(Entity):
    name: str

    def __init__(self, id: int, name: str) -> None:
        super().__init__(id)
        self.name = name


class AccountTag(Entity):
    tag: Tag
    order: int

    def __init__(self, id: int, tag: Tag, order: int) -> None:
        super().__init__(id)
        self.tag = tag
        self.order = order


class UserAccount(Entity):
    name: AccountName
    balance: AccountBalance
    user: User
    tags: List[AccountTag]

    def __init__(self, id: int, name: AccountName, balance: AccountBalance, user: User, tags=None) -> None:
        super().__init__(id)
        self.tags = [] if tags is None else tags
        self.name = name
        self.balance = balance
        self.user = user

    def withdraw(self, money: Money) -> None:
        self.balance = self.balance.withdraw(money)

    def refill(self, money: Money) -> None:
        self.balance = self.balance.refill(money)

