from typing import Optional

#from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

from app.model import Book, Exchange


#Profile

class ProfileDefault(SQLModel):
    full_name: str = Field(default="")
    city: str = Field(default="")
    about: str = Field(default="")
    account_id: int = Field(foreign_key="account.id", ondelete="CASCADE")


class ProfileUpdate(SQLModel):
    full_name: str|None = None
    city: str|None = None
    about: str|None = None


class Profile(ProfileDefault, table=True):
    id: int = Field(default=None, primary_key=True)

    account: "Account" = Relationship(
        back_populates="profile",
    )

#Account

class AccountDefault(SQLModel):
    login: str = Field(unique=True)
    password: str
    email: str = Field(unique=True)


class AccountUpdate(AccountDefault):
    login: str|None = None
    password: str|None = None
    email: str|None = None


class ResponseAccountProfile(AccountDefault):
    profile: Optional["Profile"] = None


class TokenedAccount(SQLModel):
    token: str
    account: "Account"


class Account(AccountDefault, table=True):
    id: int = Field(default=None, primary_key=True)

    profile: Optional["Profile"] = Relationship(back_populates="account",  sa_relationship_kwargs={"cascade": "all, delete"})

    books: Optional[list["Book"]] = Relationship(back_populates="owner")
    sent_exchanges: Optional[list["Exchange"]] = Relationship(
        back_populates="sender",
        sa_relationship_kwargs={"foreign_keys": "Exchange.sender_id", "cascade": "all, delete"}
    )
    received_exchanges: Optional[list["Exchange"]] = Relationship(
        back_populates="receiver",
        sa_relationship_kwargs={"foreign_keys": "Exchange.receiver_id", "cascade": "all, delete"}
    )
