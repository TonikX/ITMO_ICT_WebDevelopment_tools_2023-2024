from fastapi import FastAPI, HTTPException, Depends
from typing import List

from sqlmodel import select, Session
from typing_extensions import TypedDict

from connection import init_db, get_session
from models import Book, Author, BookCategory, Category, AuthorDefault, CategoryDefault, BookDefault, \
    BookIn, BookOut

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/books", response_model=List[BookOut])
def books_list(session=Depends(get_session)):
    return session.exec(select(Book)).all()


@app.get("/books/{book_id}", response_model=BookOut)
def books_get(book_id: int, session=Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books", response_model=BookOut)
def books_create(book: BookIn, session=Depends(get_session)):
    book = Book.model_validate(book)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@app.delete("/books/{book_id}", response_model=dict)
def book_delete(book_id: int, session=Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"message": "Book deleted successfully"}


@app.patch("/books/{book_id}")
def book_update(book_id: int, book: BookIn, session=Depends(get_session)):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)
    session.add(db_book)
    session.commit()


@app.get("/authors")
def authors_list(session: Session = Depends(get_session)) -> List[Author]:
    authors = session.exec(select(Author)).all()
    return authors


@app.get("/authors/{author_id}")
def author_get(author_id: int, session: Session = Depends(get_session)) -> Author:
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors")
def author_create(author: AuthorDefault, session: Session = Depends(get_session)) -> Author:
    author = Author.model_validate(author)
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@app.patch("/authors/{author_id}")
def author_update(author_id: int, updated_author: AuthorDefault, session: Session = Depends(get_session)) -> Author:
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    for key, value in updated_author.model_dump(exclude_unset=True).items():
        setattr(author, key, value)
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@app.delete("/authors/{author_id}")
def author_delete(author_id: int, session: Session = Depends(get_session)) -> TypedDict("Response", {"message": str}):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    session.delete(author)
    session.commit()
    return {"message": "Author deleted successfully"}


@app.get("/categories", response_model=List[Category])
def categories_list(session=Depends(get_session)):
    return session.exec(select(Category)).all()


@app.get("/categories/{category_id}", response_model=Category)
def category_get(category_id: int, session=Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.post("/categories", response_model=Category)
def category_create(category: CategoryDefault, session=Depends(get_session)):
    category = Category.model_validate(category)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@app.delete("/categories/{category_id}", response_model=dict)
def category_delete(category_id: int, session=Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"message": "Category deleted successfully"}


@app.patch("/categories/{category_id}", response_model=Category)
def category_update(category_id: int, category: Category, session=Depends(get_session)):
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in category.model_dump(exclude_unset=True).items():
        setattr(db_category, key, value)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@app.get("/books/{book_id}/categories", response_model=List[Category])
def book_categories_list(book_id: int, session=Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return [book_category for book_category in book.categories]


@app.post("/books/{book_id}/categories/{category_id}", response_model=Category)
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
    return category


@app.delete("/books/{book_id}/categories/{category_id}", response_model=dict)
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
