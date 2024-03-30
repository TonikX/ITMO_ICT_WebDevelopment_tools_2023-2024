import models
from db import get_session_func
import sqlmodel


def get_user_by_username(username: str) -> models.User:
    with get_session_func() as session:
        select_statement = \
            sqlmodel.select(models.User).\
            where(models.User.username == username)
        user = session.exec(select_statement).one_or_none()
    if user is None:
        raise ValueError('no user with such username')
    return user
