import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
EXPIRATION_TIME = timedelta(minutes=30)


def createJWTToken(data: dict):
    expiration = datetime.utcnow() + EXPIRATION_TIME
    data.update({"exp": expiration})
    token = jwt.encode(data, key=SECRET_KEY, algorithm=ALGORITHM)
    return token


def verifyJWTToken(token: str):
    try:
        decoded_data = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data
    except jwt.PyJWTError:
        return None
