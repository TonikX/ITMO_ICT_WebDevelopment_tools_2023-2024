from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.db.helper import helper
from src.models import User, Token, UserLogin, UserBase, UserPasswordCreate, UserPasswordUpdate
from src.services import auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login/")

router = APIRouter(prefix="/auth")


async def validate_auth_user(
        credentials: Annotated[UserLogin, Depends()],
        session: Annotated[AsyncSession, Depends(helper.scoped_session_dependency)]
):
    default_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid email or password",
    )
    user = await session.execute(select(User).where(User.email == credentials.email))
    user = user.first()

    if not user:
        raise default_exc

    user = user[0]

    if not auth.validate_password(
            password=credentials.password,
            hashed_password=user.password_hash
    ):
        raise default_exc

    return user


def get_current_token_payload(
        token: Annotated[str, Depends(oauth2_scheme)]
) -> dict:
    try:
        payload = auth.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


async def get_current_auth_user(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        session: Annotated[AsyncSession, Depends(helper.scoped_session_dependency)]
):
    default_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )
    try:
        email: str = payload.get('sub')
        user = await session.execute(select(User).where(User.email == email))
        user = user.first()[0]
    except InvalidTokenError as e:
        raise default_exc
    return user


@router.post('/login/', response_model=Token)
async def login_user(
        user: Annotated[User, Depends(validate_auth_user)],
):
    payload = {
        'sub': user.email
    }

    token = auth.encode_jwt(payload)
    return Token(access_token=token, token_type='Bearer')


@router.post('/register/', response_model=UserBase)
async def register_user(
        user: Annotated[UserPasswordCreate, Depends()],
        session: Annotated[AsyncSession, Depends(helper.scoped_session_dependency)]
):
    exists_user = await session.execute(select(User).where(User.email == user.email))

    if exists_user.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    password_hash = auth.hash_password(user.password)

    user_in = User(**user.dict(), password_hash=password_hash)
    session.add(user_in)
    await session.commit()
    return user_in


@router.post('/change-password/')
async def change_password(
        scheme: Annotated[UserPasswordUpdate, Depends()],
        user: Annotated[User, Depends(get_current_auth_user)],
        session: Annotated[AsyncSession, Depends(helper.scoped_session_dependency)]
):
    if not auth.validate_password(scheme.old_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old Password Is Incorrect"
        )

    password_hash = auth.hash_password(scheme.new_password)
    user.password_hash = password_hash
    await session.commit()
    return {"msg": "Password Changed Successfully"}


@router.get('/me/')
async def auth_user_check_self_info(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user: Annotated[User, Depends(get_current_auth_user)],
):
    return {
        'subject': payload.get('sub'),
        'expire': payload.get('exp'),
        'logged_in_at': payload.get('iat'),
        'user_data': UserBase(**user.dict()),
    }
