from sqlmodel import select
from sqlmodel import Session

from db import engine
from lib.models import User


def find_user(username):
    with Session(engine) as session:
        return session.exec(select(User).where(User.username == username)).first()
