# Аутентификация

## Инструменты
```python
from passlib.context import CryptContext
from jose import JWTError, jwt
from pathlib import Path
from dotenv import dotenv_values
import datetime
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import db_queries

#dotenv setup
env_path = Path(__file__).parent / '.env'
config = dotenv_values(env_path)
# jwt setup
SECRET_KEY = config['JWT_SECRET_KEY']
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 800000
# hasher setup
crypto_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
# auth scheme setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(provided_password, actual_hash):
    return crypto_context.verify(provided_password, actual_hash)


def get_password_hash(password):
    return crypto_context.hash(password)


def generate_token(username):
    to_encode = {
        'exp': datetime.datetime.now() + datetime.timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        'iat': datetime.datetime.now(),
        'sub': username
    }
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_token(token):
    return jwt.decode(
        token,
        SECRET_KEY,
        ALGORITHM
    )


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    return get_user_by_token(token)


def get_user_by_token(token):
    token_data = decode_token(token)
    username = token_data['sub']
    return db_queries.get_user_by_username(username)

```


## Конечные точки
```python
@app.post('/token/', status_code=200, tags=[Tags.user])
def create_api_token(
        user_login: models.UserLogin
) -> tp.TypedDict('token_response', {'access_token': str, 'token_type': str}):
    try:
        user_db = db_queries.get_user_by_username(user_login.username)
    except ValueError:
        raise HTTPException(status_code=400, detail=f'no user with username {user_login.username}')

    is_password_correct = auth.verify_password(user_login.password, user_db.hashed_password)
    if not is_password_correct:
        raise HTTPException(status_code=400, detail=f'Incorrect password for username: {user_login.username}')

    token = auth.generate_token(user_login.username)
    return {'access_token': token, 'token_type': 'bearer'}

@app.post('/user/', status_code=201, tags=[Tags.user])
def create_user(
        user: models.UserRegister,
        session:Session=Depends(get_session_depends)
)-> tp.TypedDict('Created message', {'msg': str}):
    hashed_password = auth.get_password_hash(user.password)
    user_data = user.dict()
    user_data['hashed_password'] = hashed_password
    user = models.User.model_validate(user_data)
    tools.add_object_to_db_and_refresh(session, user)
    return {'msg': "Created"}


@app.put('/user/password/', status_code=201, tags=[Tags.user])
def change_user_password(
        user_password: models.UserChangePassword,
        user_db: models.User = Depends(auth.get_current_user),
        session: Session = Depends(get_session_depends)
) -> tp.TypedDict('password_put_response', {'msg': str}):
    is_password_correct = auth.verify_password(user_password.current_password, user_db.hashed_password)
    if not is_password_correct:
        raise HTTPException(status_code=400, detail='Incorrect current password')

    if user_password.new_password != user_password.new_password_verification:
        raise HTTPException(status_code=400, detail='Passwords don\'t match')

    new_hash = auth.get_password_hash(user_password.new_password)
    user_db.hashed_password = new_hash
    session.add(user_db)
    session.commit()
    return {'msg': 'password changed'}

```