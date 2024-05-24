from datetime import date
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLEnum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

__all__ = ['Gender', 'Profile']

if TYPE_CHECKING:
    from .user import User
    from .trip import Trip
    from .participant import Participant


class Gender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'


class Profile(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), unique=True
    )
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    middle_name: Mapped[str] = mapped_column(String(32))
    birth_date: Mapped[date] = mapped_column()
    gender: Mapped[Gender] = mapped_column(SQLEnum(Gender))
    bio: Mapped[str] = mapped_column(Text, default='', server_default='')
    country: Mapped[str] = mapped_column(String(64))
    city: Mapped[str | None] = mapped_column(String(64), nullable=True)
    language: Mapped[str] = mapped_column(String(16))

    user: Mapped['User'] = relationship(back_populates='profile')
    trips: Mapped[list['Trip']] = relationship(
        secondary='participants', back_populates='participants'
    )
    trips_details: Mapped[list['Participant']] = relationship(back_populates='profile')
