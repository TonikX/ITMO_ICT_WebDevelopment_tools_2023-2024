from typing import List
from fastapi import HTTPException, Depends, APIRouter
from sqlmodel import select
from typing_extensions import TypedDict
from models import Category, CategoryDefault
from connection import get_session

router = APIRouter()

@router.get("/")
def categories_list(session=Depends(get_session)) -> List[Category]:
    return session.exec(select(Category)).all()

@router.get("/{category_id}")
def get_category(category_id: int, session=Depends(get_session)) -> Category:
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/")
def category_create(category: CategoryDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Category}):
    category = Category.model_validate(category)
    session.add(category)
    session.commit()
    session.refresh(category)
    return {"status": 200, "data": category}

@router.delete("/{category_id}")
def delete_category(category_id: int, session=Depends(get_session)) -> TypedDict('Response', {"is_deleted": bool}):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"is_deleted": True}

@router.patch("/{category_id}")
def update_category(category_id: int, category: CategoryDefault, session=Depends(get_session)) -> Category:
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    category_data = category.model_dump(exclude_unset=True)
    for key, value in category_data.items():
        setattr(db_category, key, value)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category
