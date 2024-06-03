from typing import List

from fastapi import HTTPException, Depends, APIRouter
from sqlmodel import select

from connection import get_session
from models import Book, BookIn, BookOut, CategoryOut, Category, BookCategory

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("", response_model=List[BookOut])
def books_list(session=Depends(get_session)):
    return session.exec(select(Book)).all()


@router.get("/{book_id}", response_model=BookOut)
def books_get(book_id: int, session=Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("", response_model=BookOut)
def books_create(book: BookIn, session=Depends(get_session)):
    book = Book.model_validate(book)
    # todo выкинуть ошибку если автора не существует
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.delete("/{book_id}", response_model=dict)
def book_delete(book_id: int, session=Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"message": "Book deleted successfully"}


@router.patch("/{book_id}", response_model=BookOut)
def book_update(book_id: int, book: BookIn, session=Depends(get_session)):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)
    session.add(db_book)
    session.commit()
    return db_book


@router.get("/{book_id}/categories", response_model=List[CategoryOut])
def book_categories_list(book_id: int, session=Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return [book_category for book_category in book.categories]


@router.post("/{book_id}/categories/{category_id}", response_model=BookOut)
def add_category_to_book(book_id: int, category_id: int, session=Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    book_category = BookCategory(book_id=book_id, category_id=category_id)
    session.add(book_category)
    session.commit()
    session.refresh(book_category)
    return book


@router.delete("/{book_id}/categories/{category_id}", response_model=dict)
def remove_category_from_book(book_id: int, category_id: int, session=Depends(get_session)):
    book_category = session.exec(
        select(BookCategory)
        .where(BookCategory.book_id == book_id)
        .where(BookCategory.category_id == category_id)
    ).first()
    if not book_category:
        raise HTTPException(status_code=404, detail="Category not found in mentioned book")
    session.delete(book_category)
    session.commit()
    return {"message": "Category removed from book successfully"}
