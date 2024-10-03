from passlib.context import CryptContext


def extract_user_data(data: dict) -> dict:
    user = {
        "email" : data["email"],
        "hashed_password" : hash_password(data["login"]["password"]),
        "first_name" : data["name"]["first"],
        "last_name" : data["name"]["last"]
    }
    return user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
