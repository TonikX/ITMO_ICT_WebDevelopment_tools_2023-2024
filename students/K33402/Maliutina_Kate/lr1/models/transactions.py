from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(default=None, nullable=False)  # тип данных дата и время
    amount: float = Field(default=None, nullable=False)
    customer_id: Optional[int] = Field(default=None, foreign_key="customer.id")  # один-ко-многим
    category_operation_link_id: Optional[int] = Field(default=None, foreign_key="categoryoperationlink.id")  # один-ко-многим
