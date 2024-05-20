from typing import Collection, Optional

from sqlmodel import Session, select

import personal_finance.infrastructure.persistance.postgres.users.repository as user_repo
from personal_finance.domain.account.account import UserAccount, AccountName, AccountBalance, AccountTag, Tag
from personal_finance.infrastructure.persistance.postgres.account.model import UserAccountModel
from personal_finance.infrastructure.persistance.repository import Repository, ID, T


def to_model(account: UserAccount) -> T:
    return UserAccountModel(
        id=account.id,
        name=account.name.name,
        currency=account.balance.currency,
        amount=account.balance.amount,
        user_id=account.user.id
        )


def to_entity(model: UserAccountModel) -> UserAccount:
    return UserAccount(
        id=model.id,
        name=AccountName(model.name),
        balance=AccountBalance(model.amount, model.currency),
        user=user_repo.to_user(model.user),
        tags=list(map(lambda x: AccountTag(x.id, Tag(x.tag.id, x.tag.name), x.order), model.tags))
    )


class UserAccountRepository(Repository[int, UserAccount]):
    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, identifier: ID) -> Optional[UserAccount]:
        model: UserAccountModel = self.session.exec(select(UserAccountModel).where(UserAccountModel.id == identifier)).first()
        if model is None:
            return None
        return to_entity(model)

    def find_all(self) -> Collection[UserAccount]:
        models: Collection[T] = self.session.exec(select(UserAccountModel)).all()
        return list(map(to_entity, models))

    def save(self, obj: T) -> UserAccount:
        model: UserAccountModel = to_model(obj)
        existing: UserAccountModel = self.session.exec(select(UserAccountModel).where(UserAccountModel.id == model.id)).first()
        if existing is None:
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return to_entity(model)

        existing: UserAccountModel = existing.sqlmodel_update(model.model_dump(exclude_unset=True))
        self.session.add(existing)
        self.session.commit()
        self.session.refresh(existing)
        return to_entity(existing)

    def delete_by_id(self, identifier: ID) -> None:
        model: UserAccountModel = self.session.exec(select(UserAccountModel).where(UserAccountModel.id == identifier)).first()
        if model is None:
            return

        self.session.delete(model)
        self.session.commit()
