from pydantic import BaseModel, Field

from personal_finance.application.users.dto import ReadUserDto


class UserReadDto(BaseModel):
    id: int = Field(example="1")
    first_name: str = Field(example="Vasya")
    last_name: str = Field(example="Ivanov")
    login: str = Field(example="vasyaivanov228")

    @staticmethod
    def from_app_dto(dto: ReadUserDto) -> "UserReadDto":
        return UserReadDto(
            **dto.model_dump()
        )


class UserCreateDto(BaseModel):
    first_name: str = Field(example="Vasya")
    last_name: str = Field(example="Ivanov")
    login: str = Field(example="vasyaivanov228")
    password: str = Field(example="<PASSWORD>")


class UserUpdateDto(BaseModel):
    first_name: str = Field(example="Vasya")
    last_name: str = Field(example="Ivanov")
    login: str = Field(example="vasyaivanov228")
    password: str = Field(example="<PASSWORD>")


class LoginDto(BaseModel):
    login: str = Field(example="vasyaivanov228")
    password: str = Field(example="<PASSWORD>")


class JwtDto(BaseModel):
    token: str = Field(example="<JWT TOKEN>")
