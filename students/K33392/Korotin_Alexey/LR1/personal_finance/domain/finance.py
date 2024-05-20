from enum import Enum
from typing import List, Any

from personal_finance.domain.base import ValueObject


class Currency(Enum):
    RUB = "RUB",
    USD = "USD",
    EUR = "EUR"


class Money(ValueObject):
    __amount: int
    __currency: Currency

    def __init__(self, amount: int, currency: Currency) -> None:
        self.__amount = amount
        self.__currency = currency

    @property
    def _equality_attributes(self) -> List[Any]:
        return [self.__amount, self.__currency]

    @property
    def amount(self) -> int:
        return self.__amount

    @property
    def currency(self) -> Currency:
        return self.__currency
