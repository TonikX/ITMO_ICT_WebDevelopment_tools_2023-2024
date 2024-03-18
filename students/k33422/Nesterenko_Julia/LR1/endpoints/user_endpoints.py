from fastapi import APIRouter, Depends, HTTPException
from typing import List
from typing_extensions import TypedDict
from sqlmodel import select

from models.user_models import * 
from connection import *
from auth import AuthHandler


user_router = APIRouter()
auth_handler = AuthHandler()


# all users
@user_router.get("/user/all", tags=['Users'])
def user_list(session=Depends(get_session)) -> List[UserDefault]:
    users = session.exec(select(User)).all()
    user_models = [user.model_dump(exclude={'password'}) for user in users]
    return [UserDefault.model_validate(user_model) for user_model in user_models]


# current user
@user_router.get("/user/me", tags=['Users'])
def user_me(session=Depends(get_session), 
            current=Depends(auth_handler.current_user)) -> UserDefault:
    user = session.get(User, current.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_model = user.model_dump(exclude={'password'})
    return UserDefault.model_validate(user_model)


# change current user password
@user_router.patch("/user/me/pwd", tags=['Users'])
def user_pwd(user_pwd: UserPwd, session=Depends(get_session), 
            current=Depends(auth_handler.current_user)) -> TypedDict('Response', {"status": int,
                                                                                  "message": str}):
    found_user = session.get(User, current.id)
    if not found_user:
        raise HTTPException(status_code=404, detail="User not found")
    verified = auth_handler.verify(user_pwd.old_password, found_user.password)
    if not verified:
        raise HTTPException(status_code=400, detail="Invalid old password")
    hashed_pwd = auth_handler.get_hash(user_pwd.new_password)
    found_user.password = hashed_pwd
    session.add(found_user)
    session.commit()
    session.refresh(found_user)
    return {"status": 200, "message": "password changed successfully"}


# one user
@user_router.get("/user/{user_id}", tags=['Users'])
def user_one(user_id: int, session=Depends(get_session)) -> UserDefault:
    #return session.exec(select(User).where(User.id == user_id)).first()
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_model = user.model_dump(exclude={'password'})
    return UserDefault.model_validate(user_model)


# register user
@user_router.post("/user/register", tags=['Users'])
def user_create(user_input: UserInput, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                           "data": User}):
    user_data = user_input.model_dump(exclude={'password2'}, exclude_unset=True)
    hashed_pwd = auth_handler.get_hash(user_data.get('password'))
    user_data['password'] = hashed_pwd
    user = User.model_validate(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"status": 200, "data": user}


# login user
@user_router.post("/user/login", tags=['Users'])
def user_login(user_login: UserLogin, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                           "token": str}):
    user_data = user_login.model_dump(exclude_unset=True)
    found_user = session.exec(select(User).where(User.username == user_data.get('username'))).first()
    if not found_user:
        raise HTTPException(status_code=404, detail="User with this username doesn't exist")
    verified = auth_handler.verify(user_data.get('password'), found_user.password)
    if not verified:
        raise HTTPException(status_code=400, detail="Invalid password")
    token = auth_handler.encode_token(found_user.id)
    return {"status": 200, "token": token}


# delete user
@user_router.delete("/user/delete/{user_id}", tags=['Users'])
def user_delete(user_id: int, 
                session=Depends(get_session), 
                current=Depends(auth_handler.current_user)) -> TypedDict('Response', {"status": int,
                                                                                      "message": str}):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not (user_id == current.id or current.is_admin):
        raise HTTPException(status_code=403, detail="Forbidden action")
    session.delete(user)
    session.commit()
    return {"status": 201, "message": f"deleted user with id {user_id}"}


# update user
@user_router.patch("/user/edit/{user_id}", tags=['Users'])
def user_update(user_id: int, user: UserDefault, 
                session=Depends(get_session), 
                current=Depends(auth_handler.current_user)) -> UserDefault:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not (user_id == current.id or current.is_admin):
        raise HTTPException(status_code=403, detail="Forbidden action")
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    user_model = db_user.model_dump(exclude={'password'})
    return UserDefault.model_validate(user_model)