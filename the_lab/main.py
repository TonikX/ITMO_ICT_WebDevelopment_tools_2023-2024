from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import EmailStr, constr
from typing import Optional, List
from datetime import timedelta, datetime
from sqlalchemy.orm import joinedload
import models
from auth import (
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from connection import init_db, get_session
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def main():
    return "Main page"


@app.post("/register/")
def register_user(
    username: str,
    email: EmailStr,
    password: constr(min_length=6, max_length=20),  # type: ignore
    name: str,
    surname: str,
    age: int,
    gender: models.Gender,
    profile_description: Optional[str] = None,
    session: Session = Depends(get_session),
):
    existing_user = (
        session.query(models.Reader)
        .filter((models.Reader.username == username) | (models.Reader.email == email))
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Username or email already registered"
        )

    new_reader = models.Reader(
        username=username,
        email=email,
        name=name,
        surname=surname,
        age=age,
        gender=gender,
        profile_description=profile_description,
    )
    new_reader.hash_password(password)
    session.add(new_reader)
    session.commit()

    return {"message": "User registered successfully"}


@app.post("/login/", response_model=dict)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = (
        session.query(models.Reader)
        .filter(
            (models.Reader.username == form_data.username)
            | (models.Reader.email == form_data.username)
        )
        .first()
    )
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me/", response_model=models.Reader)
def read_users_me(current_user: models.Reader = Depends(get_current_user)):
    return current_user


@app.post("/change_password/")
def change_password(
    old_password: str,
    new_password: constr(min_length=6, max_length=20),  # type: ignore
    new_password_repeat: constr(min_length=6, max_length=20),  # type: ignore
    current_user: models.Reader = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if not current_user.verify_password(old_password):
        raise HTTPException(status_code=401, detail="Old password is incorrect")

    if new_password == new_password_repeat:
        current_user.hash_password(new_password)
        session.commit()
        return {"message": "Password changed successfully"}
    else:
        raise HTTPException(status_code=400, detail="Your new passwords don't match")


@app.get("/readers/", response_model=List[models.ReaderResponse])
def get_readers(session: Session = Depends(get_session)):
    readers = session.execute(select(models.Reader)).scalars().all()
    return readers


@app.get("/readers/{reader_id}/", response_model=models.ReaderResponse)
def get_reader(reader_id: int, session: Session = Depends(get_session)):
    reader = (
        session.query(models.Reader)
        .options(
            joinedload(models.Reader.books), joinedload(models.Reader.work_experience)
        )
        .filter(models.Reader.id == reader_id)
        .first()
    )

    if not reader:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reader not found"
        )

    return models.ReaderResponse(
        id=reader.id,
        username=reader.username,
        email=reader.email,
        name=reader.name,
        surname=reader.surname,
        age=reader.age,
        gender=reader.gender,
        profile_description=reader.profile_description,
        books=[models.BookBase.from_orm(book) for book in reader.books],
        work_experience=[
            models.WorkExperienceBase.from_orm(exp) for exp in reader.work_experience
        ],
    )


@app.post("/readers/{reader_id}/add_experience/", response_model=models.WorkExperience)
def add_work_experience(
    reader_id: int,
    organization: str,
    position: str,
    start_date: datetime,
    end_date: Optional[datetime] = None,
    session: Session = Depends(get_session),
):
    reader = session.get(models.Reader, reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found.")

    new_experience = models.WorkExperience(
        organization=organization,
        position=position,
        start_date=start_date,
        end_date=end_date,
        reader_id=reader_id,
    )
    session.add(new_experience)
    session.commit()
    session.refresh(new_experience)

    return new_experience


@app.get("/readers/{reader_id}/experience/", response_model=List[models.WorkExperience])
def get_all_work_experience(reader_id: int, session: Session = Depends(get_session)):
    reader = session.get(models.Reader, reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found.")

    return reader.work_experience


@app.post("/new_book/", response_model=models.Book)
def create_book(
    name: str,
    author: str,
    publication_year: int,
    description: Optional[str] = None,
    session: Session = Depends(get_session),
):

    book = models.Book(
        name=name,
        author=author,
        publication_year=publication_year,
        description=description,
    )
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@app.get("/books/", response_model=List[models.BookResponse])
def get_books(session: Session = Depends(get_session)):
    books = session.query(models.Book).options(joinedload(models.Book.genres)).all()

    return books


@app.get("/books/{book_id}", response_model=models.BookResponse)
def get_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(models.Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")
    return book


@app.put("/change_book/{book_id}/", response_model=models.Book)
def change_book(
    book_id: int,
    description: Optional[str] = None,
    publication_year: Optional[int] = None,
    session: Session = Depends(get_session),
):
    book = session.get(models.Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    if description is not None:
        book.description = description

    if publication_year is not None:
        book.publication_year = publication_year

    session.commit()
    session.refresh(book)

    return book


@app.delete("/delete_book/{book_id}/", response_model=models.Book)
def delete_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(models.Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    session.query(models.BookOwnership).filter_by(book_id=book_id).delete()

    session.delete(book)
    session.commit()

    return book


@app.post("/new_genre/", response_model=models.Genre)
def create_genre(name: str, session: Session = Depends(get_session)):
    genre = models.Genre(name=name)
    session.add(genre)
    session.commit()
    session.refresh(genre)
    return genre


@app.get("/genres/", response_model=List[models.Genre])
def get_genres(session: Session = Depends(get_session)):
    genres = session.execute(select(models.Genre)).scalars().all()
    return genres


@app.delete("/genres/{genre_id}/", response_model=models.Genre)
def delete_genre(genre_id: int, session: Session = Depends(get_session)):
    genre = session.get(models.Genre, genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    session.delete(genre)
    session.commit()
    return genre


@app.post("/book_genre_link/", response_model=models.BookGenreLink)
def create_book_genre_link(
    genre_id: int, book_id: int, session: Session = Depends(get_session)
):
    existing_link = (
        session.query(models.BookGenreLink)
        .filter_by(book_id=book_id, genre_id=genre_id)
        .first()
    )

    if existing_link:
        raise HTTPException(status_code=400, detail="This link already exists.")

    book_genre_link = models.BookGenreLink(book_id=book_id, genre_id=genre_id)
    session.add(book_genre_link)
    session.commit()
    session.refresh(book_genre_link)

    return book_genre_link


@app.post("/new_ownership/", response_model=models.BookOwnership)
def create_ownership(
    book_id: int, owner_id: int, session: Session = Depends(get_session)
):
    book = session.get(models.Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    existing_ownership = (
        session.query(models.BookOwnership).filter_by(book_id=book_id).first()
    )
    if existing_ownership:
        raise HTTPException(
            status_code=400, detail="This book is already owned by someone."
        )

    ownership = models.BookOwnership(book_id=book_id, owner_id=owner_id)
    session.add(ownership)
    session.commit()
    session.refresh(ownership)

    return ownership


@app.delete("/book_genre_link/", response_model=models.BookGenreLink)
def delete_book_genre_link(
    genre_id: int, book_id: int, session: Session = Depends(get_session)
):
    link = (
        session.query(models.BookGenreLink)
        .filter_by(book_id=book_id, genre_id=genre_id)
        .first()
    )

    if not link:
        raise HTTPException(status_code=404, detail="Link not found.")

    session.delete(link)
    session.commit()

    return link


@app.get("/ownerships/", response_model=List[models.BookOwnershipResponse])
def get_ownerships(session: Session = Depends(get_session)):
    ownerships = session.execute(select(models.BookOwnership)).scalars().all()
    return ownerships


@app.delete("/delete_ownership/", response_model=models.BookOwnership)
def delete_ownership(
    book_id: int, owner_id: int, session: Session = Depends(get_session)
):
    ownership = (
        session.query(models.BookOwnership)
        .filter_by(book_id=book_id, owner_id=owner_id)
        .first()
    )
    if not ownership:
        raise HTTPException(status_code=404, detail="Ownership not found.")

    session.delete(ownership)
    session.commit()

    return ownership


@app.post("/new_request/", response_model=models.UserRequest)
def create_request(
    book_id: int,
    receiver_id: int,
    session: Session = Depends(get_session),
    current_user: models.User = Depends(get_current_user),
):
    book = session.get(models.Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    if not book.available:
        raise HTTPException(
            status_code=400, detail="Book is not available for exchange."
        )

    ownership = (
        session.query(models.BookOwnership)
        .filter_by(book_id=book_id, owner_id=receiver_id)
        .first()
    )
    if not ownership:
        raise HTTPException(status_code=403, detail="Person does not own this book.")

    new_request = models.UserRequest(
        book_id=book_id, sender_id=current_user.id, receiver_id=receiver_id
    )
    session.add(new_request)
    session.commit()
    session.refresh(new_request)

    book.available = False
    session.commit()

    return new_request


@app.get("/requests/", response_model=List[models.UserRequest])
def get_requests(session: Session = Depends(get_session)):
    requests = session.execute(select(models.UserRequest)).scalars().all()
    return requests


@app.post("/requests/{request_id}/approve", response_model=models.UserRequest)
def approve_request(
    request_id: int,
    current_user: models.Reader = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    request = session.get(models.UserRequest, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found.")

    if request.receiver_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the request receiver can approve this request.",
        )

    request.approve()
    session.commit()

    book = session.get(models.Book, request.book_id)
    if book:
        current_ownership = (
            session.query(models.BookOwnership).filter_by(book_id=book.id).first()
        )
        if current_ownership:
            current_ownership.owner_id = request.sender_id
            session.commit()
            book.available = True
            session.commit()

    return request


@app.post("/requests/{request_id}/reject", response_model=models.UserRequest)
def reject_request(
    request_id: int,
    current_user: models.Reader = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    request = session.get(models.UserRequest, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found.")

    if request.receiver_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Only the request receiver can reject this request."
        )

    request.reject()
    session.commit()

    book = session.get(models.Book, request.book_id)
    if book:
        book.available = True
        session.commit()

    return request
