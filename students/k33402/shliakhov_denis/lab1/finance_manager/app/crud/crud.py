from typing import List, Optional, Dict
from sqlmodel import Session, select, func
from app.models.models import User, Transaction, Category, Budget, TransactionType


def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)

def create_user(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_users(session: Session) -> List[User]:
    statement = select(User)
    results = session.exec(statement).all()
    return results

def delete_user(session: Session, user_id: int):
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
    return user

def update_user(session: Session, user_id: int, user_data: User) -> Optional[User]:
    user = session.get(User, user_id)
    if not user:
        return None
    user.username = user_data.username or user.username
    user.email = user_data.email or user.email
    user.hashed_password = user_data.hashed_password or user.hashed_password
    session.commit()
    session.refresh(user)
    return user

def create_transaction(session: Session, transaction: Transaction) -> Transaction:
    budget = session.query(Budget).filter(
        Budget.category_id == transaction.category_id
    ).first()

    if budget:
        if transaction.type == TransactionType.EXPENSE:
            budget.amount -= transaction.amount
        else:
            budget.amount += transaction.amount

    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction

def get_transaction(session: Session, transaction_id: int) -> Optional[Transaction]:
    return session.get(Transaction, transaction_id)

def get_income_transactions(session: Session) -> Optional[List[Transaction]]:
    return session.query(Transaction).filter(Transaction.type == TransactionType.INCOME)

def get_expense_transactions(session: Session) -> Optional[List[Transaction]]:
    return session.query(Transaction).filter(Transaction.type == TransactionType.EXPENSE)

def get_transactions(session: Session) -> List[Transaction]:
    statement = select(Transaction)
    results = session.exec(statement).all()
    return results

def delete_transaction(session: Session, transaction_id: int):
    transaction = session.get(Transaction, transaction_id)
    if transaction:
        session.delete(transaction)
        session.commit()
    return transaction

def update_transaction(session: Session, transaction_id: int, transaction_data: Transaction) -> Optional[Transaction]:
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        return None
    transaction.amount = transaction_data.amount or transaction.amount
    transaction.timestamp = transaction_data.timestamp or transaction.timestamp
    transaction.description = transaction_data.description or transaction.description
    transaction.category_id = transaction_data.category_id or transaction.category_id
    session.commit()
    session.refresh(transaction)
    return transaction

def get_transactions_by_category(session: Session, category_name: str) -> List[Transaction]:
    statement = (select(Transaction)
                 .join(Category)
                 .where(Category.name == category_name))
    results = session.exec(statement).all()
    return results

def create_category(session: Session, category: Category) -> Category:
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

def get_category(session: Session, category_id: int) -> Optional[Category]:
    return session.get(Category, category_id)

def get_categories(session: Session) -> List[Category]:
    statement = select(Category)
    results = session.exec(statement).all()
    return results

def delete_category(session: Session, category_id: int):
    category = session.get(Category, category_id)
    if category:
        session.delete(category)
        session.commit()
    return category

def update_category(session: Session, category_id: int, category_data: Category) -> Optional[Category]:
    category = session.get(Category, category_id)
    if not category:
        return None
    category.name = category_data.name or category.name
    session.commit()
    session.refresh(category)
    return category

def create_budget(session: Session, budget: Budget) -> Budget:
    session.add(budget)
    session.commit()
    session.refresh(budget)
    return budget

def get_budget(session: Session, budget_id: int) -> Optional[Budget]:
    return session.get(Budget, budget_id)

def get_budgets(session: Session) -> List[Budget]:
    statement = select(Budget)
    results = session.exec(statement).all()
    return results

def delete_budget(session: Session, budget_id: int):
    budget = session.get(Budget, budget_id)
    if budget:
        session.delete(budget)
        session.commit()
    return budget

def update_budget(session: Session, budget_id: int, budget_data: Budget) -> Optional[Budget]:
    budget = session.get(Budget, budget_id)
    if not budget:
        return None
    budget.amount = budget_data.amount or budget.amount
    budget.start_date = budget_data.start_date or budget.start_date
    budget.end_date = budget_data.end_date or budget.end_date
    budget.category_id = budget_data.category_id or budget.category_id
    session.commit()
    session.refresh(budget)
    return budget

def get_financial_report(session: Session) -> Dict[str, float]:
    income_statement = select(func.sum(Transaction.amount)).where(Transaction.type == TransactionType.INCOME)
    total_income = session.exec(income_statement).first() or 0

    expense_statement = select(func.sum(Transaction.amount)).where(Transaction.type == TransactionType.EXPENSE)
    total_expense = session.exec(expense_statement).first() or 0

    financial_report = {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense
    }

    return financial_report