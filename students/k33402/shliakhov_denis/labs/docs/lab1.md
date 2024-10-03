# Лабораторная работа № 1

## Задание
### Разработка сервиса для управления личными финансами
Необходимо создать простой сервис для управления личными финансами. Сервис должен позволять пользователям вводить доходы и расходы, устанавливать бюджеты на различные категории, а также просматривать отчеты о своих финансах. Дополнительные функции могут включать в себя возможность получения уведомлений о превышении бюджета, анализа трат и установки целей на будущее.

## Процесс разработки
## БД
`base.py`
```python
from sqlmodel import SQLModel, Field
from typing import Optional

class BaseModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
```
`__init__.py`
```python
from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = "postgresql://postgres@localhost/d.shlyakhov"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
```

`crud.py`
```python
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
```

`transactions.py`
```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db import get_session
from app.models.models import Transaction, TransactionRead
from app.crud import crud

router = APIRouter()

@router.post("/transactions/", response_model=Transaction)
def create_transaction(transaction: Transaction, session: Session = Depends(get_session)):
    return crud.create_transaction(session, transaction)

@router.get("/transactions/{transaction_id}", response_model=TransactionRead)
def read_transaction(transaction_id: int, session: Session = Depends(get_session)):
    db_transaction = crud.get_transaction(session, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@router.get("/transactions/", response_model=List[TransactionRead])
def read_transactions(session: Session = Depends(get_session)):
    return crud.get_transactions(session)

@router.get("/transactions/all/expense", response_model=List[TransactionRead])
def read_expense_transactions(session: Session = Depends(get_session)):
    return crud.get_expense_transactions(session)

@router.get("/transactions/all/income", response_model=List[TransactionRead])
def read_income_transactions(session: Session = Depends(get_session)):
    return crud.get_income_transactions(session)

@router.delete("/transactions/{transaction_id}", response_model=Transaction)
def delete_transaction(transaction_id: int, session: Session = Depends(get_session)):
    transaction = crud.delete_transaction(session, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.put("/transactions/{transaction_id}", response_model=Transaction)
def update_transaction(transaction_id: int, transaction: Transaction, session: Session = Depends(get_session)):
    updated_transaction = crud.update_transaction(session, transaction_id, transaction)
    if updated_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return updated_transaction
```

`models.py`
```python
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from enum import Enum

class TransactionType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str

    transactions: List["Transaction"] = Relationship(back_populates="user")
    budgets: List["Budget"] = Relationship(back_populates="user")

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, default="Other")

    transactions: List["Transaction"] = Relationship(back_populates="category")
    budgets: List["Budget"] = Relationship(back_populates="category")


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float
    timestamp: datetime = datetime.utcnow()
    description: Optional[str] = None
    type: TransactionType = TransactionType.EXPENSE

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")

    user: Optional[User] = Relationship(back_populates="transactions")
    category: Optional[Category] = Relationship(back_populates="transactions")


class Budget(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float
    start_date: datetime
    end_date: datetime

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")

    user: Optional[User] = Relationship(back_populates="budgets")
    category: Optional[Category] = Relationship(back_populates="budgets")

class CategoryRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class TransactionRead(BaseModel):
    id: int
    amount: float
    timestamp: datetime
    description: Optional[str]
    type: TransactionType
    category: CategoryRead

    class Config:
        orm_mode = True

class UserRead(BaseModel):
    id: int
    username: str
    email: str
    transactions: List[TransactionRead] = []

    class Config:
        orm_mode = True
```
# Выводы

Создал интерфейс для сервиса бюджета, который буду интегрировать в приложение на андроиде