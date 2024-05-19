from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select, exc, insert
from starlette import status

from lab.config import settings
from lab.db.database import DatabaseSession
from lab.db.models import User as UserModel
from lab.rest.auth.schemas import TokenData, UserCreateData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
OAuthScheme = Annotated[str, Depends(oauth2_scheme)]


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(secret=plain_password, hash=hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(secret=password)


def get_user(session: DatabaseSession, username: str) -> UserModel | None:
    stmt = select(UserModel).where(UserModel.username == username)
    try:
        return session.scalars(stmt).one()
    except (exc.NoResultFound, exc.MultipleResultsFound):
        return None


def get_users(session: DatabaseSession) -> list[UserModel]:
    stmt = select(UserModel)
    return session.scalars(stmt).all()


def create_user(session: DatabaseSession, user_data: UserCreateData) -> UserModel | None:
    stmt = (
        insert(UserModel)
        .values(
            username=user_data.username,
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
        )
        .returning(UserModel)
    )
    try:
        return session.scalars(stmt).one()
    except (exc.NoResultFound, exc.MultipleResultsFound):
        return None


def authenticate_user(session: DatabaseSession, username: str, password: str) -> UserModel | None:
    user = get_user(session=session, username=username)
    if not user:
        return None
    if not verify_password(plain_password=password, hashed_password=user.hashed_password):
        return None
    return user


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(claims=to_encode, key=settings.security.secret_key, algorithm=settings.security.algorithm)
    return encoded_jwt


async def get_current_user(token: OAuthScheme, session: DatabaseSession) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token=token, key=settings.security.secret_key, algorithms=[settings.security.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(session=session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


CurrentUser = Annotated[UserModel, Depends(get_current_user)]
