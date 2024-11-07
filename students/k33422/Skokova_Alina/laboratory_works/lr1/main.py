from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select, join
from typing import List
from typing_extensions import TypedDict

from connection import init_db, get_session
from models import *
from auth import AuthHandler

app = FastAPI()
auth_handler = AuthHandler()

@app.on_event("startup")
def on_startup():
    init_db()

# API Book

@app.post("/book", tags=['book'])
def book_create(book: BookDefault, session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> TypedDict('Response', {"status": int, "data": Book}):
    db_library = session.get(Library, book.library_id)
    if not db_library:
        raise HTTPException(status_code=404, detail="Library not found")
    if db_library.user_id != user.user_id:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    book = Book.model_validate(book)
    session.add(book)
    session.commit()
    session.refresh(book)
    return {"status": 200, "data": book}

@app.get("/books_search", response_model=List[BookLibraries], tags=['book'])
def books_search(name: Optional[str] = None, author: Optional[str] = None, genre: Optional[str] = None,
                condition: Optional[ConditionType]=None, session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> List[Book]:
    books = select(Book)
    if name:
        books = books.where(Book.book_name == name)
    if author:
        books = books.where(Book.book_author == author)
    if condition:
        books = books.where(Book.book_condition == condition)
    if genre:
        books = books.where(Book.genres.any(genre_name=genre))
    return session.exec(books).all()

@app.get("/books_list", response_model=List[BookLibraries], tags=['book'])
def books_list(session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> List[Book]:
    return session.exec(select(Book)).all()

@app.get("/books_list/user/me", response_model=List[BookLibraries], tags=['book'])
def books_list_user(session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> List[Book]:
    return session.exec(select(Book).select_from(join(Book,Library)).where(Library.user_id == user.user_id)).all()

@app.get("/book/{id_book}", response_model=BookLibraries, tags=['book'])
def book_get(id_book: int, session=Depends(get_session), user=Depends(auth_handler.get_current_user))-> Book:
    db_book = session.get(Book, id_book)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.patch("/book{id_book}", tags=['book'])
def book_update(id_book: int, book: BookDefault, session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> BookDefault:
    db_book = session.get(Book, id_book)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_book.library.user_id != user.user_id:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    book_data = book.model_dump(exclude_unset=True) 
    for key, value in book_data.items():
        setattr(db_book, key, value)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@app.delete("/book/delete{id_book}", tags=['book'])
def book_delete(id_book: int, session=Depends(get_session), user=Depends(auth_handler.get_current_user)):
    db_book = session.get(Book, id_book)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_book.library.user_id != user.user_id:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    session.delete(db_book)
    session.commit()
    return {"ok": True}

# API Library

@app.get("/libraries_list", response_model=List[LibraryOutput], tags=['library'])
def libraries_list(session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> List[Library]:
    return session.exec(select(Library)).all()

@app.get("/libraries_list/user/me", response_model=List[LibraryOutput], tags=['library'])
def libraries_list_user(session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> List[Library]:
    return session.exec(select(Library).where(Library.user_id == user.user_id)).all()

@app.get("/library/{id_library}", response_model=LibraryOutput, tags=['library'])
def library_get(id_library: int, session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> Library:
    db_library = session.get(Library, id_library)
    if not db_library:
        raise HTTPException(status_code=404, detail="Library not found")
    return db_library

@app.post("/library", tags=['library'])
def library_create(library: LibraryInput, session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> TypedDict('Response', {"status": int, "data": Library}):
    lib = LibraryDefault(library_name=library.library_name, user_id=user.user_id)
    library = Library.model_validate(lib)
    session.add(library)
    session.commit()
    session.refresh(library)
    return {"status": 200, "data": library}

@app.patch("/library{id_library}", tags=['library'])
def library_update(id_library: int, library: LibraryDefault, session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> LibraryDefault:
    db_library = session.get(Library, id_library)
    if not db_library:
        raise HTTPException(status_code=404, detail="Library not found")
    if db_library.user_id != user.user_id:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    library_data = library.model_dump(exclude_unset=True) 
    for key, value in library_data.items():
        setattr(db_library, key, value)
    session.add(db_library)
    session.commit()
    session.refresh(db_library)
    return db_library

@app.delete("/library/delete{id_library}", tags=['library'])
def library_delete(id_library: int, session=Depends(get_session), user=Depends(auth_handler.get_current_user)):
    db_library = session.get(Library, id_library)
    if not db_library:
        raise HTTPException(status_code=404, detail="Library not found")
    if db_library.user_id != user.user_id:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    session.delete(db_library)
    session.commit()
    return {"ok": True}


# API User

@app.post('/registration', tags=['user'])
def register(user: UserInput, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": User}):
    users = session.exec(select(User)).all()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_pwd = auth_handler.get_password_hash(user.password)
    u = UserPassword(username=user.username, password=hashed_pwd, email=user.email)
    us = User.model_validate(u)
    session.add(us)
    session.commit()
    session.refresh(us)
    return {"status": 200, "data": us}

@app.post('/login', tags=['user'])
def login(user: UserLogin, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "token": str}):
    user_found = session.exec(select(User).where(User.username == user.username)).first()
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user_found.username)
    return {"status": 200, "token": token}

@app.get('/users/me', tags=['user'])
def get_current_user(user: User = Depends(auth_handler.get_current_user), session=Depends(get_session)) -> User:
    return user

@app.get('/users_list', response_model=List[UserOutput], tags=['user'])
def users_list(user: User = Depends(auth_handler.get_current_user), session=Depends(get_session)) -> List[User]:
    return session.exec(select(User)).all()

@app.patch("/change_password", tags=['user'])
def change_password(password_new: str, user: User = Depends(auth_handler.get_current_user), session=Depends(get_session)) -> User:
    hashed_pwd = auth_handler.get_password_hash(password_new)
    setattr(user, 'password', hashed_pwd)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# API Request

@app.get("/requests_list", tags=['request'])
def requests_list(session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> List[Request]:
    return session.exec(select(Request)).all()

@app.get("/requests_to_me", tags=['request'])
def requests_list_to_me(session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> List[Request]:
    return session.exec(select(Request).select_from(join(Request,select(Book).select_from(join(Book,Library)).where(Library.user_id == user.user_id)))).all()

@app.get("/requests_from_me", tags=['request'])
def requests_list_from_me(session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> List[Request]:
    return session.exec(select(Request).where(Request.user_id == user.user_id)).all()

# @app.get("/request/{id_request}", tags=['request'])
# def request_get(id_request: int, session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> Request:
#     db_request = session.get(Request, id_request)
#     if not db_request:
#         raise HTTPException(status_code=404, detail="Request not found")
#     return db_request

@app.post("/request", tags=['request'])
def request_create(request: RequestDefault, session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> TypedDict('Response', {"status": int, "data": Request}):
    request = Request.model_validate(request)
    session.add(request)
    session.commit()
    session.refresh(request)
    return {"status": 200, "data": request}

@app.patch("/request{id_request}", tags=['request'])
def request_update(id_request: int, request: RequestStatus, session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> RequestStatus:
    db_request = session.get(Request, id_request)
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    db_book = session.get(Book, db_request.book_id)
    if db_book.library.user_id != user.user_id:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    request_data = request.model_dump(exclude_unset=True) 
    for key, value in request_data.items():
        setattr(db_request, key, value)
    session.add(db_request)
    session.commit()
    session.refresh(db_request)
    return db_request

@app.delete("/request/delete{id_request}", tags=['request'])
def request_delete(id_request: int, session=Depends(get_session), user=Depends(auth_handler.get_current_user)):
    db_request = session.get(Request, id_request)
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    if db_request.user_id != user.user_id:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    session.delete(db_request)
    session.commit()
    return {"ok": True}

# API BookGenreLink

@app.get("/book_genres_list", tags=['book_genre'])
def book_genres_list(session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> List[BookGenreLink]:
    return session.exec(select(BookGenreLink)).all()

@app.get("/book_genre_search", tags=['book_genre'])
def book_genre_search(genre_id: Optional[int] = None, book_genre_degree: Optional[DegreeType] = None, 
                    session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> List[BookGenreLink]:
    book_genre_links = select(BookGenreLink)
    if genre_id:
        book_genre_links = book_genre_links.where(BookGenreLink.genre_id == genre_id)
    if book_genre_degree:
        book_genre_links = book_genre_links.where(BookGenreLink.book_genre_degree == book_genre_degree)
    return session.exec(book_genre_links).all()

@app.post("/book_genre", tags=['book_genre'])
def book_genre_create(book_genre: BookGenreLinkDefault, session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> TypedDict('Response', {"status": int, "data": BookGenreLink}):
    db_genre = session.get(Genre, book_genre.genre_id)
    db_book = session.get(Book, book_genre.book_id)
    if not db_genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_book.library.user_id != user.user_id:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    book_genre = BookGenreLink.model_validate(book_genre)
    session.add(book_genre)
    session.commit()
    session.refresh(book_genre)
    return {"status": 200, "data": book_genre}

@app.patch("/book_genre/{id_book_genre}", tags=['book_genre'])
def book_genre_update(id_book_genre: int, book_genre: BookGenreLinkDefault, session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> BookGenreLinkDefault:
    db_book_genre = session.get(BookGenreLink, id_book_genre)
    if not db_book_genre:
        raise HTTPException(status_code=404, detail="BookGenreLink not found")
    db_book = session.get(Book, db_book_genre.book_id)
    if db_book.library.user_id != user.user_id:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    book_genre_data = book_genre.model_dump(exclude_unset=True) 
    for key, value in book_genre_data.items():
        setattr(db_book_genre, key, value)
    session.add(db_book_genre)
    session.commit()
    session.refresh(db_book_genre)
    return db_book_genre

@app.delete("/book_genre/delete{id_book_genre}", tags=['book_genre'])
def book_genre_delete(id_book_genre: int, session=Depends(get_session), user=Depends(auth_handler.get_current_user)):
    db_book_genre = session.get(BookGenreLink, id_book_genre)
    if not db_book_genre:
        raise HTTPException(status_code=404, detail="BookGenreLink not found")
    db_book = session.get(Book, db_book_genre.book_id)
    if db_book.library.user_id != user.user_id:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    session.delete(db_book_genre)
    session.commit()
    return {"ok": True}

# API Genre

@app.get("/genres_list", response_model=List[GenreBooks], tags=['genre'])
def genres_list(session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> List[Genre]:
    return session.exec(select(Genre)).all()

# @app.get("/genre/{id_genre}", response_model=GenreBooks, tags=['genre'])
# def genre_get(id_genre: int, session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> Genre:
#     db_genre = session.get(Genre, id_genre)
#     if not db_genre:
#         raise HTTPException(status_code=404, detail="Genre not found")
#     return db_genre

@app.post("/genre", tags=['genre'])
def genre_create(genre: GenreDefault, session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> TypedDict('Response', {"status": int, "data": Genre}):
    genre = Genre.model_validate(genre)
    session.add(genre)
    session.commit()
    session.refresh(genre)
    return {"status": 200, "data": genre}

# @app.patch("/genre{id_genre}", tags=['genre'])
# def genre_update(id_genre: int, genre: GenreDefault, session=Depends(get_session), user=Depends(auth_handler.get_current_user)) -> GenreDefault:
#     db_genre = session.get(Genre, id_genre)
#     if not db_genre:
#         raise HTTPException(status_code=404, detail="Genre not found")
#     genre_data = genre.model_dump(exclude_unset=True) 
#     for key, value in genre_data.items():
#         setattr(db_genre, key, value)
#     session.add(db_genre)
#     session.commit()
#     session.refresh(db_genre)
#     return db_genre

# @app.delete("/genre/delete{id_genre}", tags=['genre'])
# def genre_delete(id_genre: int, session=Depends(get_session), user=Depends(auth_handler.get_current_user)):
#     db_genre = session.get(Genre, id_genre)
#     if not db_genre:
#         raise HTTPException(status_code=404, detail="Genre not found")
#     session.delete(db_genre)
#     session.commit()
#     return {"ok": True}
