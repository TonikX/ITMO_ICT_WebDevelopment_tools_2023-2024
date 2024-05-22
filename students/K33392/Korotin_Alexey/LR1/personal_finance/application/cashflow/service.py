from typing import Collection, Optional

from personal_finance.application.cashflow.dto import WriteCashFlowDto, ReadCashFlowDto
from personal_finance.application.exceptions import NotFoundException
from personal_finance.application.service import CrudService, ID, W, R
from personal_finance.domain.cashflow.cashflow import IncomeSource, ExpenseCategory
from personal_finance.infrastructure.persistance.postgres.cashflow.repository import IncomeSourceRepository, \
    ExpenseCategoryRepository


class IncomeSourceService(CrudService[int, ReadCashFlowDto, WriteCashFlowDto]):
    __repository: IncomeSourceRepository

    def __init__(self, repository: IncomeSourceRepository) -> None:
        self.__repository = repository

    def find_by_id(self, identifier: ID) -> Optional[ReadCashFlowDto]:
        source: IncomeSource | None = self.__repository.find_by_id(identifier)
        if source is None:
            raise NotFoundException("Category not found")

        return ReadCashFlowDto.from_source(source)

    def find_all(self) -> Collection[ReadCashFlowDto]:
        collection: Collection[IncomeSource] = self.__repository.find_all()
        return list(map(ReadCashFlowDto.from_source, collection))

    def save(self, obj: W) -> ReadCashFlowDto:
        source: IncomeSource = obj.to_source()
        source = self.__repository.save(source)
        return ReadCashFlowDto.from_source(source)

    def update(self, id: ID, obj: WriteCashFlowDto) -> R:
        if self.__repository.find_by_id(id) is None:
            raise NotFoundException("Income source not found")
        source: IncomeSource = obj.to_source()
        source.id = id
        source = self.__repository.save(source)
        return ReadCashFlowDto.from_source(source)

    def delete_by_id(self, identifier: ID) -> None:
        if self.__repository.find_by_id(identifier) is None:
            raise NotFoundException("Category not found")

        self.__repository.delete_by_id(identifier)


class ExpenseCategoryService(CrudService[int, ReadCashFlowDto, WriteCashFlowDto]):
    __repository: ExpenseCategoryRepository

    def __init__(self, repository: ExpenseCategoryRepository) -> None:
        self.__repository = repository

    def find_by_id(self, identifier: ID) -> Optional[ReadCashFlowDto]:
        category: ExpenseCategory | None = self.__repository.find_by_id(identifier)
        if category is None:
            raise NotFoundException("Category not found")

        return ReadCashFlowDto.from_category(category)

    def find_all(self) -> Collection[ReadCashFlowDto]:
        collection: Collection[ExpenseCategory] = self.__repository.find_all()
        return list(map(ReadCashFlowDto.from_category, collection))

    def save(self, obj: W) -> ReadCashFlowDto:
        category: ExpenseCategory = obj.to_category()
        category = self.__repository.save(category)
        return ReadCashFlowDto.from_category(category)

    def update(self, id: ID, obj: WriteCashFlowDto) -> R:
        if self.__repository.find_by_id(id) is None:
            raise NotFoundException("Category not found")
        category: ExpenseCategory = obj.to_category()
        category.id = id
        category = self.__repository.save(category)
        return ReadCashFlowDto.from_category(category)

    def delete_by_id(self, identifier: ID) -> None:
        if self.__repository.find_by_id(identifier) is None:
            raise NotFoundException("Category not found")

        self.__repository.delete_by_id(identifier)