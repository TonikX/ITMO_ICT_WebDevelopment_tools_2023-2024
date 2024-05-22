from typing import List

from pydantic import BaseModel

from personal_finance.application.users.dto import ReadUserDto
from personal_finance.domain.account.account import UserAccount, AccountBalance, AccountName
from personal_finance.presentation.http.accounts.dto import AccountTagReadDto, TagReadDto


class ReadAccountDto(BaseModel):
    id: int
    user: ReadUserDto
    name: str
    balance: int
    currency: str
    tags: List[AccountTagReadDto]

    @staticmethod
    def from_entity(e: UserAccount) -> "ReadAccountDto":
        return ReadAccountDto(
            id=e.id,
            user=ReadUserDto.from_entity(e.user),
            name=e.name.name,
            balance=e.balance.amount,
            currency=e.balance.currency,
            tags=list(map(lambda x: AccountTagReadDto(id=x.id, tag=TagReadDto(id=x.tag.id, name=x.tag.name), order=x.order), e.tags))
        )

    def to_entity(self) -> UserAccount:
        return UserAccount(
            id=self.id,
            user=self.user.to_entity(),
            name=AccountName(self.name),
            balance=AccountBalance(self.balance, self.currency)
        )


class WriteAccountDto(BaseModel):
    user: ReadUserDto
    name: str
    balance: int
    currency: str

    def to_entity(self) -> UserAccount:
        return UserAccount(
            id=None,
            user=self.user.to_entity(),
            name=AccountName(self.name),
            balance=AccountBalance(self.balance, self.currency)
        )