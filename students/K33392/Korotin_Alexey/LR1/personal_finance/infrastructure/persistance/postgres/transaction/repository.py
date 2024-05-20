import datetime
from typing import Collection, Optional

from fastapi import Depends
from sqlmodel import Session, select

from personal_finance.application.accounts.service import UserAccountService
from personal_finance.application.users.service import UserService
from personal_finance.domain.finance import Money
from personal_finance.domain.transaction.transaction import IncomeTransaction, TransactionComment, ExpenseTransaction, \
    TransferTransaction
from personal_finance.infrastructure.persistance.postgres.database import get_session
from personal_finance.infrastructure.persistance.postgres.transaction.model import IncomeTransactionModel, \
    ExpenseTransactionModel, TransferTransactionModel
from personal_finance.infrastructure.persistance.repository import Repository, ID, T
import personal_finance.infrastructure.persistance.postgres.users.repository as user_repo
import personal_finance.infrastructure.persistance.postgres.cashflow.repository as cf_repo
import personal_finance.infrastructure.persistance.postgres.account.repository as acc_repo


def income_to_model(transaction: IncomeTransaction) -> IncomeTransactionModel:
    return IncomeTransactionModel(
        id=transaction.id,
        transaction_type=transaction.transaction_type,
        status=transaction.status,
        comment=transaction.comment.value,
        user_id=transaction.user.id,
        timestamp=transaction.timestamp,
        currency=transaction.money.currency,
        amount=transaction.money.amount,
        source_id=transaction.source.id,
        destination_id=transaction.destination.id
    )


def income_to_entity(transaction: IncomeTransactionModel) -> IncomeTransaction:
    return IncomeTransaction(
        transaction.id,
        transaction.status,
        TransactionComment(transaction.comment),
        user_repo.to_user(transaction.user),
        Money(transaction.amount, transaction.currency),
        cf_repo.source_model_to_entity(transaction.source),
        acc_repo.to_entity(transaction.destination),
    )


class IncomeTransactionRepository(Repository[int, IncomeTransaction]):
    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, identifier: ID) -> Optional[IncomeTransaction]:
        model: IncomeTransactionModel | None = (self.session.exec(select(IncomeTransactionModel)
                                                                 .where(IncomeTransactionModel.id == identifier))
                                                .first())

        if model is None:
            return None

        return income_to_entity(model)

    def find_all(self) -> Collection[IncomeTransaction]:
        models: Collection[IncomeTransactionModel] = self.session.exec(select(IncomeTransactionModel)).all()
        return list(map(income_to_entity, models))

    def save(self, obj: IncomeTransaction) -> IncomeTransaction:
        model: IncomeTransactionModel = income_to_model(obj)
        existing: IncomeTransactionModel = self.session.exec(select(IncomeTransactionModel)
                                                        .where(IncomeTransactionModel.id == model.id)).first()
        if existing is None:
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return income_to_entity(model)

        existing: IncomeTransactionModel = existing.sqlmodel_update(model.model_dump(exclude_unset=True))
        self.session.add(existing)
        self.session.commit()
        self.session.refresh(existing)
        return income_to_entity(existing)

    def delete_by_id(self, identifier: ID) -> None:
        model: IncomeTransactionModel = self.session.exec(select(IncomeTransactionModel)
                                                     .where(IncomeTransactionModel.id == identifier)).first()
        if model is None:
            return

        self.session.delete(model)
        self.session.commit()


def expense_to_model(transaction: ExpenseTransaction) -> ExpenseTransactionModel:
    return ExpenseTransactionModel(
        id=transaction.id,
        transaction_type=transaction.transaction_type,
        status=transaction.status,
        comment=transaction.comment.value,
        user_id=transaction.user.id,
        timestamp=transaction.timestamp,
        currency=transaction.money.currency,
        amount=transaction.money.amount,
        source_id=transaction.source.id,
        category_id=transaction.category.id
    )


def expense_to_entity(transaction: ExpenseTransactionModel) -> ExpenseTransaction:
    return ExpenseTransaction(
        transaction.id,
        transaction.status,
        TransactionComment(transaction.comment),
        user_repo.to_user(transaction.user),
        Money(transaction.amount, transaction.currency),
        acc_repo.to_entity(transaction.source),
        cf_repo.category_model_to_entity(transaction.category)
    )


class ExpenseTransactionRepository(Repository[int, ExpenseTransaction]):
    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, identifier: ID) -> Optional[ExpenseTransaction]:
        model: ExpenseTransactionModel | None = (self.session.exec(select(ExpenseTransactionModel)
                                                                 .where(ExpenseTransactionModel.id == identifier))
                                                .first())

        if model is None:
            return None

        return expense_to_entity(model)

    def find_all(self) -> Collection[ExpenseTransaction]:
        models: Collection[ExpenseTransactionModel] = self.session.exec(select(ExpenseTransactionModel)).all()
        return list(map(expense_to_entity, models))

    def save(self, obj: ExpenseTransaction) -> ExpenseTransaction:
        model: ExpenseTransactionModel = expense_to_model(obj)
        existing: ExpenseTransactionModel = self.session.exec(select(ExpenseTransactionModel)
                                                        .where(ExpenseTransaction.id == model.id)).first()
        if existing is None:
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return expense_to_entity(model)

        existing: ExpenseTransactionModel = existing.sqlmodel_update(model.model_dump(exclude_unset=True))
        self.session.add(existing)
        self.session.commit()
        self.session.refresh(existing)
        return expense_to_entity(existing)

    def delete_by_id(self, identifier: ID) -> None:
        model: ExpenseTransactionModel = self.session.exec(select(ExpenseTransactionModel)
                                                     .where(ExpenseTransactionModel.id == identifier)).first()
        if model is None:
            return

        self.session.delete(model)
        self.session.commit()


def transfer_to_model(transaction: TransferTransaction) -> TransferTransactionModel:
    return TransferTransactionModel(
        id=transaction.id,
        transaction_type=transaction.transaction_type,
        status=transaction.status,
        comment=transaction.comment.value,
        user_id=transaction.user.id,
        #timestamp=transaction.timestamp,
        timestamp=datetime.datetime.now(),
        currency=str(transaction.money.currency),
        amount=transaction.money.amount,
        source_id=transaction.source.id,
        destination_id=transaction.destination.id
    )


def transfer_to_entity(transaction: TransferTransactionModel) -> TransferTransaction:
    return TransferTransaction(
        transaction.id,
        transaction.status,
        TransactionComment(transaction.comment),
        user_repo.to_user(transaction.user),
        Money(transaction.amount, transaction.currency),
        acc_repo.to_entity(transaction.source),
        acc_repo.to_entity(transaction.destination)
    )


class TransferTransactionRepository(Repository[int, TransferTransaction]):
    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, identifier: ID) -> Optional[TransferTransaction]:
        model: TransferTransactionModel | None = (self.session.exec(select(TransferTransactionModel)
                                                                 .where(TransferTransactionModel.id == identifier))
                                                .first())

        if model is None:
            return None

        return transfer_to_entity(model)

    def find_all(self) -> Collection[TransferTransaction]:
        models: Collection[TransferTransactionModel] = self.session.exec(select(TransferTransactionModel)).all()
        return list(map(transfer_to_entity, models))

    def save(self, obj: TransferTransaction) -> TransferTransaction:
        model: TransferTransactionModel = transfer_to_model(obj)
        existing: TransferTransactionModel = self.session.exec(select(TransferTransactionModel)
                                                        .where(TransferTransactionModel.id == model.id)).first()
        if existing is None:
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return transfer_to_entity(model)

        existing: TransferTransactionModel = existing.sqlmodel_update(model.model_dump(exclude_unset=True))
        self.session.add(existing)
        self.session.commit()
        self.session.refresh(existing)
        return transfer_to_entity(existing)

    def delete_by_id(self, identifier: ID) -> None:
        model: TransferTransactionModel = self.session.exec(select(TransferTransactionModel)
                                                     .where(TransferTransactionModel.id == identifier)).first()
        if model is None:
            return

        self.session.delete(model)
        self.session.commit()
