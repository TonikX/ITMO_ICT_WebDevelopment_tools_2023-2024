from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core import db
from app.models.main import TransactionsUpdate
from app.models.main import (
    Transactions,
    Category,
    CategoryTransactionLink,
)
from app.models.user import User
import app.services.auth as auth_service

router = APIRouter()


@router.put("/{transaction_id}", response_model=Transactions)
def update_transaction(
    transaction_id: int,
    transaction: TransactionsUpdate,
    session: Session = Depends(db.get_session),
    user: User = Depends(auth_service.get_current_user),
):
    db_transaction = session.get(Transactions, transaction_id)
    if db_transaction is None or db_transaction.balance is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    category = session.exec(
        select(Category).where(Category.id == transaction.category_id)
    ).first()
    if category is None:
        raise HTTPException(status_code=400, detail="Invalid category")

    if db_transaction.type == "income":
        db_transaction.balance.balance -= db_transaction.value
    elif db_transaction.type == "expenses":
        db_transaction.balance.balance += db_transaction.value

    for key, value in transaction.dict(exclude_unset=True).items():
        setattr(db_transaction, key, value)

    if transaction.type == "income":
        db_transaction.balance.balance += transaction.value
    elif transaction.type == "expenses":
        db_transaction.balance.balance -= transaction.value

    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)

    db_category_transaction_link = session.exec(
        select(CategoryTransactionLink).where(
            CategoryTransactionLink.transaction_id == transaction_id
        )
    )
    session.delete(db_category_transaction_link)
    category_transaction_link = CategoryTransactionLink(
        category_id=transaction.category_id, transaction_id=transaction_id
    )
    session.add(category_transaction_link)
    session.commit()

    return db_transaction
