# endpoints/auth.py

Необходимые импорты
```
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from pydantic import BaseModel

from db.models import AppUser, AppUserDefault
from security.password_encoder import oauth2_scheme, verify_password, get_password_hash
from security.jwt_process import create_access_token, parse_jwt_token
from connection import get_session
```

Создается экземпляр APIRouter, который используется для определения маршрутов API.
```
router = APIRouter()
```

Класс Token — это модель Pydantic, определяющая структуру ответа токена, которая включает в себя токен доступа и тип токена (по умолчанию установлен на «носитель»).
```
class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
```

Эта функция представляет собой асинхронную зависимость, которая используется для получения текущего пользователя из базы данных на основе предоставленного токена JWT.  
Он использует функцию parse_jwt_token для извлечения идентификатора пользователя из токена, а затем извлекает соответствующий объект AppUser из базы данных.  
Если пользователь не найден, возникает исключение HTTPException с кодом состояния 404.  
Функция возвращает объект AppUser.
```
async def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    user_id = parse_jwt_token(token)

    user = session.get(AppUser, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
```

Эта функция управляет процессом входа в систему.  
Он берет учетные данные пользователя (имя пользователя и пароль) из зависимости OAuth2PasswordRequestForm.  
Он извлекает объект AppUser из базы данных на основе предоставленного имени пользователя.  
Если пользователь не найден или пароль неверен, возникает исключение HTTPException с кодом состояния 404.  
Если учетные данные действительны, он создает токен доступа с помощью функции create_access_token и возвращает объект Token.
```
@router.post("/token", response_model=Token)
def login(user_credits: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user: AppUser = session.exec(select(AppUser).filter(AppUser.username == user_credits.username)).first()

    if user is None:
        raise HTTPException(status_code=404, detail="Username not found")

    if not verify_password(user_credits.password, user.password):
        raise HTTPException(status_code=404, detail="Incorrect password")

    token = create_access_token({"sub": user.id})
    return Token(access_token=token)
```

Эта функция управляет процессом регистрации пользователя.  
В качестве входных данных принимаются новые пользовательские данные (AppUserDefault).  
Он проверяет, занято ли указанное имя пользователя. В этом случае возникает исключение HTTPException с кодом состояния 404.  
Если имя пользователя доступно, он создает новый объект AppUser с предоставленными данными, устанавливает хеш пароля с помощью функции get_password_hash и добавляет пользователя в базу данных.  
После сохранения нового пользователя он создает токен доступа с помощью функции create_access_token и возвращает объект Token.
```
@router.post("/register", response_model=Token)
def register(new_user: AppUserDefault, session: Session = Depends(get_session)):
    user: AppUser = session.exec(select(AppUser).filter(AppUser.username == new_user.username)).first()

    if user is not None:
        raise HTTPException(status_code=404, detail="Username already taken")

    db_user = AppUser(
        username=new_user.username,
        email=new_user.email,
        password=get_password_hash(new_user.password),
        about=new_user.about,
        location=new_user.location,
    )
    session.add(db_user)
    session.commit()

    token = create_access_token({"sub": db_user.id})
    return Token(access_token=token)
```