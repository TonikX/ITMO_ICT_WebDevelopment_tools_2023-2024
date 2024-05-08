from pydantic import BaseModel

from personal_finance.application.users.dto import ReadUserDto
from personal_finance.domain.cashflow.cashflow import IncomeSource, ExpenseCategory, CashflowName
from personal_finance.domain.finance import Money


class ReadCashFlowDto(BaseModel):
    id: int
    user: ReadUserDto
    name: str
    currency: str
    expected: int

    @staticmethod
    def from_source(source: IncomeSource) -> "ReadCashFlowDto":
        return ReadCashFlowDto(
            id=source.id,
            user=ReadUserDto.from_entity(source.user),
            name=source.name.name,
            currency=source.expected_periodic_amount.currency,
            expected=source.expected_periodic_amount.amount
        )

    @staticmethod
    def from_category(category: ExpenseCategory) -> "ReadCashFlowDto":
        return ReadCashFlowDto(
            id=category.id,
            user=ReadUserDto.from_entity(category.user),
            name=category.name.name,
            currency=category.expected_periodic_amount.currency,
            expected=category.expected_periodic_amount.amount
        )


class WriteCashFlowDto(BaseModel):
    name: str
    user: ReadUserDto
    currency: str
    expected: int

    def to_source(self) -> IncomeSource:
        return IncomeSource(
            id=None,
            name=CashflowName(self.name),
            user=self.user.to_entity(),
            amount=Money(self.expected, self.currency)
        )

    def to_category(self) -> ExpenseCategory:
        return ExpenseCategory(
            id=None,
            name=CashflowName(self.name),
            user=self.user.to_entity(),
            amount=Money(self.expected, self.currency)
        )