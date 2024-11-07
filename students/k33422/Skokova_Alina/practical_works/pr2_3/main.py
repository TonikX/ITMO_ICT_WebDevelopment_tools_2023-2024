from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select
from typing import List
from typing_extensions import TypedDict

from connection import init_db, get_session
from models import *

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

# API Book

@app.post("/book")
def book_create(book: BookDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Book}):
    book = Book.model_validate(book)
    session.add(book)
    session.commit()
    session.refresh(book)
    return {"status": 200, "data": book}

@app.get("/books_list", response_model=List[BookLibraries])
def books_list(session=Depends(get_session)) -> List[Book]:
    return session.exec(select(Book)).all()

@app.get("/book/{id_book}", response_model=BookLibraries)
def book_get(id_book: int, session=Depends(get_session))-> Book:
    db_book = session.get(Book, id_book)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.patch("/book{id_book}")
def book_update(id_book: int, book: BookDefault, session=Depends(get_session)) -> BookDefault:
    db_book = session.get(Book, id_book)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    book_data = book.model_dump(exclude_unset=True) #only the data that was set (sent in the request), omitting default values
    for key, value in book_data.items():
        setattr(db_book, key, value)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@app.delete("/book/delete{id_book}")
def book_delete(id_book: int, session=Depends(get_session)):
    db_book = session.get(Book, id_book)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(db_book)
    session.commit()
    return {"ok": True}

# API Library

@app.get("/libraries_list", response_model=List[LibraryUsers])
def libraries_list(session=Depends(get_session)) -> List[Library]:
    return session.exec(select(Library)).all()

@app.get("/library/{id_library}", response_model=LibraryUsers)
def library_get(id_library: int, session=Depends(get_session)) -> Library:
    db_library = session.get(Library, id_library)
    if not db_library:
        raise HTTPException(status_code=404, detail="Library not found")
    return db_library

@app.post("/library")
def library_create(library: LibraryDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Library}):
    library = Library.model_validate(library)
    session.add(library)
    session.commit()
    session.refresh(library)
    return {"status": 200, "data": library}

@app.patch("/library{id_library}")
def library_update(id_library: int, library: LibraryDefault, session=Depends(get_session)) -> LibraryDefault:
    db_library = session.get(Library, id_library)
    if not db_library:
        raise HTTPException(status_code=404, detail="Library not found")
    library_data = library.model_dump(exclude_unset=True) #only the data that was set (sent in the request), omitting default values
    for key, value in library_data.items():
        setattr(db_library, key, value)
    session.add(db_library)
    session.commit()
    session.refresh(db_library)
    return db_library

@app.delete("/library/delete{id_library}")
def library_delete(id_library: int, session=Depends(get_session)):
    db_library = session.get(Library, id_library)
    if not db_library:
        raise HTTPException(status_code=404, detail="Library not found")
    session.delete(db_library)
    session.commit()
    return {"ok": True}


# API User

@app.get("/users_list", response_model=List[UserBooks])
def users_list(session=Depends(get_session)) -> List[User]:
    return session.exec(select(User)).all()

@app.get("/user/{id_user}", response_model=UserBooks)
def user_get(id_user: int, session=Depends(get_session)) -> User:
    db_user = session.get(User, id_user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/user")
def user_create(user: UserDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": User}):
    user = User.model_validate(user)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"status": 200, "data": user}

@app.patch("/user{id_user}")
def user_update(id_user: int, user: UserDefault, session=Depends(get_session)) -> UserDefault:
    db_user = session.get(User, id_user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True) #only the data that was set (sent in the request), omitting default values
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.delete("/user/delete{id_user}")
def user_delete(id_user: int, session=Depends(get_session)):
    db_user = session.get(User, id_user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(db_user)
    session.commit()
    return {"ok": True}

# API Request

@app.get("/requests_list")
def requests_list(session=Depends(get_session)) -> List[Request]:
    return session.exec(select(Request)).all()

@app.get("/request/{id_request}")
def request_get(id_request: int, session=Depends(get_session)) -> Request:
    db_request = session.get(Request, id_request)
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request

@app.post("/request")
def request_create(request: RequestDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Request}):
    request = Request.model_validate(request)
    session.add(request)
    session.commit()
    session.refresh(request)
    return {"status": 200, "data": request}

@app.patch("/request{id_request}")
def request_update(id_request: int, request: RequestDefault, session=Depends(get_session)) -> RequestDefault:
    db_request = session.get(Request, id_request)
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    request_data = request.model_dump(exclude_unset=True) #only the data that was set (sent in the request), omitting default values
    for key, value in request_data.items():
        setattr(db_request, key, value)
    session.add(db_request)
    session.commit()
    session.refresh(db_request)
    return db_request

@app.delete("/request/delete{id_request}")
def request_delete(id_request: int, session=Depends(get_session)):
    db_request = session.get(Request, id_request)
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    session.delete(db_request)
    session.commit()
    return {"ok": True}