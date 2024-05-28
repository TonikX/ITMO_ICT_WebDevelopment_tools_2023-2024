from sqlmodel import Session
from sqlmodel import select

from src.models import User
from src.settings.connection import engine


def find_user(name):
    with Session(engine) as session:
        statement = select(User).where(User.username == name)
        return session.exec(statement).first()
