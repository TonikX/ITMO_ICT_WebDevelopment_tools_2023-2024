from typing import Collection, Optional

from personal_finance.application.exceptions import NotFoundException
from personal_finance.application.service import CrudService, ID, W, R
from personal_finance.application.transactions.dto import WriteTransferTransactionDto, ReadTransferTransactionDto
from personal_finance.domain.transaction.transaction import TransferTransaction
from personal_finance.infrastructure.persistance.postgres.transaction.repository import TransferTransactionRepository


class TransferTransactionService(CrudService[int, ReadTransferTransactionDto, WriteTransferTransactionDto]):

    __repository: TransferTransactionRepository

    def __init__(self, repository: TransferTransactionRepository):
        self.__repository = repository

    def find_by_id(self, identifier: ID) -> Optional[ReadTransferTransactionDto]:
        transaction: TransferTransaction | None = self.__repository.find_by_id(identifier)
        if transaction is None:
            raise NotFoundException("Category not found")

        return ReadTransferTransactionDto.from_source(transaction)

    def find_all(self) -> Collection[ReadTransferTransactionDto]:
        collection: Collection[TransferTransaction] = self.__repository.find_all()
        return list(map(ReadTransferTransactionDto.from_entity, collection))

    def save(self, obj: WriteTransferTransactionDto) -> ReadTransferTransactionDto:
        transaction: TransferTransaction = obj.to_entity()
        transaction = self.__repository.save(transaction)
        return ReadTransferTransactionDto.from_entity(transaction)

    def update(self, id: ID, obj: WriteTransferTransactionDto) -> ReadTransferTransactionDto:
        if self.__repository.find_by_id(id) is None:
            raise NotFoundException("Transaction not found")
        transaction: TransferTransaction = obj.to_entity()
        transaction.id = id
        transaction = self.__repository.save(transaction)
        return ReadTransferTransactionDto.from_entity(transaction)

    def delete_by_id(self, identifier: ID) -> None:
        if self.__repository.find_by_id(identifier) is None:
            raise NotFoundException("Transaction not found")

        self.__repository.delete_by_id(identifier)
