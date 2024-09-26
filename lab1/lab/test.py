import jwt
from datetime import datetime, timedelta

secret_key = "your_secret_key"

def encode_token(username: str) -> str:
    payload = {
        'exp': datetime.utcnow() + timedelta(hours=12),
        'iat': datetime.utcnow(),
        'sub': username
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')