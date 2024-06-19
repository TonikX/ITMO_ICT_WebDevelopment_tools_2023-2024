import datetime
from fastapi import Security, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
import jwt
from starlette import status
from database.conn import get_session
from models import User
from sqlmodel import select


class AuthHandler:
    # Определение класса AuthHandler
    security = HTTPBearer()  # Создание экземпляра HTTPBearer для обеспечения безопасности
    pwd_context = CryptContext(schemes=['bcrypt'])  # Создание экземпляра CryptContext для хэширования паролей
    SECRET_KEY = 'SECRET_KEY'  # Установка секретного ключа для кодирования и декодирования JWT токенов

    # Метод для получения хэша пароля
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    # Метод для проверки пароля
    def verify_password(self, pwd, hashed_pwd):
        return self.pwd_context.verify(pwd, hashed_pwd)

    # Метод для кодирования JWT токена
    def encode_token(self, username):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),  # Устанавливаем время истечения токена
            'iat': datetime.datetime.utcnow(),  # Устанавливаем время создания токена
            'sub': username  # Устанавливаем имя пользователя как подписчика токена
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm='HS256')  # Кодируем токен с использованием секретного ключа и алгоритма HS256

    # Метод для декодирования JWT токена
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=['HS256'])  # Декодируем токен с использованием секретного ключа и алгоритма HS256
            return payload['sub']  # Возвращаем имя пользователя из поля 'sub' декодированного токена
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Expired signature')  # Вызываем исключение при истечении срока действия токена
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')  # Вызываем исключение при недействительном токене

    # Метод-обёртка для аутентификации
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)  # Декодируем токен, получаем имя пользователя

    # Метод для получения текущего пользователя
    def get_current_user(self, auth: HTTPAuthorizationCredentials = Security(security), session=Depends(get_session)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials'
        )
        username = self.decode_token(auth.credentials)  # Декодируем токен, получаем имя пользователя
        if username is None:
            raise credentials_exception  # Вызываем исключение, если имя пользователя не получено из токена
        user = session.exec(select(User).where(User.username == username)).first()  # Получаем пользователя из базы данных по имени пользователя из токена
        if user is None:
            raise credentials_exception  # Вызываем исключение, если пользователь не найден в базе данных
        return user  # Возвращаем найденного пользователя
