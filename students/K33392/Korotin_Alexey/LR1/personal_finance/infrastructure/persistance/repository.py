from abc import abstractmethod, ABCMeta
from typing import TypeVar, Generic, Collection, Optional

from sqlmodel import SQLModel

from personal_finance.domain.base import Entity

T = TypeVar('T', bound=SQLModel)
ID = TypeVar('ID', bound=Entity)


class Repository(Generic[ID, T], metaclass=ABCMeta):

    @abstractmethod
    def find_by_id(self, identifier: ID) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> Collection[T]:
        raise NotImplementedError

    @abstractmethod
    def save(self, obj: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, identifier: ID) -> None:
        raise NotImplementedError

    def __getitem__(self, index: ID) -> Optional[T]:
        return self.find_by_id(index)
