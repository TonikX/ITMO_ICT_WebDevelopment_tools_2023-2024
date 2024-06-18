import datetime
from pydantic import BaseModel
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
import datetime


class Source(Enum):
    job = 'job'
    freelance = 'freelance'
    scholarship = 'scholarship'
    other = 'other'


class IncomeDefault(SQLModel):
    value: float
    source: Source
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Income(IncomeDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    user:  Optional["User"] = Relationship(back_populates="incomes")



class WasteDefault(SQLModel):
    value: float
    poc_id: Optional[int] = Field(default=None, foreign_key="periodofcategory.id")


class WasteShow(WasteDefault):
    poc: Optional["PeriodOfCategory"] = None


class Waste(WasteDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    date: datetime.datetime
    poc:  Optional["PeriodOfCategory"] = Relationship(back_populates="wastes")


class PeriodOfCategoryDefault(SQLModel):
    limit: float
    period_id: Optional[int] = Field(default=None, foreign_key="period.id")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class PeriodOfCategoryShow(PeriodOfCategoryDefault):
    periods: Optional["Period"] = None
    categorys: Optional["Category"] = None
    user: Optional["User"] = None


class PeriodOfCategory(PeriodOfCategoryDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    periods: Optional["Period"] = Relationship(back_populates="pocs")
    categorys: Optional["Category"] = Relationship(back_populates="pocs")

    wastes: Optional[List["Waste"]] = Relationship(back_populates="poc",
                                                   sa_relationship_kwargs={
                                                       "cascade": "all, delete",
                                                   }
                                                   )
    user:  Optional["User"] = Relationship(back_populates="pocs")


class CategoryDefault(SQLModel):
    name: str


class CategoryShow(CategoryDefault):
    periods: Optional[List["Period"]] = None
    pocs: Optional[List["PeriodOfCategory"]] = None


class Category(CategoryDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    periods: Optional[List["Period"]] = Relationship(
        back_populates="categorys", link_model=PeriodOfCategory
    )
    pocs: Optional[List["PeriodOfCategory"]] = Relationship(back_populates="categorys")


class PeriodDefault(SQLModel):
    date_start: datetime.date
    date_end: datetime.date


class PeriodShow(PeriodDefault):
    categorys: Optional[List["Category"]] = None
    pocs: Optional[List["PeriodOfCategory"]] = None


class Period(PeriodDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    categorys: Optional[List["Category"]] = Relationship(
        back_populates="periods", link_model=PeriodOfCategory
    )
    pocs: Optional[List["PeriodOfCategory"]] = Relationship(back_populates="periods")


class UserBase(SQLModel):
    username: str
    password: str


class UserShow(UserBase):
    incomes: Optional[List["Income"]] = None
    pocs: Optional[List["PeriodOfCategory"]] = None


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    incomes: Optional[List["Income"]] = Relationship(back_populates="user",
                                                   sa_relationship_kwargs={
                                                       "cascade": "all, delete",
                                                   }
                                                   )
    pocs: Optional[List["PeriodOfCategory"]] = Relationship(back_populates="user",
                                                   sa_relationship_kwargs={
                                                       "cascade": "all, delete",
                                                   }
                                                   )


class ChangePassword(SQLModel):
    old_password: str
    new_password: str
