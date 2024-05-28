from sqlmodel import select

from database import engine, Session
from models.user import User

def select_all_users():
    with Session(engine) as session:
        statement = select(User)
        res = session.exec(statement).all()
        return res


def find_user(name):
    with Session(engine) as session:
        statement = select(User).where(User.username == name)
        return session.exec(statement).first()
    
def find_user_balance_id(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user:
            return user.balance.id if user.balance else None
        return None