from models import User
from sqlmodel import select

# Global environment variables
security = HTTPBearer()
pwd_context = CryptContext(schemes=['bcrypt'])
secret_key = 'supersecret'


def get_password_hash(password):
    print(pwd_context.hash(password))
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def encode_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')


def decode_token(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')


def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(security)):
    return decode_token(auth.credentials)


def get_current_user(auth: HTTPAuthorizationCredentials = Security(security), session=Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,