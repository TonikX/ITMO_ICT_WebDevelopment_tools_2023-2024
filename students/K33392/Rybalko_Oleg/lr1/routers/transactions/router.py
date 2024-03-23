from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from conn import get_session
from dependencies import verify_jwt
from models import Transaction

from .models import DeletedTransactionResponse, TransactionRead

router = APIRouter(prefix="/transactions", dependencies=[Depends(verify_jwt)])


@router.post("/", response_model=Transaction)
def create_transaction(transaction: Transaction, session: Session = Depends(get_session)) -> Transaction:
    transaction = Transaction.model_validate(transaction)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


@router.get("/{transaction_id}", response_model=TransactionRead)
def get_transaction(transaction_id: int, session: Session = Depends(get_session)) -> Optional[Transaction]:
    if (transaction := session.get(Transaction, transaction_id)) is None:
        raise HTTPException(HTTPStatus.NOT_FOUND)
    return transaction


@router.put("/{transaction_id}", response_model=Transaction)
def update_transaction(
    transaction_id: int, transaction: Transaction, session: Session = Depends(get_session)
) -> Transaction:
    transaction_obj = session.get(Transaction, transaction_id)
    if not transaction_obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Transaction not found")
    for key, value in transaction.dict().items():
        setattr(transaction_obj, key, value)
    session.add(transaction_obj)
    session.commit()
    session.refresh(transaction_obj)
    return transaction_obj


@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, session: Session = Depends(get_session)) -> DeletedTransactionResponse:
    transaction_obj = session.get(Transaction, transaction_id)
    if not transaction_obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Transaction not found")
    session.delete(transaction_obj)
    session.commit()
    return {"message": "Transaction deleted successfully"}
