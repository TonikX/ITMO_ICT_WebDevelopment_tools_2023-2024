from passlib.context import CryptContext
from dotenv import load_dotenv
import os
pwd_context = CryptContext(schemes=['bcrypt'])
SALT = os.getenv('SALT')
PEPPER = os.getenv('PEPPER')
load_dotenv()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(f'{SALT}{password}{PEPPER}'.encode())


def verify_password(pwd:  str, hashed_pwd: bytes | str) -> bool:
    return pwd_context.verify(f'{SALT}{pwd}{PEPPER}', hashed_pwd)
