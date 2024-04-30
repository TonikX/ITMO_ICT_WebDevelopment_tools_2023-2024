from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLEnum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

__all__ = ['Status', 'Participant']

if TYPE_CHECKING:
    from .profile import Profile
    from .trip import Trip


class Status(str, Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


class Participant(Base):
    __table_args__ = (
        UniqueConstraint('profile_id', 'trip_id', name='profile_trip_unique'),
    )

    profile_id: Mapped[int] = mapped_column(
        ForeignKey('profiles.id', ondelete='CASCADE')
    )
    trip_id: Mapped[int] = mapped_column(ForeignKey('trips.id', ondelete='CASCADE'))
    status: Mapped[Status] = mapped_column(SQLEnum(Status), default=Status.PENDING)

    profile: Mapped['Profile'] = relationship(back_populates='trips_details')
    trip: Mapped['Trip'] = relationship(back_populates='profiles_details')
