from typing import List

from pydantic import BaseModel, Field

from personal_finance.domain.finance import Currency
from personal_finance.presentation.http.users.dto import UserReadDto


class TagCreateDto(BaseModel):
    name: str


class AccountTagCreateDto(BaseModel):
    tag_id: int
    account_id: int
    order: int


class TagReadDto(BaseModel):
    id: int
    name: str


class AccountTagReadDto(BaseModel):
    tag: TagReadDto
    order: int


class AccountCreateDto(BaseModel):
    name: str = Field(description="name")
    currency: Currency = Field(description="currency")
    balance: int = Field(description="balance")


class AccountReadDto(BaseModel):
    id: int = Field(description="id")
    name: str = Field(description="name")
    currency: Currency = Field(description="currency")
    balance: int = Field(description="balance")
    user: UserReadDto = Field(description="owner user")
    tags: List[AccountTagReadDto] = Field(description="tags")
