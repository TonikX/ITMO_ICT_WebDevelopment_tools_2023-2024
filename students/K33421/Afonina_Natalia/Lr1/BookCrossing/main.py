from fastapi import FastAPI, Depends, HTTPException, status
from typing import List, Dict
from connection import init_db, get_session
from models import *
from sqlmodel import *
from typing_extensions import TypedDict

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/users_list")
def users_list(session=Depends(get_session)) -> List[UserProfile]:
    return session.exec(select(UserProfile)).all()


@app.get("/user/{user_id}")
def get_user(user_id: int, session=Depends(get_session)) -> UserProfile:
    user = session.exec(select(UserProfile).where(UserProfile.id == user_id)).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/user")
def create_user(user: UserDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                           "data": UserProfile}):
    validated_user = UserProfile.model_validate(user)
    session.add(validated_user)
    session.commit()
    session.refresh(validated_user)
    return {"status": 200, "data": validated_user}


@app.delete("/user/user{user_id}")
def delete_user(user_id: int, session=Depends(get_session)):
    user = session.get(UserProfile, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}


@app.patch("/user{user_id}")
def update_user(user_id: int, user: UserDefault, session=Depends(get_session)) -> UserDefault:
    db_user = session.get(UserProfile, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get("/author_list")
def authors_list(session=Depends(get_session)) -> List[Author]:
    return session.exec(select(Author)).all()


@app.get("/author/{author_id}")
def get_author(author_id: int, session=Depends(get_session)) -> Author:
    author = session.exec(select(Author).where(Author.id == author_id)).first()
    if author:
        return author
    else:
        raise HTTPException(status_code=404, detail="Author not found")


@app.post("/author")
def create_author(author: Author, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                          "data": Author}):
    validated_author = Author.model_validate(author)
    session.add(validated_author)
    session.commit()
    session.refresh(validated_author)
    return {"status": 200, "data": validated_author}

@app.delete("/author/author{author_id}")
def delete_author(author_id: int, session=Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(author)
    session.commit()
    return {"ok": True}

@app.get("/book_list")
def books_list(session=Depends(get_session)) -> List[Book]:
    return session.exec(select(Book)).all()


@app.get("/book/{book_id}", response_model=BooksAuthor)
def get_book(book_id: int, session=Depends(get_session)) -> Book:
    # book = session.exec(select(Book).where(Book.id == book_id)).first()
    book = session.get(Book, book_id)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@app.post("/book")
def create_book(book: BookDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                           "data": Book}):
    validated_book = Book.model_validate(book)
    session.add(validated_book)
    session.commit()
    session.refresh(validated_book)
    return {"status": 200, "data": validated_book}

# @app.put("/book/{book_id}")
# def update_book(book_id: int, book_update: Book):
#     for data in temp_bd:
#         for book_data in data.get("books", []):
#             if book_data.get("id") == book_id:
#                 book_data.update(book_update.dict())
#                 return {"message": "Book updated successfully"}
#     raise HTTPException(status_code=404, detail="Book not found")
#
#
# def get_all_book_reviews() -> List[BookReview]:
#     reviews = [review_data for data in temp_bd for review_data in data.get("book_reviews", [])]
#     return reviews
#
#
# @app.get("/book_review/{review_id}")
# def get_book_review(review_id: int) -> BookReview:
#     for data in temp_bd:
#         for review_data in data.get("book_reviews", []):
#             if review_data.get("id") == review_id:
#                 return review_data
#     raise HTTPException(status_code=404, detail="Book review not found")
#
#
# @app.post("/book_review")
# def create_book_review(review: BookReview):
#     for data in temp_bd:
#         if "book_reviews" in data:
#             data["book_reviews"].append(review.dict())
#             return review
#     raise HTTPException(status_code=404, detail="Book reviews not found")
#
#
# @app.put("/book_review/{review_id}")
# def update_book_review(review_id: int, review_update: BookReview):
#     for data in temp_bd:
#         if "book_reviews" in data:
#             for review_data in data["book_reviews"]:
#                 if review_data["id"] == review_id:
#                     review_data.update(review_update.dict())
#                     return review_update
#     raise HTTPException(status_code=404, detail="Book review not found")
#
#
# @app.delete("/book_review/{review_id}")
# def delete_book_review(review_id: int):
#     for data in temp_bd:
#         if "book_reviews" in data:
#             for review_data in data["book_reviews"]:
#                 if review_data["id"] == review_id:
#                     data["book_reviews"].remove(review_data)
#                     return {"message": "Book review deleted successfully"}
#     raise HTTPException(status_code=404, detail="Book review not found")
