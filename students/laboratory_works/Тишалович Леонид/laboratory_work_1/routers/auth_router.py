import datetime
from fastapi import APIRouter, HTTPException, Depends, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from schemas import Participant, ParticipantDefault, ParticipantDisplay, ChangePassword, Login
from database import get_session
from sqlmodel import select
from passlib.context import CryptContext
from jose import jwt
import dotenv

dotenv.load_dotenv()

security = HTTPBearer()
pwd_context = CryptContext(schemes=['bcrypt'])
secret = 'top_secret'
algorythm = 'HS256'


router = APIRouter(tags=["Auth"])


#хэширование пароля
def get_password_hash(password):
    return pwd_context.hash(password)


@router.post('/registration', status_code=201)
def register(user: ParticipantDefault, session=Depends(get_session)):
    users = session.exec(select(Participant)).all()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_pwd = get_password_hash(user.password)
    user = Participant(username=user.username, password=hashed_pwd, email=user.email,
                       contact_number=user.contact_number)
    session.add(user)
    session.commit()
    return {"status": 201, "message": "Created"}


def verify_password(pwd, hashed_pwd):
    return pwd_context.verify(pwd, hashed_pwd)

#создание токена
def encode_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, secret, algorithm=algorythm)


@router.post('/login')
def login(user: Login, session=Depends(get_session)):
    user_found = session.exec(select(Participant).where(Participant.username == user.username)).first()
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    verified = verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = encode_token(user_found.username)
    return {'token': token}

# декодирование токена
def decode_token(token):
    try:
        payload = jwt.decode(token, secret, algorithms=[algorythm])
        return payload['sub']
    except Exception:
        raise HTTPException(status_code=401, detail='Token error')


def get_current_user(auth: HTTPAuthorizationCredentials = Security(security), session=Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials'
    )
    username = decode_token(auth.credentials)
    if username is None:
        raise credentials_exception
    user = session.exec(select(Participant).where(Participant.username == username)).first()
    if user is None:
        raise credentials_exception
    return user


@router.get('/users/me')
def user_me(user: Participant = Depends(get_current_user)) -> ParticipantDisplay:
    return user


@router.patch("/users/me/reset-password")
def user_pwd(user_pwd: ChangePassword, session=Depends(get_session), current=Depends(get_current_user)):
    found_user = session.get(Participant, current.id)
    if not found_user:
        raise HTTPException(status_code=404, detail="User not found")
    verified = verify_password(user_pwd.old_password, found_user.password)
    if not verified:
        raise HTTPException(status_code=400, detail="Invalid old password")
    hashed_pwd = get_password_hash(user_pwd.new_password)
    found_user.password = hashed_pwd
    session.add(found_user)
    session.commit()
    session.refresh(found_user)
    return {"status": 200, "message": "password changed successfully"}
