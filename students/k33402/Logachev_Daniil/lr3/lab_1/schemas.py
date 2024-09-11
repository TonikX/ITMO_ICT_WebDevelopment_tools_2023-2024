from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
import datetime

class Parce(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str
    article_title: str

# Salary
class SalaryDB(SQLModel):
    value: float
    #legal: bool
    salary_period_for_user_id: Optional[int] = Field(default=None, foreign_key="salaryperiodforuser.id")


class SalaryDisplay(SalaryDB):
    salary_period_for_user: Optional["SalaryPeriodForUser"] = None


class Salary(SalaryDB, table=True):
    id: int = Field(default=None, primary_key=True)
    date: datetime.datetime
    salary_period_for_user:  Optional["SalaryPeriodForUser"] = Relationship(back_populates="salarys")


#Period for user

class SalaryPeriodForUserDB(SQLModel):
    salary_period_id: Optional[int] = Field(default=None, foreign_key="salaryperiod.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class SalaryPeriodForUserDisplay(SalaryPeriodForUserDB):
    salary_period: Optional["SalaryPeriod"] = None
    salarys: Optional[List["Salary"]] = None
    user: Optional["User"] = None


class SalaryPeriodForUser(SalaryPeriodForUserDB, table=True):
    id: int = Field(default=None, primary_key=True)
    salary_period: Optional["SalaryPeriod"] = Relationship(back_populates="salary_period_for_users")

    salarys: Optional[List["Salary"]] = Relationship(back_populates="salary_period_for_user",
                                                   sa_relationship_kwargs={
                                                       "cascade": "all, delete",
                                                   }
                                                   )
    user:  Optional["User"] = Relationship(back_populates="salary_periods_for_user")


# WastePeriod

class SalaryPeriodDB(SQLModel):
    date_start: datetime.date
    date_end: datetime.date


class SalaryPeriodDisplay(SalaryPeriodDB):
    salary_period_for_users: Optional[List["SalaryPeriodForUser"]] = None


class SalaryPeriod(SalaryPeriodDB, table=True):
    id: int = Field(default=None, primary_key=True)
    salary_period_for_users: Optional[List["SalaryPeriodForUser"]] = Relationship(back_populates="salary_period")



# Waste

class Type(Enum):
    clothes = "clothes"
    meals = "meals"
    hobby = 'hobby'
    travel = 'travel'


class WasteDB(SQLModel):
    value: float
    type: Type
    waste_period_for_user_id: Optional[int] = Field(default=None, foreign_key="wasteperiodforuser.id")


class WasteDisplay(WasteDB):
    waste_period_for_user: Optional["WastePeriodForUser"] = None


class Waste(WasteDB, table=True):
    id: int = Field(default=None, primary_key=True)
    date: datetime.datetime
    waste_period_for_user:  Optional["WastePeriodForUser"] = Relationship(back_populates="wastes")


#Period for user

class WastePeriodForUserDB(SQLModel):
    limit: float
    waste_period_id: Optional[int] = Field(default=None, foreign_key="wasteperiod.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class WastePeriodForUserDisplay(WastePeriodForUserDB):
    waste_period: Optional["WastePeriod"] = None
    wastes: Optional[List["Waste"]] = None
    user: Optional["User"] = None


class WastePeriodForUser(WastePeriodForUserDB, table=True):
    id: int = Field(default=None, primary_key=True)
    waste_period: Optional["WastePeriod"] = Relationship(back_populates="waste_period_for_users")

    wastes: Optional[List["Waste"]] = Relationship(back_populates="waste_period_for_user",
                                                   sa_relationship_kwargs={
                                                       "cascade": "all, delete",
                                                   }
                                                   )
    user:  Optional["User"] = Relationship(back_populates="waste_periods_for_user")


# WastePeriod

class WastePeriodDB(SQLModel):
    date_start: datetime.date
    date_end: datetime.date


class WastePeriodDisplay(WastePeriodDB):
    waste_period_for_users: Optional[List["WastePeriodForUser"]] = None


class WastePeriod(WastePeriodDB, table=True):
    id: int = Field(default=None, primary_key=True)
    waste_period_for_users: Optional[List["WastePeriodForUser"]] = Relationship(back_populates="waste_period")


# User

class UserBase(SQLModel):
    username: str
    password: str


class UserDisplay(UserBase):
    salary_periods_for_user: Optional[List["SalaryPeriodForUser"]] = None
    waste_periods_for_user: Optional[List["WastePeriodForUser"]] = None


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    salary_periods_for_user: Optional[List["SalaryPeriodForUser"]] = Relationship(back_populates="user",
                                                   sa_relationship_kwargs={
                                                       "cascade": "all, delete",
                                                   }
                                                   )
    waste_periods_for_user: Optional[List["WastePeriodForUser"]] = Relationship(back_populates="user",
                                                   sa_relationship_kwargs={
                                                       "cascade": "all, delete",
                                                   }
                                                   )


class ChangePassword(SQLModel):
    old_password: str
    new_password: str
