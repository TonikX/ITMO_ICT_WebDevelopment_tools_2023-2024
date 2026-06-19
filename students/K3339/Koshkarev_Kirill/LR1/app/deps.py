"""Зависимости FastAPI, в т.ч. РУЧНАЯ аутентификация по JWT (п.3 задания).

Заголовок Authorization разбирается вручную, без использования сторонних
утилит вроде OAuth2PasswordBearer / fastapi.security. Токен проверяется
функцией decode_access_token из security.py (тоже ручная реализация).
"""
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, UserRole
from app.security import JWTError, decode_access_token

_UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Не удалось проверить учётные данные",
    headers={"WWW-Authenticate": "Bearer"},
)


def _extract_bearer_token(request: Request) -> str:
    """Вручную достаёт токен из заголовка 'Authorization: Bearer <token>'."""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise _UNAUTHORIZED

    parts = auth_header.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1].strip():
        raise _UNAUTHORIZED

    return parts[1].strip()


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """Аутентифицирует пользователя по JWT из заголовка Authorization."""
    token = _extract_bearer_token(request)

    try:
        payload = decode_access_token(token)
    except JWTError:
        raise _UNAUTHORIZED

    subject = payload.get("sub")
    if subject is None:
        raise _UNAUTHORIZED

    try:
        user_id = int(subject)
    except (TypeError, ValueError):
        raise _UNAUTHORIZED

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise _UNAUTHORIZED

    return user


def require_role(*roles: UserRole):
    """Фабрика зависимостей: доступ только пользователям с нужной ролью."""

    def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения операции",
            )
        return current_user

    return checker
