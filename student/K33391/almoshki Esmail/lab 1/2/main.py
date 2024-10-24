from fastapi import FastAPI, Depends
from typing import Optional, List
from typing_extensions import TypedDict
from models import BookOwners, RequestStatus, DefaultRequest, BookOwnershipResponse, RequestResponse,Request, Person,DefaultProfile, Profile, Book, BookOwnership, PersonProfile ,DefaultBook, DefaultPerson, BookResponse
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from connection import init_db, get_session

app = FastAPI()


@app.on_event('startup')
def on_startup():
    init_db()


@app.get('/')
def hello():
    return "Welcome to the finest bookcrossing app"


@app.get("/users_list", response_model=List[PersonProfile])
def users_list(session: Session = Depends(get_session)) -> List[Person]:
    return session.exec(select(Person)).all()

@app.get("/user/{name}", response_model=List[PersonProfile])
def get_user_by_name(name: str ,session: Session = Depends(get_session)) -> List[Person]:
    return session.exec(select(Person).where(Person.name == name)).all()

@app.post('/user',tags=["Post Methods"])
def create_user(user: DefaultPerson, session: Session = Depends(get_session)) -> TypedDict("Response", {"status": int , "data": Person}):
    user = Person.model_validate(user)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"status": 200 , 'data': user}

@app.post('/profile',tags=["Post Methods"])
def create_profile(profile: DefaultProfile, session: Session = Depends(get_session)) -> TypedDict("Response", {"status": int , "data": Profile}):
    profile = Profile.model_validate(profile)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return {"status": 200 , 'data': profile}

@app.get('/books', response_model= List[BookOwners])
def get_books(session: Session = Depends(get_session))-> List[BookOwners]:
    return session.exec(select(Book)).all()

@app.get("/book/{name}", response_model=List[BookOwners])
def get_book_by_title(name: str, session: Session =Depends(get_session)) -> List[BookOwners]:
    books = session.exec(select(Book).filter(Book.title.like(f"%{name}%")))
    if not books:
        return 
    return books

@app.post('/book',tags=["Post Methods"])
def create_book(book: DefaultBook, session: Session = Depends(get_session)) -> TypedDict("Response", {"status": int , "data": Book}):
    book = Book.model_validate(book)
    session.add(book)
    session.commit()
    session.refresh(book)
    return {"status": 200 , 'data': book }

# TODO  use BookOwnershipResponse and uncomment relashionships
# @app.get('/ownerships' ,response_model=BookOwnership)
# def get_ownerships(session: Session = Depends(get_session)) -> List[BookOwnership]:
#     return session.exec(select(BookOwnership)).all()



@app.post('/ownership',tags=["Post Methods"])
def create_ownership( ownership: BookOwnership, session: Session= Depends(get_session))-> TypedDict("Response", {"status": int , "data": BookOwnership}):
    ownership = BookOwnership.model_validate(ownership)
    session.add(ownership)
    session.commit()
    session.refresh(ownership)
    return { "status": 200, "data": ownership}

@app.post('/request',tags=["Post Methods"])
def create_request(request: DefaultRequest , session: Session = Depends(get_session))-> TypedDict("Response", {"status": int , "data": Request}):
    request = Request.model_validate(request)
    session.add(request)
    session.commit()
    session.refresh(request)
    return   {"status": 200 , 'data': request }

@app.get("/requests/", response_model=List[RequestResponse])
def get_requests(session: Session = Depends(get_session)):
    statement = (
        select(Request)
        .options(selectinload(Request.sender))    # Eager load the sender
        .options(selectinload(Request.receiver))  # Eager load the receiver
        .options(selectinload(Request.book))      # Eager load the book
    )
    requests = session.exec(statement).all()
    return requests

@app.get("/request/{id}", response_model=List[RequestResponse])
def get_requests(id : int, session: Session = Depends(get_session)):
    statement = (
        select(Request)
        .options(selectinload(Request.sender))    # Eager load the sender
        .options(selectinload(Request.receiver))  # Eager load the receiver
        .options(selectinload(Request.book)).where(Request.id == id)   # Eager load the book
    )
    requests = session.exec(statement)
    return requests

@app.put('/request/{id}')
def respond_to_request(id: int, response: RequestStatus, session: Session= Depends(get_session))-> TypedDict("Response", {"status": int, "data": Request}):
    request = session.get(Request, id)
    if request is None:
        return {"status": 404, "message": "Request not found"}
    request.status =  response
    session.add(request)
    session.commit()
    session.refresh(request)
    return {"status": 200 , "data": request }
