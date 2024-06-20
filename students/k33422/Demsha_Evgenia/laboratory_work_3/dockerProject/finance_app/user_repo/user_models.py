from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator, EmailStr
from typing import ForwardRef

Expense = ForwardRef("Expense")
Income = ForwardRef("Income")
Account = ForwardRef("Account")
ExpenseCategory = ForwardRef("ExpenseCategory")
SourceOfIncome = ForwardRef("SourceOfIncome")


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: str
    password: str
    is_admin: bool = False

    expenses: list[Expense] | None = Relationship(back_populates="user")
    incomes: list[Income] | None = Relationship(back_populates="user")
    accounts: list[Account] | None = Relationship(back_populates="user")
    categories: list[ExpenseCategory] | None = Relationship(back_populates="user")
    sources: list[SourceOfIncome] | None = Relationship(back_populates="user")


class UserInput(SQLModel):
    username: str
    password: str = Field(max_length=256, min_length=6)
    password2: str
    email: EmailStr

    @field_validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values.data and v != values.data['password']:
            raise ValueError('passwords don\'t match')
        return v


class UserLogin(SQLModel):
    username: str
    password: str


class UserPasswordChange(SQLModel):
    old_password: str
    new_password: str = Field(max_length=256, min_length=6)
    new_password2: str

    @field_validator('new_password2')
    def password_match(cls, v, values, **kwargs):
        if 'new_password' in values.data and v != values.data['new_password']:
            raise ValueError('passwords don\'t match')
        return v
