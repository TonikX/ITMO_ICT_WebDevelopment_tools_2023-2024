from fastapi import Depends, HTTPException, status, APIRouter
from sqlmodel import Session, select
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import secrets

from backend.database import get_session
from backend.models import UserCreate, User

router = APIRouter()


# Функция для генерации секретного ключа, используемого для подписи JWT
def generate_secret_key(length=32):
    return secrets.token_urlsafe(length)


# Генерация секретного ключа, определение алгоритма шифрования и времени жизни токена
SECRET_KEY = generate_secret_key()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Создание экземпляра OAuth2PasswordBearer для получения токена из запросов
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Создание контекста шифрования для работы с паролями, используя bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Функции для верификации паролей и генерации хеша пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# Функция для создания токена доступа с опциональным сроком действия
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Эндпоинт для регистрации нового пользователя
# Хеширует пароль и сохраняет пользователя в базе данных
@router.post("/users/", response_model=User)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# Эндпоинт для аутентификации пользователя и получения токена доступа
@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Функция для аутентификации пользователя, проверяет существование пользователя и верифицирует пароль
def authenticate_user(username: str, password: str, session: Session):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# Функция для получения текущего аутентифицированного пользователя из токена
async def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = username
    except JWTError:
        raise credentials_exception
    user = session.exec(select(User).where(User.username == token_data)).first()
    if user is None:
        raise credentials_exception
    return user


# Эндпоинт для получения данных о текущем аутентифицированном пользователе
@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
