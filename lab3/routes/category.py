from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import select
from connection import get_session
from models import Category

router = APIRouter()

@router.get("/categories", response_model=List[Category], tags=["category"])
def get_categories(session=Depends(get_session)) -> List[Category]:
    return session.exec(select(Category)).all()

@router.get("/categories/{category_id}", response_model=Category, tags=["category"])
def get_category(category_id: int, session=Depends(get_session)) -> Category:
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/categories", response_model=Category, tags=["category"])
def create_category(category: Category, session=Depends(get_session)) -> Category:
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

@router.patch("/categories/{category_id}", response_model=Category, tags=["category"])
def update_category(category_id: int, category: Category, session=Depends(get_session)) -> Category:
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    category_data = category.dict(exclude_unset=True)
    for key, value in category_data.items():
        setattr(db_category, key, value)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category

@router.delete("/categories/{category_id}", tags=["category"])
def delete_category(category_id: int, session=Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"ok": True}