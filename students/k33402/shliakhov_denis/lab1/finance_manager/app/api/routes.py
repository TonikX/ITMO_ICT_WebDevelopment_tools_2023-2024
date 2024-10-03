from fastapi import APIRouter, Depends
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.db import get_session
from app.crud import crud

router = APIRouter()

@router.get("/report", response_model=Dict[str, Any])
def get_financial_report(session: Session = Depends(get_session)):
    return crud.get_financial_report(session)