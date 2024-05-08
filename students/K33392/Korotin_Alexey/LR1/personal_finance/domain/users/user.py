from typing import List, Any

from .exceptions import InvalidUsernameException, InvalidUserLoginException
from ..base import Entity, ValueObject


class UserName(ValueObject):
    __value: str

    @property
    def value(self) -> str:
        return self.__value

    def __init__(self, value: str) -> None:
        if len(value) < 5 or len(value) > 30:
            raise InvalidUsernameException
        self.__value = value

    @property
    def _equality_attributes(self) -> List[Any]:
        return [self.value]


class Login(ValueObject):
    __value: str

    @property
    def value(self) -> str:
        return self.__value

    def __init__(self, value: str) -> None:
        if len(value) < 5 or len(value) > 30:
            raise InvalidUserLoginException
        self.__value = value

    @property
    def _equality_attributes(self) -> List[Any]:
        return [self.value]


class User(Entity):
    first_name: UserName
    last_name: UserName
    login: Login
    password: str

    def __init__(self, id: int, first_name: UserName, last_name: UserName, login: Login, password: str) -> None:
        super().__init__(id)
        self.first_name = first_name
        self.last_name = last_name
        self.login = login
        self.password = password

