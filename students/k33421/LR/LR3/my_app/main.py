import os
from enum import Enum
from typing import Optional, List
import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, or_
from pydantic import BaseModel
import jwt
from fastapi import FastAPI, HTTPException, Depends, status
import hashlib
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import Users, Books, Readings, Genres, ReadingStatus, Review, Requests
from pydantic_models import *
from db import get_session, init_db
from celery_app import parse_url
from celery.result import AsyncResult
#import sys

#sys.path.append('../')

'''#from async3 import main as main_async, create_aiohttp_session
from threading3 import main as main_threading
from multiprocess3 import main as main_multiprocessing

import requests
from bs4 import BeautifulSoup
import psycopg2
import aiohttp
import asyncio
import asyncpg'''


class Token(BaseModel):
    access_token: str
    token_type: str


# Readings.update_forward_refs()
# Users.update_forward_refs()
# Books.update_forward_refs()


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password, hashed_password):
    return get_password_hash(plain_password) == hashed_password


def authenticate_user(username: str, hashed_password: str, session):
    user = session.exec(select(Users).where(Users.username == username)).first()
    if user and verify_password(hashed_password, user.hashed_password):  # 'password']):
        return username
    return False


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail=f"Invalid token")


def get_current_user(token: str = Depends(oauth2_scheme), session=Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = decode_token(token)
        if not username:
            raise HTTPException(status_code=401, detail="User not authorized")
        user = session.exec(select(Users).where(Users.username == username)).first()
        if username is None or user is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    return session.exec(select(Users).where(Users.username == username)).first()


app = FastAPI()


@app.get("/")
def hello():
    return "Hello, Diana!"


@app.on_event("startup")
def on_startup():
    init_db()


'''class Parsing(Enum):
    #async_parse = "async_parse"
    multiprocessing_parse = "multiprocessing_parse"
    threading_parse = "threading_parse"


@app.post("/parse")
def parse(pages: List[int], parsing: Parsing):
    try:
        if parsing == Parsing.threading_parse:
            main_threading(pages)
            return {"message": "Parsing completed"}
        elif parsing == Parsing.multiprocessing_parse:
            main_multiprocessing(pages)
            return {"message": "Parsing completed"}
        #elif parsing == Parsing.async_parse:
        #    await main_async(pages)
        #    return {"message": "Parsing completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'''


@app.post("/parse")
async def parse(url: str):
    task = parse_url.delay(url)
    result = AsyncResult(task.id)

    try:
        parsed_result = result.get()
        return {"message": "Parsing completed", "result": parsed_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/post_books/")
def create_book(book: BooksPost, current_user: User = Depends(get_current_user), session=Depends(get_session)):
    book = Books(title=book.title,
                 author=book.author,
                 genre=book.genre,
                 publisher=book.publisher,
                 year_of_publication=book.year_of_publication,
                 description=book.description,
                 owner_id=current_user.id)

    # book = Books.model_validate(book)
    session.add(book)
    session.flush()
    # session.commit()
    # session.refresh(book)
    new_reading = Readings(reader_id=current_user.id,
                           book_id=book.id,
                           status="available",
                           start_date=datetime.date.today(),
                           end_date=None
                           )
    session.add(new_reading)
    session.commit()
    session.refresh(book)

    return book


@app.get("/get_books/", response_model=List[BooksPost])
def read_books(author: Optional[str] = Query(None, title="Author", description="Filter books by author"),
               status: ReadingStatus = None,
               genre: Genres = None,
               session=Depends(get_session)):
    if status:
        statement = (
            select(Books)
                .join(Books.book_read)
                .where(Readings.status == status)
        )
    else:
        statement = select(Books)
    if author:
        statement = statement.where(Books.author.contains(author))
    if genre:
        statement = statement.where(Books.genre == genre)

    books = session.exec(statement).all()
    return books


@app.get("/books/{book_id}", response_model=BooksBase)
def get_concrete_book(book_id: int, current_user: User = Depends(get_current_user), session=Depends(get_session)):
    book = session.exec(select(Books).where(Books.id == book_id)).first()
    return book


@app.get("/books/my_library/", response_model=List[MyBooksBase])
def get_my_books(current_user: User = Depends(get_current_user), session=Depends(get_session)):
    user = session.exec(select(Users).where(Users.username == current_user.username)).first()
    books = session.exec(select(Books).where(Books.owner_id == user.id)).all()
    return books


@app.post("/post_readings/{book_id}/")
def create_reading(book_id: Optional[int], reading: ReadingPost, current_user: User = Depends(get_current_user),
                   session=Depends(get_session)):
    new_reading = Readings(reader_id=current_user.id,
                           book_id=book_id,
                           status=reading.status,
                           start_date=reading.start_date,
                           end_date=None
                           )
    session.add(new_reading)
    session.commit()
    session.refresh(new_reading)
    return new_reading


'''
@app.get("/get_readings/", response_model=List[ReadingRead])
def get_readings(status: ReadingStatus = None,
                 session=Depends(get_session)):
    statement = select(Readings)
    if status:
        statement = statement.where(Readings.status == status)
    readings = session.exec(statement).all()
    return readings
'''


@app.get("/get_my_readings/", response_model=List[ReadingRead])
def get_my_readings(status: ReadingStatus = None,
                    current_user: User = Depends(get_current_user),
                    session=Depends(get_session)):
    statement = select(Readings).where(Readings.reader_id == current_user.id)
    if status:
        statement = statement.where(Readings.status == status)
    readings = session.exec(statement).all()
    return readings


@app.put("/readings/{book_id}", response_model=ReadingRead)
def update_reading(book_id: Optional[int],
                   status: ReadingStatus,
                   end_date: Optional[date] = None,
                   current_user: User = Depends(get_current_user),
                   session: Session = Depends(get_session)):
    reading = session.exec(select(Readings).where(Readings.reader_id == current_user.id,
                                                  Readings.book_id == book_id)
                           ).first()

    if not reading:
        raise HTTPException(status_code=404, detail="Reading record not found")

    # Update the fields if provided
    if status:
        reading.status = status
    if end_date:
        reading.end_date = end_date

    session.commit()
    session.refresh(reading)

    return reading


@app.post("/post_request/{book_id}/")
def create_request(book_id: Optional[int],
                   request: BaseRequest,
                   current_user: User = Depends(get_current_user),
                   session=Depends(get_session)):
    reading = session.exec(select(Readings).where(Readings.book_id == book_id,
                                                  # Readings.end_date is None,
                                                  Readings.status == "available")).first()

    new_request = Requests(sender_id=current_user.id,
                           receiver_id=reading.reader_id,
                           book_id=book_id,
                           status="sent",
                           conditions=request.conditions,
                           response=None
                           )
    session.add(new_request)
    session.commit()
    session.refresh(new_request)
    return new_request


@app.get("/get_my_requests/", response_model=List[GetRequest])
def get_my_requests(status: RequestStatus = None,
                    sent: bool = True,
                    received: bool = True,
                    current_user: User = Depends(get_current_user),
                    session=Depends(get_session)):
    statement = select(Requests)
    if sent and received:
        statement = statement.where(
            or_(
                Requests.sender_id == current_user.id,
                Requests.receiver_id == current_user.id
            ))
    elif sent and not received:
        statement = statement.where(Requests.sender_id == current_user.id)
    elif received and not sent:
        statement = statement.where(Requests.receiver_id == current_user.id)
    if status:
        statement = statement.where(Requests.status == status)
    requests = session.exec(statement).all()
    return requests


@app.put("/requests/{book_id}", response_model=UpdateRequest)
def update_response(book_id: Optional[int],
                    status: RequestStatus = "accepted",
                    response: Optional[str] = None,
                    current_user: User = Depends(get_current_user),
                    session: Session = Depends(get_session)):
    request = session.exec(select(Requests).where(Requests.receiver_id == current_user.id,
                                                  Requests.book_id == book_id,
                                                  Requests.status == "sent")
                           ).first()

    if not request:
        raise HTTPException(status_code=404, detail="Request record not found or status isn't 'sent'")

    if status:
        request.status = status
    if response:
        request.response = response

    session.commit()
    session.refresh(response)

    return response


@app.get("/users/", response_model=List[UserBase])
def read_users(session=Depends(get_session)):
    users = session.exec(select(Users)).all()
    return users


@app.get("/user/{user_id}", response_model=UserGet)
def get_concrete_users(user_id: int,
                       country: str = None,
                       city: str = None,
                       current_user: User = Depends(get_current_user),
                       session=Depends(get_session)):
    statement = select(Users).where(Users.id == user_id)
    if city:
        statement = statement.where(Users.city == city)
    if country:
        statement = statement.where(Users.country == country)
    user = session.exec(statement).first()
    return user


@app.post("/post_review/{book_id}/")
def create_review(book_id: Optional[int],
                  review: ReviewBase,
                  current_user: User = Depends(get_current_user),
                  session=Depends(get_session)):
    if review.rating < 0 or review.rating > 10:
        raise HTTPException(status_code=404, detail="Rating should be in interval [0, 10]")

    new_review = Review(reviewer_id=current_user.id,
                        book_id=book_id,
                        rating=review.rating,
                        comment=review.comment
                        )
    session.add(new_review)
    session.commit()
    session.refresh(new_review)
    return new_review


@app.get("/books/{book_id}/reviews", response_model=List[ReviewsGet])
def read_reviews_on_book(book_id: int, session=Depends(get_session)):
    # book = session.exec(select(Books).where(Books.id == book_id)).first()
    reviews = session.exec(select(Review).where(Review.book_id == book_id))
    return reviews


@app.post("/register/")
def register(user: UsersRegistration, session=Depends(get_session)):
    user = Users.model_validate(user)
    statement = select(Users).where(Users.username == user.username)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # if user.username in session.exec(select(Users)).all().:
    #    raise HTTPException(status_code=400, detail="Username already registered")
    user.hashed_password = get_password_hash(user.hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"status": 200, "data": user}


@app.post('/token', response_model=Token)
def login_for_token(
        payload: OAuth2PasswordRequestForm = Depends(),
        session=Depends(get_session)):
    username = authenticate_user(payload.username, payload.password, session)
    if not username:
        raise HTTPException(status_code=401, detail="Incorrect username or password 1")
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/login/")
def login(user: Users, session=Depends(get_session)):
    username = authenticate_user(user.username, user.hashed_password, session)
    if not username:
        raise HTTPException(status_code=401, detail="Incorrect username or password 2")
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user), session=Depends(get_session)):
    return session.exec(select(Users).where(Users.id == current_user.id)).first()


@app.delete("/users_me/delete{user_id}")
def user_delete_my_account(user_id: int, current_user: User = Depends(get_current_user), session=Depends(get_session)):
    if user_id != current_user.id:
        raise HTTPException(status_code=401, detail="You can't delete another user")

    statement = select(Users).where(Users.id == user_id)
    results = session.exec(statement)
    user = results.one()
    session.delete(user)
    session.commit()

    return {"status": 201, "message": "deleted"}


@app.delete("/books/delete/{book_id}")
def delete_my_book(book_id: int,
                   current_user: User = Depends(get_current_user),
                   session=Depends(get_session)):
    book = session.exec(select(Books).where(Books.id == book_id)).first()
    if book.owner_id != current_user.id:
        raise HTTPException(status_code=401, detail="You can't delete book not yours")

    session.delete(book)
    session.commit()
    return {"status": 201, "message": "deleted"}


@app.delete("/reviews/{review_id}")
def delete_my_review(review_id: int,
                     current_user: User = Depends(get_current_user),
                     session=Depends(get_session)):
    reading = session.exec(select(Review).where(Review.id == review_id)).first()

    if reading.reviewer_id != current_user.id:
        raise HTTPException(status_code=401, detail="You can't delete review not yours")

    session.delete(reading)
    session.commit()
    return {"status": 201, "message": "deleted"}


@app.delete("/readings/{book_id}")
def delete_my_reading(book_id: int, current_user: User = Depends(get_current_user), session=Depends(get_session)):
    reading = session.exec(select(Readings).where(Readings.reader_id == current_user.id,
                                                  Readings.book_id == book_id)
                           ).first()
    session.delete(reading)
    session.commit()
    return {"status": 201, "message": "deleted"}
