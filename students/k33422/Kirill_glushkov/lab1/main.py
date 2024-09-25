from typing import List
from fastapi import APIRouter, FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from app.database import SessionLocal, init_db
from models import UserDB, IncomeDB
from app.schemas import Income, UserLogin, Budget, User
from auth import encode_token, decode_token, find_user, get_current_user
from encode import verify_password, get_password_hash
from fastapi.security import HTTPAuthorizationCredentials
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})
router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/users")
async def get_users() -> List[User]:
    with SessionLocal() as db:
        users = db.query(UserDB).all()
        return users
    
@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    with SessionLocal() as db:
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        print(user, 'usr')
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    with SessionLocal() as db:
        db_user = db.query(UserDB).get(user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(db_user)
        db.commit()
        return JSONResponse(status_code=204, content="User deleted")
    

@router.post("/users/register", response_model=User)
async def register(user: UserLogin):
    with SessionLocal() as db:
        user_data = user.model_dump(exclude={'password'})
        db_user = UserDB(**user_data, password = get_password_hash(user.password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


@router.post("/login", response_model=Token)
def login(user: UserLogin) -> Token:
    user_found = find_user(user.username)

    if not user_found:
        raise HTTPException(status_code=401, detail="Invalid username and/or password")
    verified = verify_password(user.password, user_found.password)

    if not verified:
        raise HTTPException(status_code=401, detail="Invalid username and/or password")

    token = encode_token(user_found.username)
    return Token(access_token=token)
    
#change password for user 
@router.put("/users/{user_id}/password")
async def change_password(user_id: int, new_password: str):
    with SessionLocal() as db:
        db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db_user.password = get_password_hash(new_password)
        db.commit()
        db.refresh(db_user)
        return db_user
    
# get current user
@router.post("/me", response_model=User)
def get_current_user(
    user: User = Depends(get_current_user),
) -> User:
    return User(
        username=user.username,
        email=user.email,
    )


@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    with SessionLocal() as db:
        db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        for var, value in vars(user).items():
            setattr(db_user, var, value)
        db.commit()
        db.refresh(db_user)
        return db_user
#many to many
@router.get("/users/{user_id}/incomes", response_model=List[Income])
async def get_user_incomes(user_id: int):
    with SessionLocal() as db:
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        incomes = db.query(IncomeDB).filter(IncomeDB.user_id == user_id).all()
        return incomes


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True, workers=1, log_level='debug', access_log=True)