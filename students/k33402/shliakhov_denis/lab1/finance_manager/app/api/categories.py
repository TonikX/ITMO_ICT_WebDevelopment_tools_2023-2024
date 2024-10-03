from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db import get_session
from app.models.models import Category
from app.crud import crud

router = APIRouter()

@router.post("/categories/", response_model=Category)
def create_category(category: Category, session: Session = Depends(get_session)):
    return crud.create_category(session, category)

@router.get("/categories/{category_id}", response_model=Category)
def read_category(category_id: int, session: Session = Depends(get_session)):
    db_category = crud.get_category(session, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.get("/categories/", response_model=List[Category])
def read_categories(session: Session = Depends(get_session)):
    return crud.get_categories(session)

@router.delete("/categories/{category_id}", response_model=Category)
def delete_category(category_id: int, session: Session = Depends(get_session)):
    category = crud.delete_category(session, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/categories/{category_id}", response_model=Category)
def update_category(category_id: int, category: Category, session: Session = Depends(get_session)):
    updated_category = crud.update_category(session, category_id, category)
    if updated_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category