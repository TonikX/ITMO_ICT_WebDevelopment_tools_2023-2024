# Аутентификация и хеширование пароля

В базе данных пароль пользователя хранится в захешированном виде, пользователь может поменять пароль.

При авторизации возвращается JWT токен, который используется для аутентификации при запросах.

## Функции хеширования и проверки пароля:
```python
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(password: str, db_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), db_password.encode())


```

## Функции кодирования и декодирования JWT:
```python
def encode_token(email: str) -> str:
    payload = {
        'exp': datetime.datetime.now() + datetime.timedelta(hours=12),
        'iat': datetime.datetime.now(),
        'sub': email
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')


def decode_token(token: str) -> int:
    try:
        payload = jwt.decode(token, secret_key, leeway=100000, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')
```

## Эндпоинт для регистрации
```python
@router.post("/registration")
def registration(user: UserDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": User}):
    user.password = hash_password(user.password)
    user = User.model_validate(user)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"status": 200, "data": user}
```

## Эндпоинт для авторизации (возвращает JWT)
```python
@router.post("/login")
def login(user: UserAuth, session=Depends(get_session)) -> str:
    query = select(User).where(User.email == user.email)
    db_user = session.exec(query).scalar()
    if not db_user:
        raise HTTPException(status_code=401, detail='Invalid email')

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail='Invalid password')

    token = encode_token(user.email)
    return token
```

## Эндпоинт для получения пользователя по токену (токен передается в headers)
```python
@router.get("/user/token", response_model=UserExtended)
def get_user_by_token(token: Optional[str] = Header(None), session=Depends(get_session)) -> User:
    token = str.replace(str(token), 'Bearer ', '')
    if not token:
        raise HTTPException(status_code=401, detail='Unauthorized')
    user_email = decode_token(token)
    query = select(User).where(User.email == user_email)
    user = session.exec(query).scalar()
    return user
```

## Эндпоинт для смены пароля
```python
@router.patch("/user/{user_id}/password", response_model=UserDefault)
def change_password(user_id: int, old_password: str, new_password: str, session=Depends(get_session)) -> User:
    user = session.get(User, user_id)
    if not verify_password(old_password, user.password):
        raise HTTPException(status_code=401, detail='Invalid password')

    new_password_hashed = hash_password(new_password).decode()
    setattr(user, 'password', new_password_hashed)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
```
