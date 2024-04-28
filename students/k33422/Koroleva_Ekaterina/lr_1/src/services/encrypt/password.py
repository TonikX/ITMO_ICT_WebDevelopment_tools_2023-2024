import bcrypt

__all__ = ['hash_password', 'validate_password']


def hash_password(
        password: str
) -> bytes:
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )


def validate_password(
        password: str,
        hashed_password: bytes
) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password
    )
