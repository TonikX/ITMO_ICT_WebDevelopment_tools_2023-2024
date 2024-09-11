from fastapi import APIRouter, HTTPException, Depends
from typing import List

from sqlmodel import Session, select

from endpoints.user_endpoints import auth_handler
from students.K33391.Volgin_Leonid.Lab_1.lab.db import session, get_session
from students.K33391.Volgin_Leonid.Lab_1.lab.models.main_models import Author, Author_Default, Publisher_Default, \
    Publisher, Book, Book_Default, WishList, WishList_Default, Acception, Publisher_Submodel

main_router = APIRouter()


@main_router.get("/authors/{author_id}")
def get_author(author_id: int):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@main_router.post("/authors")
def create_author(def_author: Author_Default,):
    author = Author.model_validate(def_author)
    session.add(author)
    session.commit()
    session.refresh(author)
    return {"status": 200, "data": author}

@main_router.get("/authors_list")
def authors_list(session=Depends(get_session)) -> List[Author]:
    return session.exec(select(Author)).all()

@main_router.delete("/authors/delete/{author_id}")
def author_delete(author_id: int, session=Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    session.delete(author)
    session.commit()
    return {"ok": True}

@main_router.patch("/authors/{author_id}")
def author_update(author_id: int, author: Author_Default, session=Depends(get_session)) -> Author_Default:
    db_author = session.get(Author, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    author_data = author.model_dump(exclude_unset=True)
    for key, value in author_data.items():
        setattr(db_author, key, value)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author



@main_router.get("/publishers/{publisher_id}",response_model=Publisher_Submodel)
def get_publisher(publisher_id: int):
    publisher = session.get(Publisher, publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return publisher

@main_router.post("/publishers")
def create_publisher(def_publisher: Publisher_Default,):
    publisher = Publisher.model_validate(def_publisher)
    session.add(publisher)
    session.commit()
    session.refresh(publisher)
    return {"status": 200, "data": publisher}

@main_router.get("/publishers_list")
def publishers_list(session=Depends(get_session)) -> List[Publisher]:
    return session.exec(select(Publisher)).all()

@main_router.delete("/publishers/delete/{publisher_id}")
def publisher_delete(publisher_id: int, session=Depends(get_session)):
    publisher = session.get(Publisher, publisher_id)
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    session.delete(publisher)
    session.commit()
    return {"ok": True}

@main_router.patch("/publishers/{publisher_id}")
def publisher_update(publisher_id: int, publisher: Publisher_Default, session=Depends(get_session)) -> Publisher_Default:
    db_publisher = session.get(Publisher, publisher_id)
    if not db_publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    publisher_data = publisher.model_dump(exclude_unset=True)
    for key, value in publisher_data.items():
        setattr(db_publisher, key, value)
    session.add(db_publisher)
    session.commit()
    session.refresh(db_publisher)
    return db_publisher


@main_router.get("/books/{book_id}")
def get_book(book_id: int):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@main_router.post("/books")
def create_book(def_book: Book_Default,user=Depends(auth_handler.get_current_user)):
    book = Book(name=def_book.name, description=def_book.description, user_id=user.id)
    session.add(book)
    session.commit()
    session.refresh(book)
    return {"status": 200, "data": book}

@main_router.get("/books_list")
def books_list(session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> List[Book]:
    return session.query(Book).filter(Book.user_id == user.id).all()


@main_router.delete("/books/delete/{book_id}")
def book_delete(book_id: int, session=Depends(get_session),user=Depends(auth_handler.get_current_user)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.user_id == user.id:
        session.delete(book)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail="You have no permission for doing this")
    return {"ok": True}

@main_router.post("/wishlists")
def make_a_wish(wishlist: WishList_Default, user=Depends(auth_handler.get_current_user)):
    book = session.get(Book, wishlist.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    wish = WishList(book_id=wishlist.book_id, user_id=user.id)
    session.add(wish)
    session.commit()
    session.refresh(wish)
    return {"status": 200, "data": wish}

@main_router.delete("/wishlists/delete/{book_id}")
def wish_delete(book_id: int, session=Depends(get_session),user=Depends(auth_handler.get_current_user)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    wish = session.query(WishList).filter(WishList.book_id == book_id, WishList.user_id == user.id).first()
    if not wish:
        raise HTTPException(status_code=404, detail="Wish not found")
    session.delete(wish)
    session.commit()
    return {"ok": True}

@main_router.put("/wishlists/accept/{book_id}")
def wish_accept(book_id: int, acception: Acception, session=Depends(get_session),user=Depends(auth_handler.get_current_user)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    wish = session.query(WishList).filter(WishList.book_id == book_id, WishList.user_id == user.id).first()
    if not wish:
        raise HTTPException(status_code=404, detail="Wish not found")

    for key, value in acception.dict(exclude_unset=True).items():
        setattr(wish, key, value)
    session.add(wish)
    session.commit()
    session.refresh(wish)
    return {"ok": True}

@main_router.get("/books_list")
def wishs_list(session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> List[WishList]:
    return session.query(WishList).filter(WishList.user_id == user.id).all()