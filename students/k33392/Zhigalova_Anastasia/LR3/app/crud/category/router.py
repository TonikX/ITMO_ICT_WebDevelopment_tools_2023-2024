from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Category
from db import get_session

from pydanticModels import *


router = APIRouter()

@router.post("/categories/", response_model=Category)
def create_category(category: Category, session: Session = Depends(get_session)):
    db_category = Category.from_orm(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@router.get("/categories/", response_model=List[Category])
def read_categories(session: Session = Depends(get_session)):
    return session.query(Category).all()

@router.get("/categories/{category_id}", response_model=Category)
def read_category(category_id: int, session: Session = Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/categories/{category_id}", response_model=Category)
def update_category(category_id: int, category: Category, session: Session = Depends(get_session)):
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    for var, value in vars(category).items():
        setattr(db_category, var, value) if value else None
    session.commit()
    return category


@router.delete("/categories/{category_id}", response_model=dict)
def delete_category(category_id: int, session: Session = Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    for task_category in category.category_tasks:
        session.delete(task_category)
    
    session.delete(category)
    session.commit()
    return {"ok": True}