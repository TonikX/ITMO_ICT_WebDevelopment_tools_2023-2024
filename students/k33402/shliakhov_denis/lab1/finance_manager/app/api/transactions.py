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