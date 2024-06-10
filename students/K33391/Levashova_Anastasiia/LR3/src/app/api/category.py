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
    return session.get(Category, category_id)


@router.post("/")
def category_create(cat: CategoryDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                  "data": Category}):
    cat = Category.model_validate(cat)
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return {"status": 200, "data": cat}


@router.delete("/{category_id}")
def delete_category(category_id: int, session=Depends(get_session)) -> TypedDict('Response', {"is_deleted": bool}):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"is_deleted": True}


@router.patch("/{category_id}")
def update_task(category_id: int, category: CategoryDefault, session=Depends(get_session)) -> CategoryDefault:
    db_categories = session.get(Category, category_id)
    if not db_categories:
        raise HTTPException(status_code=404, detail="Category not found")
    categories_data = category.model_dump(exclude_unset=True)
    for key, value in categories_data.items():
        setattr(db_categories, key, value)
    session.add(db_categories)
    session.commit()
    session.refresh(db_categories)
    return db_categories
