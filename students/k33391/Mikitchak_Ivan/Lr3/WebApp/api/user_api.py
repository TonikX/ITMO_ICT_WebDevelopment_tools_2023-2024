from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from models import(
    User,
    UserUpdateEmailForm,
    UserUpdatePasswordForm,
    UserCreateForm,
    UserDeleteForm,
    UserSerialized,
    UserUpdateForm
    )
from connection import get_session
from utilities import get_user_by_token, hash_password, verify_password

from dependencies import oauth2_scheme


router = APIRouter()


# Create a new user (register)
@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(request: UserCreateForm,
                session: Session = Depends(get_session)) -> UserSerialized:
    existing_user = session.exec(select(User).where(User.email == request.email)).one_or_none()
    if existing_user is not None:
        raise HTTPException(status_code=409, detail="Email already taken.")
    
    hashed_password = hash_password(request.password)
    user = User(email=request.email,
                hashed_password=hashed_password,
                first_name=request.first_name,
                last_name=request.last_name)

    session.add(user)
    session.commit()
    session.refresh(user)

    return UserSerialized(id=user.id,
                          email=user.email,
                          first_name=request.first_name,
                          last_name=request.last_name)


# Read users (search)
@router.get("/users")
def read_users(keywords: Optional[str] = None,
               offset: int = Query(0, ge=0),
               limit: int = Query(10, gt=0, le=100),
               token: Optional[str] = Depends(oauth2_scheme),
               session: Session = Depends(get_session)) -> List[UserSerialized]:
    get_user_by_token(token, session)
    
    query = select(User)
    if keywords:
        query = query.where((User.email.ilike(f"%{keywords}%")) |
                            (User.first_name.ilike(f"%{keywords}%")) |
                            (User.last_name.ilike(f"%{keywords}%")))
    
    users = session.exec(query.offset(offset).limit(limit)).all()
    print(users)
    
    return [UserSerialized(id=user.id,
                           email=user.email,
                           first_name=user.first_name,
                           last_name=user.last_name) for user in users]


# Read my user
@router.get("/users/me")
def retrieve_my_user(token: Optional[str] = Depends(oauth2_scheme),
                     session: Session = Depends(get_session)) -> UserSerialized:
    user = get_user_by_token(token, session)
    
    return UserSerialized(id=user.id,
                          email=user.email,
                          first_name=user.first_name,
                          last_name=user.last_name)


# Update my email
@router.post("/users/me/update_email")
def update_my_user_email(request: UserUpdateEmailForm,
                         token: Optional[str] = Depends(oauth2_scheme),
                         session: Session = Depends(get_session)) -> UserSerialized:
    user = get_user_by_token(token, session)
    
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Wrong password.")

    existing_user = session.exec(select(User).where(User.email == request.email)).one_or_none()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already taken.")

    user.email = request.email
    
    session.add(user)
    session.commit()
    session.refresh(user)

    return UserSerialized(id=user.id,
                          email=user.email,
                          first_name=user.first_name,
                          last_name=user.last_name)


# Update my password
@router.post("/users/me/update_password")
def update_my_user_password(request: UserUpdatePasswordForm,
                            token: Optional[str] = Depends(oauth2_scheme),
                            session: Session = Depends(get_session)) -> UserSerialized:
    user = get_user_by_token(token, session)
    
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Wrong password.")

    user.hashed_password = hash_password(request.new_password)
    
    session.add(user)
    session.commit()
    session.refresh(user)

    return UserSerialized(id=user.id,
                        email=user.email,
                        first_name=user.first_name,
                        last_name=user.last_name)


# Update my user (all fields except email and password)
@router.put("/users/me")
def update_my_user(request: UserUpdateForm,
                   token: Optional[str] = Depends(oauth2_scheme),
                   session: Session = Depends(get_session)) -> UserSerialized:
    user = get_user_by_token(token, session)
    
    if request.first_name is not None:
        user.first_name = request.first_name
    if request.last_name is not None:
        user.last_name = request.last_name

    session.add(user)
    session.commit()
    session.refresh(user)
    
    return UserSerialized(id=user.id,
                          email=user.email,
                          first_name=user.first_name,
                          last_name=user.last_name)


# Delete my user
@router.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_user(request: UserDeleteForm,
                   token: Optional[str] = Depends(oauth2_scheme),
                   session: Session = Depends(get_session)):
    user = get_user_by_token(token, session)
    
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Wrong password.")
    
    session.delete(user)
    session.commit()


# Read a user
@router.get("/users/{user_id}")
def read_user(user_id: int,
              token: Optional[str] = Depends(oauth2_scheme),
              session: Session = Depends(get_session)) -> UserSerialized:
    get_user_by_token(token, session)
    
    user = session.exec(select(User).where(User.id == user_id)).one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    
    return UserSerialized(id=user.id,
                          email=user.email,
                          first_name=user.first_name,
                          last_name=user.last_name)
