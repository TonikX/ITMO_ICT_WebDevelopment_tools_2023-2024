from typing import Collection, Optional

from sqlmodel import Session, select

from personal_finance.domain.cashflow.cashflow import IncomeSource, CashflowName, ExpenseCategory
from personal_finance.domain.finance import Money
from personal_finance.infrastructure.persistance.postgres.cashflow.model import IncomeSourceModel, ExpenseCategoryModel
from personal_finance.infrastructure.persistance.repository import Repository, ID, T
import personal_finance.infrastructure.persistance.postgres.users.repository as user_repo


def source_model_to_entity(source: IncomeSourceModel) -> IncomeSource:
    return IncomeSource(
        id=source.id,
        name=CashflowName(source.name),
        user=user_repo.to_user(source.user),
        amount=Money(source.amount, source.currency)
    )


def source_entity_to_model(source: IncomeSource) -> IncomeSourceModel:
    return IncomeSourceModel(
        id=source.id,
        name=source.name.name,
        user_id=source.user.id,
        amount=source.expected_periodic_amount.amount,
        currency=source.expected_periodic_amount.currency
    )


class IncomeSourceRepository(Repository[int, IncomeSource]):
    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, identifier: ID) -> Optional[IncomeSource]:
        model: IncomeSourceModel | None = self.session.exec(select(IncomeSourceModel)
                                                     .where(IncomeSourceModel.id == identifier)).first()

        if model is None:
            return None

        return source_model_to_entity(model)

    def find_all(self) -> Collection[IncomeSource]:
        models: Collection[T] = self.session.exec(select(IncomeSourceModel)).all()
        return list(map(source_model_to_entity, models))

    def save(self, obj: T) -> IncomeSource:
        model: IncomeSourceModel = source_entity_to_model(obj)
        existing: IncomeSourceModel = self.session.exec(select(IncomeSourceModel)
                                                        .where(IncomeSourceModel.id == model.id)).first()
        if existing is None:
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return source_model_to_entity(model)

        existing: IncomeSourceModel = existing.sqlmodel_update(model.model_dump(exclude_unset=True))
        self.session.add(existing)
        self.session.commit()
        self.session.refresh(existing)
        return source_model_to_entity(existing)

    def delete_by_id(self, identifier: ID) -> None:
        model: IncomeSourceModel = self.session.exec(select(IncomeSourceModel)
                                                     .where(IncomeSourceModel.id == identifier)).first()
        if model is None:
            return

        self.session.delete(model)
        self.session.commit()


def category_model_to_entity(category: ExpenseCategoryModel) -> ExpenseCategory:
    return ExpenseCategory(
        id=category.id,
        name=CashflowName(category.name),
        user=user_repo.to_user(category.user),
        amount=Money(category.amount, category.currency)
    )


def category_entity_to_model(category: ExpenseCategory) -> ExpenseCategoryModel:
    return ExpenseCategoryModel(
        id=category.id,
        name=category.name.name,
        user_id=category.user.id,
        amount=category.expected_periodic_amount.amount,
        currency=category.expected_periodic_amount.currency
    )


class ExpenseCategoryRepository(Repository[int, ExpenseCategory]):

    session: Session

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, identifier: ID) -> Optional[ExpenseCategory]:
        model: ExpenseCategoryModel | None = self.session.exec(select(ExpenseCategoryModel)
                                                            .where(ExpenseCategoryModel.id == identifier)).first()

        if model is None:
            return None

        return category_model_to_entity(model)

    def find_all(self) -> Collection[ExpenseCategory]:
        models: Collection[T] = self.session.exec(select(ExpenseCategoryModel)).all()
        return list(map(category_model_to_entity, models))

    def save(self, obj: T) -> ExpenseCategory:
        model: ExpenseCategoryModel = category_entity_to_model(obj)
        existing: ExpenseCategoryModel = self.session.exec(select(ExpenseCategoryModel)
                                                        .where(ExpenseCategoryModel.id == model.id)).first()
        if existing is None:
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return category_model_to_entity(model)

        existing: ExpenseCategoryModel = existing.sqlmodel_update(model.model_dump(exclude_unset=True))
        self.session.add(existing)
        self.session.commit()
        self.session.refresh(existing)
        return category_model_to_entity(existing)

    def delete_by_id(self, identifier: ID) -> None:
        model: ExpenseCategoryModel = self.session.exec(select(ExpenseCategoryModel)
                                                     .where(ExpenseCategoryModel.id == identifier)).first()
        if model is None:
            return

        self.session.delete(model)
        self.session.commit()
