from typing import Optional
from sqlmodel import SQLModel, Field


class CategoryOperationLink(SQLModel, table=True):  # многие-ко-многим, связь категорий и операций
    id: Optional[int] = Field(default=None, primary_key=True, unique=True)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", primary_key=True)  # внешний ключ
    operation_id: Optional[int] = Field(default=None, foreign_key="operation.id", primary_key=True)  # внешний ключ
    amount: Optional[float] = Field(default=None)
    # тут составной первичный ключ по 3 полям

