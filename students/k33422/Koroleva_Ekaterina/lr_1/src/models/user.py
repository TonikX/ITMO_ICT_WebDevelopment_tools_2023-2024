from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from pydantic import EmailStr


__all__ = ['User']

if TYPE_CHECKING:
    from .profile import Profile


class User(Base):
    email: Mapped[EmailStr] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str | bytes] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    profile: Mapped['Profile'] = relationship(back_populates='user')
