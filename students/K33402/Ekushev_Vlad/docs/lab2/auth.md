# Авторизация и JWT

С помощью функций `encode_token` и `decode_token` шифруется информация о пользователе и генерируется JWT токен с помощью библиотеки `jose`.

Пароли хешируются с помощью `bcrypt` и хранятся в таком виде в базе данных.

Для того, чтобы закрыть роут за авторизацией и получить объект пользователя внутри роута, достаточно написать:

```Python
@router.get("/")
def get(
    ...
    user: User = Depends(auth_service.get_current_user),
    ...
)
```

```Python title="services/auth.py"
import datetime
from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import jwt
from starlette import status
from app.core.config import settings
from app.services.user import find_user

ACCESS_TOKEN_HASH_ALGORITHM: str = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(pwd, hashed_pwd):
    return pwd_context.verify(pwd, hashed_pwd)


def encode_token(user_id):
    now = datetime.datetime.now(datetime.UTC)
    payload = {
        "exp": now + datetime.timedelta(hours=8),
        "iat": now,
        "sub": user_id,
    }
    return jwt.encode(
        payload, settings.SECRET_KEY, algorithm=ACCESS_TOKEN_HASH_ALGORITHM
    )


def decode_token(token):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ACCESS_TOKEN_HASH_ALGORITHM]
        )
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired signature"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(security)):
    return decode_token(auth.credentials)


def get_current_user(auth: HTTPAuthorizationCredentials = Security(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    username = decode_token(auth.credentials)
    if username is None:
        raise credentials_exception
    user = find_user(username)
    if username is None:
        raise credentials_exception
    return user
```