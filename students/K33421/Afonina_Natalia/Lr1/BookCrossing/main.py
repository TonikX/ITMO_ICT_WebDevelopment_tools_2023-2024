from fastapi import FastAPI, Depends, HTTPException, status
from typing import List, Dict
from connection import init_db, get_session
from models import *
from sqlmodel import *
from typing_extensions import TypedDict
from sqlalchemy.orm import selectinload
from auth import Authorization
import hashlib
import datetime
import jwt
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()
auth = Authorization()


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/register")
def register(username: str, password: str, firstname: str = None, lastname: str = None,
             age: int = None, location: str = None, bio: str = None, session=Depends(get_session)):
    # Проверяем, существует ли пользователь уже
    existing_user = session.exec(select(UserProfile).where(UserProfile.username == username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Хэшируем пароль
    hashed_password = auth.get_password_hash(password)

    # Создаем запись пользователя в базе данных
    new_user = UserProfile(username=username, firstname=firstname, lastname=lastname,
                           age=age, location=location, bio=bio, password_hash=hashed_password)
    session.add(new_user)
    session.commit()

    # Создаем JWT токен
    token = auth.encode_token(new_user.id)

    # Возвращаем результат
    return {"message": "User registered successfully", "token": token}


@app.post("/login")
def login(username: str, password: str, auth: Authorization = Depends(), session=Depends(get_session)):
    try:
        # Аутентификация пользователя
        user = auth.authenticate_user(username, password, session)
        # Если аутентификация прошла успешно, создаем JWT токен
        token = auth.encode_token(user.id)
        # Возвращаем токен
        return {"token": token}
    except HTTPException as e:
        # В случае ошибки аутентификации, возбуждаем исключение с кодом и сообщением из HTTPException
        raise e


@app.put("/change_password/{username}")
def change_password(username: str, old_password: str, new_password: str, auth: Authorization = Depends(),
                    session=Depends(get_session)):
    try:
        # Аутентификация пользователя для смены пароля
        user = auth.authenticate_user(username, old_password, session)

        # Хэшируем новый пароль
        hashed_new_password = auth.get_password_hash(new_password)

        # Обновляем пароль пользователя в базе данных
        user.password_hash = hashed_new_password
        session.commit()

        return {"message": "Password changed successfully"}
    except HTTPException as e:
        # В случае ошибки аутентификации, возбуждаем исключение с кодом и сообщением из HTTPException
        raise e

@app.get("/users_list")
def users_list(session=Depends(get_session)) -> List[UserProfile]:
    return session.exec(select(UserProfile)).all()


@app.get("/user/{user_id}")
def get_user(username: str, session=Depends(get_session)) -> UserProfile:
    user = session.exec(select(UserProfile).where(UserProfile.username == username)).first()
    if user:
        return {
            "id": user.id,
            "username": user.username,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "age": user.age,
            "location": user.location,
            "bio": user.bio
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")


# @app.post("/user")
# def create_user(user: UserDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
#                                                                                            "data": UserProfile}):
#     validated_user = UserProfile.model_validate(user)
#     session.add(validated_user)
#     session.commit()
#     session.refresh(validated_user)
#     return {"status": 200, "data": validated_user}


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
def create_author(author: AuthorDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
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


@app.get("/book_list", response_model=List[BookWithAuthors])
def get_books(session=Depends(get_session)):
    books = session.exec(select(Book)).all()

    # Для каждой книги получаем связанных авторов и их идентификаторы
    books_with_authors = []
    for book in books:
        author_links = session.exec(select(AuthorBookLink).where(AuthorBookLink.book_id == book.id)).all()
        author_ids = [link.author_id for link in author_links]
        books_with_authors.append(BookWithAuthors(book=book, author_ids=author_ids))

    return books_with_authors


@app.get("/book/{book_id}")
def get_book(book_id: int, session=Depends(get_session)) -> BookWithAuthors:
    query = select(Book).where(Book.id == book_id)
    book = session.exec(query).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    author_links = session.exec(select(AuthorBookLink).where(AuthorBookLink.book_id == book_id)).all()
    author_ids = [link.author_id for link in author_links]

    return BookWithAuthors(book=book, author_ids=author_ids)


@app.post("/book", response_model=Book)
def create_book(book_data: BookWithAuthors, session=Depends(get_session)) -> Book:
    # Создаем книгу из данных запроса
    book = Book(**book_data.book.dict())
    session.add(book)
    session.commit()
    session.refresh(book)

    # Связываем книгу с каждым автором по их идентификаторам
    for author_id in book_data.author_ids:
        author_book_link = AuthorBookLink(author_id=author_id, book_id=book.id)
        session.add(author_book_link)
    session.commit()

    return book


@app.get("/user/{user_id}/library")
def get_user_library(user_id: int, session=Depends(get_session)):
    user = session.get(UserProfile, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_library = session.exec(select(UserLibrary).where(UserLibrary.user_id == user_id)).all()
    if not user_library:
        return {"message": "User library is empty"}

    # Для каждой книги получаем связанных авторов и их идентификаторы
    library_with_authors = []
    for entry in user_library:
        book = session.get(Book, entry.book_id)
        if book:
            author_links = session.exec(select(AuthorBookLink).where(AuthorBookLink.book_id == book.id)).all()
            author_ids = [link.author_id for link in author_links]
            library_with_authors.append(BookWithAuthors(book=book, author_ids=author_ids))

    return {"user": user, "library": library_with_authors}


@app.post("/user/{user_id}/add_book_to_library/{book_id}")
def add_book_to_library(user_id: int, book_id: int, session=Depends(get_session)):
    user = session.get(UserProfile, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    user_library = UserLibrary(user_id=user_id, book_id=book_id)
    session.add(user_library)
    session.commit()
    return {"message": "Book added to user's library successfully"}


@app.post("/user/{sender_id}/send_exchange_request/{receiver_id}")
def send_exchange_request(sender_id: int, receiver_id: int, offered_book_id: int, requested_book_id: int,
                          session=Depends(get_session)):
    sender = session.get(UserProfile, sender_id)
    receiver = session.get(UserProfile, receiver_id)
    offered_book = session.get(Book, offered_book_id)
    requested_book = session.get(Book, requested_book_id)

    if not sender or not receiver or not offered_book or not requested_book:
        raise HTTPException(status_code=404, detail="Sender, receiver, or book not found")

    # Проверяем, есть ли у отправителя книга в его библиотеке
    sender_library = session.exec(select(UserLibrary).where(
        (UserLibrary.user_id == sender_id) & (UserLibrary.book_id == offered_book_id))).first()
    if not sender_library:
        raise HTTPException(status_code=400, detail="Sender doesn't have the book in their library")

    # Проверяем, есть ли запрашиваемая книга у другого пользователя
    requester_library = session.exec(select(UserLibrary).where(
        (UserLibrary.user_id == receiver_id) & (UserLibrary.book_id == requested_book_id))).first()
    if not requester_library:
        raise HTTPException(status_code=400, detail="Requester doesn't have the book in their library")

    # Создаем новый запрос на обмен
    exchange_request = ExchangeRequest(
        books_offered=offered_book,
        books_requested=requested_book,
        accepted=False,
        sender_id=sender_id,
        receiver_id=receiver_id
    )
    session.add(exchange_request)
    session.commit()

    return {"message": "Exchange request sent successfully"}


@app.put("/exchange_request/{request_id}/{action}")
def respond_to_exchange_request(request_id: int, action: str, session=Depends(get_session)):
    # Проверяем действие: accept или reject
    if action not in ["accept", "reject"]:
        raise HTTPException(status_code=400, detail="Invalid action. Use 'accept' or 'reject'")

    exchange_request = session.get(ExchangeRequest, request_id)
    if not exchange_request:
        raise HTTPException(status_code=404, detail="Exchange request not found")

    if action == "accept":
        exchange_request.accepted = True
        message = "Exchange request accepted successfully"
    else:
        exchange_request.accepted = False
        message = "Exchange request rejected successfully"

    session.commit()
    return {"message": message}

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
