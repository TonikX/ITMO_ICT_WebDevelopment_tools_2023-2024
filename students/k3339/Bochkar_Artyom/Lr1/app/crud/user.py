from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

from app.db.conection import get_session
from app.schemas.schemas import UserRegisterWithProfile, LoginResponse, UserRegisterResponse, TokenLogin
from app.services.hashing import hash_password
from app.services.auth import AuthHandler
from app.models.models import User, Profile

router = APIRouter()
auth_handler = AuthHandler()

@router.post("/register", response_model=UserRegisterResponse)
async def register(user_data: UserRegisterWithProfile, session: Session = Depends(get_session)):
    # Проверяем, существует ли пользователь
    existing_user = session.exec(select(User).where(
        (User.username == user_data.username) | (User.email == user_data.email)
    )).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    # Хэшируем пароль
    hashed_password, salt = hash_password(user_data.password)
    
    # Создаем пользователя
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        salt=salt
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Создаем профиль для пользователя
    profile = Profile(
        username=user_data.username,
        name=user_data.name,
        surname=user_data.surname,
        age=user_data.age,
        gender=user_data.gender,
        address=user_data.address,
        user_id=user.id
    )
    
    session.add(profile)
    session.commit()
    
    # Генерируем JWT токен
    token = auth_handler.encode_token(user.username)
    
    # Возвращаем пользователя с токеном
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "created_at": user.created_at,
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/login", response_model=LoginResponse)
async def login(login_data: TokenLogin, session: Session = Depends(get_session)):
    """
    Вход только по JWT токену, полученному при регистрации. 
    Возвращает только данные пользователя и профиля
    """
    try:
        # Декодируем токен и проверяем его валидность
        username = auth_handler.decode_token(login_data.token)
        
        # Проверяем, существует ли пользователь с таким username
        user = session.exec(select(User).where(User.username == username)).first()
        
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Возвращаем только данные пользователя и профиля
        return {
            "user": user,
        }
        
    except HTTPException:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
