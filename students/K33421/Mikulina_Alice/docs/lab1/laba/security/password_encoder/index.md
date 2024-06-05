# security/password_encoder.py

Необходимые импорты
```
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
```
Создается экземпляр pwd_context, который настроен на использование схемы хеширования «bcrypt» и установлен на «авто» для обработки устаревания.
```
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

Создается экземпляр oauth2_scheme, который настроен на использование конечной точки «токен» для аутентификации на основе токенов.
```
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```


Функцияverify_password принимает простой текстовый пароль и хешированный пароль и использует метод pwd_context.verify для их безопасного сравнения.  
Эта функция возвращает True, если простой текстовый пароль соответствует хешированному паролю, и False в противном случае.
```
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
```

Функция get_password_hash принимает простой текстовый пароль и использует метод pwd_context.hash для создания безопасного хэша пароля.  
Хешированный пароль затем можно сохранить в базе данных или другом безопасном хранилище.
```
def get_password_hash(password):
    return pwd_context.hash(password)
```