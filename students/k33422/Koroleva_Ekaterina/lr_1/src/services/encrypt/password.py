import bcrypt

__all__ = ['hash_password', 'validate_password']


def hash_password(
        password: str
) -> str:
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def validate_password(
        password: str,
        hashed_password: str
) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )
