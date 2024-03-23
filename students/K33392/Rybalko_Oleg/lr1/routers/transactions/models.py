from datetime import datetime
from typing import TypedDict

from pydantic import BaseModel

from routers.users.models import UserRead


class DeletedTransactionResponse(TypedDict):
    message: str


class TransactionRead(BaseModel):
    transaction_id: int
    user_id: int
    amount: float
    transaction_type: str
    category_id: int
    timestamp: datetime
    user: UserRead
