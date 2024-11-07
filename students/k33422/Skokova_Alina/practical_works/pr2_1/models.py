from enum import Enum
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

class ConditionType(Enum):
    excellent = "отличное"
    good = "хорошее"
    used = "удовлетворительное"

class Library(BaseModel):
    library_id: int
    user_id: int
    library_name: str

class RequestStatusType(Enum):
    waiting = "ожидание"
    approved = "одобрено"
    rejected = "отклонено"

class Request(BaseModel):
    request_id: int
    user_id: int
    request_date: datetime
    request_status: RequestStatusType

class Book(BaseModel):
    book_id: int
    book_name: str
    book_author: str
    book_condition: ConditionType
    library: Library
    requests: Optional[List[Request]] = []