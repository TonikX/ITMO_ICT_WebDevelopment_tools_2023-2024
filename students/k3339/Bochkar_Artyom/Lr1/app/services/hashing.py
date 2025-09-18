import hashlib
import os
import base64


# Функция для хэширования пароля с солью
def hash_password(password: str) -> tuple[str, str]:
    salt = os.urandom(16)
    password_salt = password.encode('utf-8') + salt
    hashed_password = hashlib.sha256(password_salt).hexdigest()
    # Кодируем salt в base64 для хранения в БД
    salt_base64 = base64.b64encode(salt).decode('utf-8')
    return hashed_password, salt_base64

# Проверка пароля
def verify_password(plain_password: str, hashed_password: str, salt_base64: str) -> bool:
    # Декодируем salt из base64
    salt = base64.b64decode(salt_base64.encode('utf-8'))
    password_salt = plain_password.encode('utf-8') + salt
    return hashlib.sha256(password_salt).hexdigest() == hashed_password