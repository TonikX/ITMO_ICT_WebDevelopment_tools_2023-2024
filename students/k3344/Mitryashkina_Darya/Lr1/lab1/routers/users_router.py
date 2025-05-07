from datetime import timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from connection import get_session
from auth_services import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user, get_password_hash, verify_password
from models import UserDefault, User
from typing_extensions import TypedDict
from base_responses import MessageResponse
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

class UserCreate(UserDefault):
    password: str

class UserResponse(TypedDict):
    status: int
    data: User

class UsersListResponse(TypedDict):
    status: int
    data: List[User]

class AccessTokenResponse(TypedDict):
    access_token: str
    token_type: str

class PasswordChange(BaseModel):
    old_password: str
    new_password: str

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)) -> AccessTokenResponse:
    query = select(User).where(User.email == form_data.username)
    result = await session.execute(query)
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_session)) -> UserResponse:
    hashed_pw = get_password_hash(user.password)
    db_user = User(name=user.name, email=user.email, hashed_password=hashed_pw)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return {"status": 200, "data": db_user}


@router.put("/change_password")
async def change_password(
    passwords: PasswordChange,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> MessageResponse:
    if not verify_password(passwords.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный старый пароль")
    current_user.hashed_password = get_password_hash(passwords.new_password)
    session.add(current_user)
    await session.commit()
    return {"status": 200, "message": "Пароль успешно изменён"}

# Создание пользователя
# @router.post("/", response_model=UserResponse)
# async def users_create(user: UserDefault, session: AsyncSession = Depends(get_session)) -> UserResponse:
#     user = User.model_validate(user)
#     session.add(user)
#     await session.commit()
#     await session.refresh(user)
#     return {"status": 200, "data": user}

# Получение списка пользователей
@router.get("/", response_model=UsersListResponse)
async def get_users(session: AsyncSession = Depends(get_session)) -> UsersListResponse:
    users = await session.execute(select(User))
    return {"status": 200, "data": users.scalars().all()}

# Получение информации о пользователе
@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    print("current_user.id:", current_user.id)
    return {"status": 200, "data": current_user}

# Обновление пользователя
@router.put("/me", response_model=UserResponse)
async def update_user(user_data: UserDefault, 
                      current_user: User = Depends(get_current_user),
                      session: AsyncSession = Depends(get_session)) -> UserResponse:
    user = await session.get(User, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_data.dict().items():
        setattr(user, key, value)
    await session.commit()
    await session.refresh(user)
    return {"status": 200, "data": user}

# Удаление пользователя
@router.delete("/me")
async def delete_user(current_user: User = Depends(get_current_user),
                      session: AsyncSession = Depends(get_session)) -> MessageResponse:
    user = await session.get(User, current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)
    await session.commit()
    return {"status": 200, "message": "User deleted"}

# Получение пользователя по ID
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)) -> UserResponse:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": 200, "data": user}
