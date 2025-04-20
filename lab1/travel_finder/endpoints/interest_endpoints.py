from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from db.connection import get_session
from model.models.models import Interest, UserInterest
from model.schemas.interest import InterestRead, InterestCreate
from model.schemas.user_interest import UserInterestRead, UserInterestCreate

interest_router = APIRouter()
user_interest_router = APIRouter()


@interest_router.post("/", response_model=InterestRead)
def create_interest(interest: InterestCreate, session: Session = Depends(get_session)):
    db_interest = Interest.model_validate(interest)
    session.add(db_interest)
    session.commit()
    session.refresh(db_interest)
    return db_interest


@interest_router.get("/", response_model=List[InterestRead])
def get_all_interests(session: Session = Depends(get_session)):
    return session.exec(select(Interest)).all()


@interest_router.get("/{interest_id}", response_model=InterestRead)
def get_interest(interest_id: int, session: Session = Depends(get_session)):
    interest = session.get(Interest, interest_id)
    if not interest:
        raise HTTPException(status_code=404, detail="Interest not found")
    return interest


@interest_router.delete("/{interest_id}", response_model=dict)
def delete_interest(interest_id: int, session: Session = Depends(get_session)):
    interest = session.get(Interest, interest_id)
    if not interest:
        raise HTTPException(status_code=404, detail="Interest not found")
    session.delete(interest)
    session.commit()
    return {"ok": True}

