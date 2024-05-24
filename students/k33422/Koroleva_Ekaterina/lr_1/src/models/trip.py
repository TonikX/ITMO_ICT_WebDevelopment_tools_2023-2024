from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

__all__ = ['Trip']

if TYPE_CHECKING:
    from .profile import Profile
    from .participant import Participant


class Trip(Base):
    __table_args__ = (
        CheckConstraint('end_date > start_date', name='dates_check'),
    )

    profile_id: Mapped[int] = mapped_column(
        ForeignKey('profiles.id', ondelete='CASCADE')
    )
    title: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(Text, default='', server_default='')
    start_date: Mapped[date] = mapped_column()
    end_date: Mapped[date] = mapped_column()
    start_location: Mapped[str] = mapped_column(String(128))
    destination: Mapped[str] = mapped_column(String(128))

    profile: Mapped['Profile'] = relationship(back_populates='trips')
    participants: Mapped[list['Profile']] = relationship(
        secondary='participants', back_populates='trips'
    )
    profiles_details: Mapped[list['Participant']] = relationship(back_populates='trip')
