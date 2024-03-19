from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import schemas
import crud
from database import SessionLocal
import security

router = APIRouter()

# Функция для получения экземпляра базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Регистрация пользователя
@router.post("/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

# Авторизация пользователя и генерация JWT-токена
@router.post("/login/")
def login_user(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db=db, email=user_credentials.email, password=user_credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Получение информации о текущем пользователе
@router.get("/user/", response_model=schemas.User)
def get_current_user(current_user: schemas.User = Depends(security.get_current_user)):
    return current_user

# Получение списка пользователей
@router.get("/users/", response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

# Смена пароля текущего пользователя
@router.put("/user/change-password/")
def change_password(new_password: schemas.UserPasswordChange, current_user: schemas.User = Depends(security.get_current_user), db: Session = Depends(get_db)):
    return crud.change_password(db=db, user=current_user, new_password=new_password)
