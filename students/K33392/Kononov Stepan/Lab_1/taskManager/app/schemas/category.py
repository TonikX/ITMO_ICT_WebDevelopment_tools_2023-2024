from typing import List, Optional, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .task import Task


class CategoryBase(BaseModel):
    name: str
    description: Optional[str]


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    tasks: List['Task'] = []

    class Config:
        from_attributes = True
