from sqlmodel import Session, select

from db.connection import engine
from models.user_models import User


def select_all_users():
    with Session(engine) as session:
        statement = select(User)
        res = session.exec(statement).all()
        return res


def find_user(name):
    with Session(engine) as session:
        statement = select(User).where(User.name == name)
        return session.exec(statement).first()

