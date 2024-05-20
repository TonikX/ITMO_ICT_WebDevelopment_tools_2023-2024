from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jose import JWTError
from datetime import datetime, timedelta
import secrets
from conn import get_session, init_db
from models import *
from conn import engine, get_session
from pydanticModels import *
from app.userRoutes import router as user_router
from app.tasksRoutes import router as tasks_router
from app.categRoutes import router as categ_router
from app.timelogsRoutes import router as timelogs_router
from app.taskcategRoutes import router as taskscateg_router
from app.addRoutes import router as add_router
from pydanticModels import *
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI(
    title = "Time Managment"
)

@app.on_event("startup")
def on_startup():
    init_db()
    with Session(engine) as session:
            create_data(session)

def create_data(session: Session):
    session.commit()

def main():
    with Session(engine) as session:
        create_data(session)

#импортированные эндпоинты
app.include_router(user_router) 
app.include_router(tasks_router) 
app.include_router(categ_router) 
app.include_router(timelogs_router) 
app.include_router(taskscateg_router) 
app.include_router(add_router) 

#контекст шифрования с использованием алгоритма bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#pwd_context для хеширования паролей и проверки паролей 
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#генерация секретного ключа для создания JWT токенов и указание алгоритма шифрования
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"

#JWT токен для аутентифицированных пользователей, включая в токен время истечения и имя пользователя
def create_access_token(data: dict, expires_delta: timedelta = None) -> str: 
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#регистрирует нового пользователя, хеширует его пароль перед сохранением в базу данных
@app.post("/usersReg")
def create_user(username: str, password: str, session: Session = Depends(get_session)):
    hashed_password = hash_password(password) 
    user = User(username=username, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

#аутентифицирует пользователя и возвращает JWT токен, если аутентификация прошла успешно
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

#проверка, существует ли пользователь с указанным именем пользователя и соответствует ли предоставленный пароль хешированному паролю в базе данных
def authenticate_user(username: str, password: str, session: Session):
    user = session.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

#cоздание экземпляра OAuth2PasswordBearer, используется FastAPI для обработки токенов аутентификации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") 

#декодирует и проверяет JWT токен, извлекая из него имя пользователя
def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

#использует токен для получения текущего аутентифицированного пользователя из базы данных, проверяя его активность
def get_current_active_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = verify_token(token, credentials_exception)
    user = session.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

#возвращает данные о текущем аутентифицированном пользователе
@app.get("/usersme")
def read_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user

#позволяет аутентифицированному пользователю изменить свой пароль, проверяя сначала старый пароль, затем обновляя его на новый
@app.post("/users/change-password")
def change_password(password_change: PasswordChange, current_user: User = Depends(get_current_active_user), session: Session = Depends(get_session)):
    try:
        user = session.query(User).filter(User.id == current_user.id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(password_change.old_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect old password")
        user.hashed_password = hash_password(password_change.new_password)
        session.add(user)
        session.commit()
        return {"msg": "Password changed successfully"}
    except SQLAlchemyError as e:
        session.rollback()

        raise HTTPException(status_code=500, detail="Internal Server Error")

