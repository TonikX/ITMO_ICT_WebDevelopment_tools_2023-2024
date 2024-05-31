from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class CategoryOperationLink(SQLModel, table=True):  # многие-ко-многим, связь категорий и операций
    id: Optional[int] = Field(default=None, primary_key=True, unique=True)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", primary_key=True)  # внешний ключ
    category: Optional[List["Category"]] = Relationship(back_populates="categories")  # внешний ключ
    operation_id: Optional[int] = Field(default=None, foreign_key="operation.id", primary_key=True)  # внешний ключ
    operation: Optional[List["Operation"]] = Relationship(back_populates="operations")  # внешний ключ
    amount: Optional[float] = Field(default=None)
    # тут составной первичный ключ по 3 полям

