from fastapi import APIRouter, HTTPException, Depends, Security
from models import UserBase, User, UserShow, ChangePassword
import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
import jwt
from starlette import status
from db import get_session
from sqlmodel import select



security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"])
secret_key = "supersecret"


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def encode_token(user_id: str) -> str:
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8),
        "iat": datetime.datetime.utcnow(),
        "sub": user_id,
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")


def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload["sub"]
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(security)):
    return decode_token(auth.credentials)


def get_current_user(
    auth: HTTPAuthorizationCredentials = Security(security),
    session=Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    username = decode_token(auth.credentials)
    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise credentials_exception
    return user


auth_router = APIRouter()


@auth_router.post("/register", status_code=201)
def register(user: UserBase, session=Depends(get_session)):
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username is taken")
    hashed_pwd = get_password_hash(user.password)
    user = User(username=user.username, password=hashed_pwd)
    session.add(user)
    session.commit()
    return {"status": 201, "message": "Created"}


@auth_router.post("/login")
def login(user: UserBase, session=Depends(get_session)):
    user_found = session.exec(select(User).where(User.username == user.username)).first()
    if not user_found or not verify_password(user.password, user_found.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = encode_token(user_found.username)
    return {"token": token}


@auth_router.get("/user", response_model=UserShow)
def get_current_user(user: User = Depends(get_current_user)) -> User:
    return user


@auth_router.patch("/me/change-password")
def change_password(
    change_password: ChangePassword,
    session=Depends(get_session),
    current=Depends(get_current_user),
):
    found_user = session.get(User, current.id)
    if not found_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(change_password.old_password, found_user.password):
        raise HTTPException(status_code=400, detail="Invalid old password")
    found_user.password = get_password_hash(change_password.new_password)
    session.add(found_user)
    session.commit()
    session.refresh(found_user)
    return {"status": 200, "message": "Password changed successfully"}