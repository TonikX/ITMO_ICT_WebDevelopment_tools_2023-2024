from fastapi import APIRouter, Depends
from db import get_session
from models import Transaction

transactionRouter = APIRouter(prefix="/transactions", tags=["transaction"])  # отвечает за swagger


@transactionRouter.get("/", response_model=list[Transaction])
async def get_transactions(session=Depends(get_session)):
    transactions = session.query(Transaction).all()
    return transactions


@transactionRouter.get("/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: int, session=Depends(get_session)):
    transaction = session.query(Transaction).filter_by(id=transaction_id).first()
    return transaction


@transactionRouter.post("/")
async def create_transaction(transaction: Transaction, session=Depends(get_session)):
    transaction = Transaction.validate(transaction)
    transaction.id = None
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


@transactionRouter.patch("/{transaction_id}")
async def update_transaction(transaction: Transaction, transaction_id: int, session=Depends(get_session)):
    transaction = Transaction.validate(transaction)
    transaction_from_db = session.query(Transaction).filter_by(id=transaction_id).first()
    if transaction_from_db is None:
        return "No such transaction"
    transaction_data = transaction.model_dump(exclude_unset=True)
    for key, value in transaction_data.items():
        setattr(transaction_from_db, key, value)
    session.add(transaction_from_db)
    session.commit()
    session.refresh(transaction_from_db)
    return transaction_from_db


@transactionRouter.delete("/{transaction_id}")
async def delete_transaction(transaction_id: int, session=Depends(get_session)):
    session.query(Transaction).filter_by(id=transaction_id).delete()
    session.commit()
    return "Deleted"
