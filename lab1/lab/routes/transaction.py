from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import select
from connection import get_session
from models import Transaction

router = APIRouter()

@router.get("/transactions", response_model=List[Transaction], tags=["transaction"])
def get_transactions(session=Depends(get_session)) -> List[Transaction]:
    return session.exec(select(Transaction)).all()

@router.get("/transactions/{transaction_id}", response_model=Transaction, tags=["transaction"])
def get_transaction(transaction_id: int, session=Depends(get_session)) -> Transaction:
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.post("/transactions", response_model=Transaction, tags=["transaction"])
def create_transaction(transaction: Transaction, session=Depends(get_session)) -> Transaction:
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction

@router.patch("/transactions/{transaction_id}", response_model=Transaction, tags=["transaction"])
def update_transaction(transaction_id: int, transaction: Transaction, session=Depends(get_session)) -> Transaction:
    db_transaction = session.get(Transaction, transaction_id)
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    transaction_data = transaction.dict(exclude_unset=True)
    for key, value in transaction_data.items():
        setattr(db_transaction, key, value)
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction

@router.delete("/transactions/{transaction_id}", tags=["transaction"])
def delete_transaction(transaction_id: int, session=Depends(get_session)):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    session.delete(transaction)
    session.commit()
    return {"ok": True}