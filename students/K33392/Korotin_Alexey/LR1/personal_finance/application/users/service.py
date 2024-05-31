from typing import Collection, Optional

from .dto import ReadUserDto, WriteUserDto
from ..auth.crypt import get_password_hash
from ..exceptions import NotFoundException, ConflictException
from ..service import CrudService, ID
from ...domain.users.user import User
from ...infrastructure.persistance.postgres.users.repository import UserRepository


class UserService(CrudService[int, ReadUserDto, WriteUserDto]):
    __repository: UserRepository

    def __init__(self, repository: UserRepository) -> None:
        self.__repository = repository

    def find_by_id(self, identifier: ID) -> Optional[ReadUserDto]:
        user: User | None = self.__repository.find_by_id(identifier)
        if user is None:
            raise NotFoundException("User not found")

        return ReadUserDto.from_entity(user)

    def find_all(self) -> Collection[ReadUserDto]:
        collection: Collection[User] = self.__repository.find_all()
        return list(map(ReadUserDto.from_entity, collection))

    def save(self, obj: WriteUserDto) -> ReadUserDto:
        user: User = obj.to_entity()
        user.password = get_password_hash(user.password)
        if self.__repository.find_by_login(user.login.value) is not None:
            raise ConflictException("Login already exists")

        user = self.__repository.save(user)
        return ReadUserDto.from_entity(user)

    def update(self, id: ID, obj: WriteUserDto) -> ReadUserDto:
        if self.__repository.find_by_id(id) is None:
            raise NotFoundException("User not found")
        user: User = obj.to_entity()
        user.id = id
        user.password = get_password_hash(user.password)
        existing_user: User = self.__repository.find_by_login(user.login.value)
        if existing_user is None:
            user = self.__repository.save(user)
            return ReadUserDto.from_entity(user)

        if existing_user != user:
            raise ConflictException("Login already exists")

        user = self.__repository.save(user)
        return ReadUserDto.from_entity(user)

    def delete_by_id(self, identifier: ID) -> None:
        if self.__repository.find_by_id(identifier) is None:
            raise NotFoundException("User not found")

        self.__repository.delete_by_id(identifier)

    def find_by_login(self, login: str) -> ReadUserDto:
        user = self.__repository.find_by_login(login)
        if user is None:
            raise NotFoundException("")

        return ReadUserDto.from_entity(user)

