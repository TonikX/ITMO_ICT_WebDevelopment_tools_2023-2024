# security/jwt_process.py

Необходимые импорты
```
from datetime import datetime, timedelta, timezone
from typing import Union

import jwt
import time
from fastapi import HTTPException, status
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
```

Константы:  

SECRET_KEY: секретный ключ, используемый для подписи и проверки токенов JWT.  
АЛГОРИТМ: алгоритм, используемый для подписи и проверки токенов JWT (в данном случае HS256).  
ACCESS_TOKEN_EXPIRE_MINUTES: количество минут, в течение которых действителен токен доступа.  
```
SECRET_KEY = "c2ey7mPHmM21BrduVUvvJGMLSDTCfnBnaJEyTnigQP2TYgYQEgLVq2i55WuEhCcP"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24
```

Эта функция принимает словарь данных (обычно данные, связанные с пользователем) и генерирует токен JWT.  
Он создает копию входных данных, добавляет поле «exp» (срок действия) с текущим временем плюс ACCESS_TOKEN_EXPIRE_MINUTES, а затем кодирует данные с использованием SECRET_KEY и АЛГОРИТМА.  
Возвращается закодированный токен JWT.
```
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
```

 Эта функция принимает токен JWT в качестве входных данных и пытается его декодировать.  
 Сначала он определяет исключение Credential_Exception, которое будет возникать в случае каких-либо проблем с токеном.  
 Затем он пытается декодировать токен, используя SECRET_KEY и АЛГОРИТМ.  
 Если декодирование прошло успешно, из полезных данных извлекается поле «sub» (тема), которое, как ожидается, будет идентификатором пользователя.  
 Если декодирование завершается неудачей (из-за ошибки InvalidTokenError или отсутствия поля «sub»), возникает исключение Credential_Exception.  
 Функция возвращает идентификатор пользователя, извлеченный из полезных данных токена.
```
def parse_jwt_token(token: str):
    print(token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except InvalidTokenError as e:
        print(e)
        raise credentials_exception

    if user_id is None:
        raise credentials_exception

    return user_id
```