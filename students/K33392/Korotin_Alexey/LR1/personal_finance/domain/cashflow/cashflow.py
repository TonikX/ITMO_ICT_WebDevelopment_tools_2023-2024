from typing import List, Any

from personal_finance.domain.base import Entity, ValueObject
from personal_finance.domain.cashflow.exceptions import InvalidCashFlowException
from personal_finance.domain.finance import Money
from personal_finance.domain.users.user import User


class CashflowName(ValueObject):
    __name: str

    def __init__(self, name: str) -> None:
        if len(name) < 2 or len(name) > 50:
            raise InvalidCashFlowException("Cashflow name must be between 2 and 50 characters long")
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    @property
    def _equality_attributes(self) -> List[Any]:
        return [self.__name]


class IncomeSource(Entity):
    name: CashflowName
    user: User
    expected_periodic_amount: Money

    def __init__(self, id: int, name: CashflowName, user: User, amount: Money) -> None:
        super().__init__(id)
        self.name = name
        self.user = user
        self.expected_periodic_amount = amount


class ExpenseCategory(Entity):
    name: CashflowName
    user: User
    expected_periodic_amount: Money

    def __init__(self, id: int, name: CashflowName, user: User, amount: Money) -> None:
        super().__init__(id)
        self.name = name
        self.user = user
        self.expected_periodic_amount = amount
