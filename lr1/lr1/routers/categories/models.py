from typing import TypedDict

from pydantic import BaseModel

from models import Budget, Transaction


class DeletedCategoryResponse(TypedDict):
    message: str


class CategoryRead(BaseModel):
    category_id: int
    category_name: str
    transactions: list[Transaction]
    budgets: list[Budget]
