from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from connection import get_session
import models
from models import UserDefault, User
from typing_extensions import TypedDict
from base_responses import MessageResponse

router = APIRouter()

class UserResponse(TypedDict):
    status: int
    data: User

class UsersListResponse(TypedDict):
    status: int
    data: List[User]

# Создание пользователя
@router.post("/", response_model=UserResponse)
async def users_create(user: UserDefault, session: AsyncSession = Depends(get_session)) -> UserResponse:
    user = User.model_validate(user)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {"status": 200, "data": user}

# Получение списка пользователей
@router.get("/", response_model=UsersListResponse)
async def get_users(session: AsyncSession = Depends(get_session)) -> UsersListResponse:
    users = await session.execute(select(User))
    return {"status": 200, "data": users.scalars().all()}

# Получение пользователя по ID
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)) -> UserResponse:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": 200, "data": user}

# Обновление пользователя
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserDefault, session: AsyncSession = Depends(get_session)) -> UserResponse:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_data.dict().items():
        setattr(user, key, value)
    await session.commit()
    await session.refresh(user)
    return {"status": 200, "data": user}

# Удаление пользователя
@router.delete("/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)) -> MessageResponse:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)
    await session.commit()
    return {"status": 200, "message": "User deleted"}