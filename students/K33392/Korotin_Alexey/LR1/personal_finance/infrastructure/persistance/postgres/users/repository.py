from typing import Collection, Optional

from sqlmodel import Session, select

from personal_finance.domain.users.user import User, UserName, Login
from personal_finance.infrastructure.persistance.repository import Repository, ID, T
from .model import UserModel


def to_user(model: UserModel) -> User:
    return User(
        id=model.id,
        first_name=UserName(model.first_name),
        last_name=UserName(model.last_name),
        login=Login(model.login),
        password=model.password
    )


def to_model(user: User) -> UserModel:
    return UserModel(
        id=user.id,
        first_name=user.first_name.value,
        last_name=user.last_name.value,
        login=user.login.value,
        password=user.password
    )


class UserRepository(Repository[int, User]):
    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, identifier: ID) -> Optional[User]:
        model: UserModel = self.session.exec(select(UserModel).where(UserModel.id == identifier)).first()
        if model is None:
            return None
        return to_user(model)

    def find_all(self) -> Collection[User]:
        models: Collection[T] = self.session.exec(select(UserModel)).all()
        return list(map(to_user, models))

    def save(self, obj: User) -> User:
        model: UserModel = to_model(obj)
        existing: UserModel = self.session.exec(select(UserModel).where(UserModel.id == model.id)).first()
        if existing is None:
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return to_user(model)

        existing: UserModel = existing.sqlmodel_update(model.model_dump(exclude_unset=True))
        self.session.add(existing)
        self.session.commit()
        self.session.refresh(existing)
        return to_user(existing)

    def delete_by_id(self, identifier: ID) -> None:
        model: UserModel = self.session.exec(select(UserModel).where(UserModel.id == identifier)).first()
        if model is None:
            return

        self.session.delete(model)
        self.session.commit()

    def find_by_login(self, login: str) -> Optional[User]:
        model: UserModel | None = self.session.exec(select(UserModel).where(UserModel.login == login)).first()
        if model is None:
            return None
        return to_user(model)


