import string
from typing import List

from fastapi import HTTPException, Depends, APIRouter
from sqlmodel import select, Session

from auth.auth import AuthService
from connection import get_session
from models import Book, User, BookCopy, UserOut, UserIn, UserLogin, UserPassword

router = APIRouter(prefix="/users", tags=["Users"])
auth_service = AuthService()


@router.post("/crud", response_model=UserOut)
def create_user(user: UserIn, session=Depends(get_session)):
    user = User.model_validate(user)
    # print("*************************************")
    session.add(user)
    # print(user)
    session.commit()
    session.refresh(user)
    return user


# Get all users
@router.get("/crud", response_model=List[UserOut])
def get_all_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()


@router.get("/crud/{user_id}", response_model=UserOut)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Update user
@router.put("/crud/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserIn, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# Delete user
@router.delete("/crud/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}


@router.post("/{user_id}/book/{book_id}", response_model=UserOut)
def create_book_copy(book_id: int, user_id: int, session=Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    book_copy = BookCopy(book_id=book_id, user_id=user_id)
    session.add(book_copy)
    session.commit()
    session.refresh(book_copy)
    return user


@router.delete("/{user_id}/book/{book_id}", response_model=dict)
def delete_book_copy(book_id: int, user_id: int, session=Depends(get_session)):
    book_copy = session.exec(
        select(BookCopy)
        .where(BookCopy.book_id == book_id)
        .where(BookCopy.user_id == user_id)
    ).first()
    if not book_copy:
        raise HTTPException(status_code=404, detail=f"User {user_id} dont have book {book_id}")
    session.delete(book_copy)
    session.commit()
    return {"message": "Book copy deleted successfully"}


@router.get('/profile')
def fetch_current_user(active_user: dict = Depends(auth_service.get_active_user)) -> dict:
    return active_user


@router.patch('/profile/update-password')
def update_password(pwd_data: UserPassword, active_user: User = Depends(auth_service.get_active_user),
                    db: Session = Depends(get_session)):
    if not auth_service.verify_password(pwd_data.old_password, active_user.password):
        raise HTTPException(status_code=400, detail="Incorrect current password")

    new_hashed_password = auth_service.hash_password(pwd_data.new_password)
    active_user.password = new_hashed_password
    db.add(active_user)
    db.commit()

    return {"message": "Password successfully updated"}


@router.post('/authenticate')
def authenticate(login_data: UserLogin, db: Session = Depends(get_session)):
    user_found = db.exec(select(User).where(User.username == login_data.username)).first()
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid login data')
    verified = auth_service.verify_password(login_data.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid login data')
    token = auth_service.create_token(user_found.username)
    return {'token': token}


@router.post('/register')
def register(new_user_data: UserIn, db: Session = Depends(get_session)):
    users = db.exec(select(User)).all()
    if any(x.username == new_user_data.username for x in users):
        raise HTTPException(status_code=400, detail='Username is already in use')
    if any(x.email == new_user_data.email for x in users):
        raise HTTPException(status_code=400, detail='Email is already in use')
    hashed_pwd = auth_service.hash_password(new_user_data.password)
    user = User(username=new_user_data.username, password=hashed_pwd, email=new_user_data.email)
    db.add(user)
    db.commit()

    return {"status": 201, "message": "User account successfully created"}
