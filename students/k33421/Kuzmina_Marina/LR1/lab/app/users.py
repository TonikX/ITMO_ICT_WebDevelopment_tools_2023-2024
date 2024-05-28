from http.client import HTTPException

from fastapi import APIRouter, Depends
from starlette import status

from .dependencies import authenticate
from lab.main import users_db, hash_password
from .models import User
from typing import List

router = APIRouter()

@router.get("/users", response_model=List[User])
async def get_users():
    return list(users_db.values())

@router.put("/users/change_password")
async def change_password(username: str, new_password: str, token: str = Depends(authenticate)):
    if username not in users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    users_db[username].password = hash_password(new_password)
    return {"message": "Password changed successfully"}
