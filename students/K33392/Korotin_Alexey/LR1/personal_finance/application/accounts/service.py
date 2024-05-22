from typing import Collection, Optional

from personal_finance.application.accounts.dto import WriteAccountDto, ReadAccountDto
from personal_finance.application.exceptions import NotFoundException
from personal_finance.application.service import CrudService, ID, W, R
from personal_finance.domain.account.account import UserAccount
from personal_finance.infrastructure.persistance.postgres.account.repository import UserAccountRepository


class UserAccountService(CrudService[int, ReadAccountDto, WriteAccountDto]):
    __repository: UserAccountRepository

    def __init__(self, repository: UserAccountRepository):
        self.__repository = repository

    def find_by_id(self, identifier: ID) -> Optional[ReadAccountDto]:
        account: UserAccount = self.__repository.find_by_id(identifier)
        if account is None:
            raise NotFoundException("Account not found")

        return ReadAccountDto.from_entity(account)

    def find_all(self) -> Collection[R]:
        collection: Collection[UserAccount] = self.__repository.find_all()
        return list(map(ReadAccountDto.from_entity, collection))

    def save(self, obj: WriteAccountDto) -> R:
        account: UserAccount = obj.to_entity()
        account = self.__repository.save(account)
        return ReadAccountDto.from_entity(account)

    def update(self, id: ID, obj: W) -> R:
        if self.__repository.find_by_id(id) is None:
            raise NotFoundException("User not found")
        account: UserAccount = obj.to_entity()
        account.id = id
        account = self.__repository.save(account)
        return ReadAccountDto.from_entity(account)

    def delete_by_id(self, identifier: ID) -> None:
        if self.__repository.find_by_id(identifier) is None:
            raise NotFoundException("User not found")

        self.__repository.delete_by_id(identifier)
