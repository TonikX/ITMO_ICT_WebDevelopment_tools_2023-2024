from pydantic import BaseModel

from personal_finance.presentation.http.users.dto import UserReadDto


class CashFlowCreateDto(BaseModel):
    name: str
    currency: str
    expected: int


class CashFlowReadDto(BaseModel):
    id: int
    name: str
    currency: str
    expected: int
    user: UserReadDto
