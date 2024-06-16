from sqlmodel import Session, select
from src.models import UserCreate, User
from src.services.auth import get_password_hash, verify_password
from typing import Union


def create_user(session: Session, user_create: UserCreate) -> User:
    db_user = User.model_validate(
        user_create, update={"pass_hash": get_password_hash(user_create.password)}
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_username(session: Session, username: str) -> Union[User, None]:
    query = select(User).where(User.username == username)
    user = session.exec(query).first()
    return user


def get_user_by_id(session: Session, id: int) -> Union[User, None]:
    query = select(User).where(User.id == id)
    user = session.exec(query).first()
    return user


def authenticate(session: Session, username: str, password: str) -> Union[User, None]:
    user = get_user_by_username(session, username)
    if not user:
        return None
    if not verify_password(password, user.pass_hash):
        return None
    return user
