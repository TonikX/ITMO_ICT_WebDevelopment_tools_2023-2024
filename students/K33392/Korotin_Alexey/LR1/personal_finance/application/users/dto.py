from pydantic import BaseModel, Field

from personal_finance.domain.users.user import User, UserName, Login
from personal_finance.infrastructure.persistance.postgres.users.model import UserModel


class ReadUserDto(BaseModel):
    id: int = Field()
    first_name: str = Field()
    last_name: str = Field()
    login: str = Field()
    password_hash: str = Field()

    @classmethod
    def from_entity(cls, user: User) -> "ReadUserDto":
        return ReadUserDto(
            id=user.id,
            first_name=user.first_name.value,
            last_name=user.last_name.value,
            login=user.login.value,
            password_hash=user.password
        )

    def to_entity(self) -> User:
        return User(
            self.id,
            UserName(self.first_name),
            UserName(self.last_name),
            Login(self.login),
            self.password_hash
        )


class WriteUserDto(BaseModel):
    first_name: str = Field()
    last_name: str = Field()
    login: str = Field()
    password: str = Field()

    def to_entity(self) -> User:
        return User(
            None,
            first_name=UserName(self.first_name),
            last_name=UserName(self.last_name),
            login=Login(self.login),
            password=self.password
        )
