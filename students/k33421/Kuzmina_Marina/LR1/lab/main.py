'''import jwt
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime, timedelta

from lab.app.dependencies import authenticate

app = FastAPI()

# Mock database
users_db = {}
user_id_counter = 0

class User(BaseModel):
    id: int
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def generate_token(username: str) -> str:
    expiration = datetime.utcnow() + timedelta(minutes=30)
    token_data = {
        "sub": username,
        "exp": expiration
    }
    token = jwt.encode(token_data, "secret", algorithm="HS256")
    return token

def hash_password(password: str) -> str:
    # Simple hashing, just for demonstration
    return password[::-1]

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return plain_password == hashed_password[::-1]

@app.post("/register", response_model=User)
async def register_user(user: UserCreate):
    global user_id_counter
    user_id_counter += 1
    hashed_password = hash_password(user.password)
    new_user = User(id=user_id_counter, username=user.username, password=hashed_password)
    users_db[user.username] = new_user
    return new_user

@app.post("/login", response_model=Token)
async def login_user(user: UserCreate):
    if user.username not in users_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    stored_user = users_db[user.username]
    if not verify_password(user.password, stored_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    token = generate_token(user.username)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def get_current_user(token: str = Depends(authenticate)):
    user_data = jwt.decode(token, "secret", algorithms=["HS256"])
    username = user_data.get("sub")
    if username is None or username not in users_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return users_db[username]
'''
from fastapi import FastAPI, HTTPException
#from lab.database import get_session, get_user, get_user_by_username, create_user, update_user, delete_user
from lab.auth.auth import authenticate_user, create_access_token
from lab.settings import SECRET_KEY

app = FastAPI()

# Операция создания токена доступа
@app.post("/token")
async def login_for_access_token(username: str, password: str):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username}, secret_key=SECRET_KEY)
    return {"access_token": access_token, "token_type": "bearer"}

# Операция чтения пользователя по идентификатору (Read)
@app.get("/users/{user_id}")
async def read_user(user_id: int):
    session = get_session()
    user = get_user(user_id, session)
    session.close()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Операция обновления пользователя (Update)
@app.put("/users/{user_id}")
async def update_user(user_id: int, user_data: dict):
    session = get_session()
    updated_user = update_user(user_id, user_data, session)
    session.close()
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# Операция удаления пользователя (Delete)
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    session = get_session()
    deleted_user = delete_user(user_id, session)
    session.close()
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# Операция создания нового пользователя (Create)
@app.post("/users/")
async def create_user(user_data: dict):
    session = get_session()
    created_user = create_user(user_data, session)
    session.close()
    return created_user
