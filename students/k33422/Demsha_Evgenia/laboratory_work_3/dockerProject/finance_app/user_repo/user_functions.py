from sqlmodel import Session, select

from finance_app.connections import engine
from finance_app.user_repo.user_models import User


def select_all_users():
    with Session(engine) as session:
        statement = select(User)
        res = session.exec(statement).all()
        return res


def find_user(name):
    with Session(engine) as session:
        statement = select(User).where(User.username == name)
        return session.exec(statement).first()
