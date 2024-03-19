from fastapi import HTTPException
from passlib.context import CryptContext
from starlette import status

from crud import authenticate_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_current_user(token: str):
    # Здесь вы должны провести аутентификацию пользователя, например, проверив токен
    # В данном примере, мы эмулируем аутентификацию с помощью токена
    user = authenticate_user(token)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
# Hashing password
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
