from fastapi import Depends, HTTPException, status, Form, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.db.helper import helper
from src.models import User, Token, UserBase, UserPasswordCreate
from src.services import auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/auth")


async def validate_auth_user(
        email: EmailStr = Form(),
        password: str = Form(),
        session: AsyncSession = Depends(helper.scoped_session_dependency)
):
    default_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid email or password",
    )
    user = await session.execute(select(User).where(User.email == email))
    user = user.first()
    print(user.first_name)

    if not user:
        raise default_exc

    if not auth.validate_password(
            password=password,
            hashed_password=user.password_hash
    ):
        raise default_exc

    return user


async def get_current_auth_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(helper.scoped_session_dependency)
):
    default_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )
    try:
        payload: dict = auth.decode_jwt(token=token)
        email: str = payload.get('sub')
        user = await session.execute(select(User).where(User.email == email))
        user = user.first()
    except InvalidTokenError as e:
        raise default_exc
    return user


@router.post('/login/', response_model=Token)
async def login_user(
        user: User = Depends(validate_auth_user),
):
    payload = {
        'sub': user.email
    }

    token = auth.encode_jwt(payload)
    return Token(access_token=token, token_type='Bearer')


@router.post('/register/', response_model=UserBase)
async def register_user(
        user: UserPasswordCreate,
        session: AsyncSession = Depends(helper.scoped_session_dependency)
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
