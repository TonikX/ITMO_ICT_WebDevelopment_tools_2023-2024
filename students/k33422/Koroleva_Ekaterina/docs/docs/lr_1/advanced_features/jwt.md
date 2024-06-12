# JWT

## Генерация JWT

Процесс создания JWT состоит из трех основных этапов: создание полезной нагрузки (payload),
кодирование и подписание токена.

### Создание полезной нагрузки

Полезная нагрузка JWT включает в себя информацию о пользователе и метаданные токена, такие как время
истечения (`exp`) и время выпуска (`iat`).

#### Пример полезной нагрузки:

```python
payload = Payload(
    sub=str(user.id),  # Идентификатор пользователя
    exp=exp,  # Время истечения токена
    iat=now,  # Время создания токена
    email=user.email,  # Электронная почта пользователя
    is_superuser=user.is_superuser  # Признак администратора
)
```

### Кодирование и подписание токена

Кодирование и подписание токена производится с использованием приватного ключа и указанного
алгоритма подписи. Это обеспечивает целостность данных, предотвращая их изменение при передаче между
клиентом и сервером.

#### Функция кодирования:

```python
def encode(
    payload: Payload | dict,
    *,
    private_key: str = jwt_settings.private_key,
    algorithm: str = jwt_settings.algorithm,
) -> JWT:
    if not isinstance(payload, Payload):
        payload = Payload.model_validate(payload)

    return JWT(
        access=jwt.encode(
            payload.model_dump(),
            private_key,
            algorithm
        )
    )
```

## Декодирование JWT

Декодирование JWT производится для проверки и извлечения данных из токена. Используется публичный
ключ и алгоритм, указанные при кодировании, что позволяет верифицировать подпись и убедиться в
неизменности данных.

#### Функция декодирования:

```python
def decode(
    jwt_token: str | bytes | JWT,
    *,
    public_key: str = jwt_settings.public_key,
    algorithm: str = jwt_settings.algorithm,
) -> Payload:
    if isinstance(jwt_token, JWT):
        jwt_token = jwt_token.access

    return Payload.model_validate(
        jwt.decode(
            jwt_token,
            public_key,
            [algorithm]
        )
    )
```
