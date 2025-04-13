import os
import jwt
from dotenv import load_dotenv
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta


load_dotenv()
secret_key = os.getenv('SECRET_KEY')
jwt_algorithm = os.getenv('JWT_ALGORITHM')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Function for hashing password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Function for verify password with hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function for creating access token
def create_access_token(data: str , expiry:timedelta = None, refresh: bool = False) -> str:
    payload = {
        'sub': data,
        'exp': datetime.now() + (expiry if expiry is not None else timedelta(minutes=60)),
        'refresh' : refresh
    }

    token = jwt.encode(
        payload=payload,
        key= secret_key,
        algorithm=jwt_algorithm
    )

    return token

# Function for decoding access token
def decode_token(token: str) -> dict:
    try:
        print(f"Decoding token: {token}")
        print(f"Using secret key: {secret_key}")
        print(f"Using algorithm: {jwt_algorithm}")

        token_data = jwt.decode(
            jwt=token,
            key=secret_key,
            algorithms=[jwt_algorithm]
        )

        current_time = datetime.utcnow()
        if 'nbf' in token_data and current_time < datetime.utcfromtimestamp(token_data['nbf']):
            raise HTTPException(
                status_code=401,
                detail="The token is not yet valid"
            )

        return token_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Expire signature"
            )

    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
            )
