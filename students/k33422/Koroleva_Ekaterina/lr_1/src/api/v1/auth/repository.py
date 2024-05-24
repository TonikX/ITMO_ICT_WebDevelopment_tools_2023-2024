from src.db import db_helper
from src.models import User
from ..core.repository import BaseRepository


class AuthRepository(BaseRepository):
    pass


repository = AuthRepository(
    model=User,
    session_factory=db_helper.get_session
)
