from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import select
from connection import get_session
from models import TransactionCategory

router = APIRouter()

@router.get("/transaction_categories", response_model=List[TransactionCategory], tags=["transaction_category"])
def get_transaction_categories(session=Depends(get_session)) -> List[TransactionCategory]:
    return session.exec(select(TransactionCategory)).all()

@router.get("/transaction_categories/{category_id}/{transaction_id}", response_model=TransactionCategory, tags=["transaction_category"])
def get_transaction_category(category_id: int, transaction_id: int, session=Depends(get_session)) -> TransactionCategory:
    transaction_category = session.get(TransactionCategory, (category_id, transaction_id))
    if not transaction_category:
        raise HTTPException(status_code=404, detail="TransactionCategory not found")
    return transaction_category

@router.post("/transaction_categories", response_model=TransactionCategory, tags=["transaction_category"])
def create_transaction_category(transaction_category: TransactionCategory, session=Depends(get_session)) -> TransactionCategory:
    session.add(transaction_category)
    session.commit()
    session.refresh(transaction_category)
    return transaction_category

@router.patch("/transaction_categories/{category_id}/{transaction_id}", response_model=TransactionCategory, tags=["transaction_category"])
def update_transaction_category(category_id: int, transaction_id: int, transaction_category: TransactionCategory, session=Depends(get_session)) -> TransactionCategory:
    db_transaction_category = session.get(TransactionCategory, (category_id, transaction_id))
    if not db_transaction_category:
        raise HTTPException(status_code=404, detail="TransactionCategory not found")
    transaction_category_data = transaction_category.dict(exclude_unset=True)
    for key, value in transaction_category_data.items():
        setattr(db_transaction_category, key, value)
    session.add(db_transaction_category)
    session.commit()
    session.refresh(db_transaction_category)
    return db_transaction_category

@router.delete("/transaction_categories/{category_id}/{transaction_id}", tags=["transaction_category"])
def delete_transaction_category(category_id: int, transaction_id: int, session=Depends(get_session)):
    transaction_category = session.get(TransactionCategory, (category_id, transaction_id))
    if not transaction_category:
        raise HTTPException(status_code=404, detail="TransactionCategory not found")
    session.delete(transaction_category)
    session.commit()
    return {"ok": True}
