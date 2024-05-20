from abc import abstractmethod, ABCMeta
from typing import TypeVar, Generic, Collection, Optional

from pydantic import BaseModel

R = TypeVar('R', bound=BaseModel)
W = TypeVar('W', bound=BaseModel)
ID = TypeVar('ID')


class CrudService(Generic[ID, R, W], metaclass=ABCMeta):

    @abstractmethod
    def find_by_id(self, identifier: ID) -> Optional[R]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> Collection[R]:
        raise NotImplementedError

    @abstractmethod
    def save(self, obj: W) -> R:
        raise NotImplementedError

    @abstractmethod
    def update(self, id: ID, obj: W) -> R:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, identifier: ID) -> None:
        raise NotImplementedError

    def __getitem__(self, index: ID) -> Optional[R]:
        return self.find_by_id(index)
