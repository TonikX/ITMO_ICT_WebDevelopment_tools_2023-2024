from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from models.categories import Category
from models.links import CategoryOperationLink


class Operation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    operation: str = Field(unique=True)
    limit: float = Field(default=0.0)
    alias: Optional[str] = Field(default=None, nullable=True)
    categories: Optional[List[Category]] = Relationship(back_populates="operations",
                                                        link_model=CategoryOperationLink)  # многие-ко-многим
