import typing as tp
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from .. import config, schemas


def encode_jwt(payload: dict[str, tp.Any]) -> str:
    return jwt.encode(
        payload,
        config.auntification.private_key,
        config.auntification.algorithm,
    )


def decode_jwt(token: str) -> tp.Any:
    return jwt.decode(
        token,
        config.auntification.public_key,
        algorithms=[config.auntification.algorithm],
    )


def create_jwt(user_id: int) -> str:
    now = datetime.now(timezone.utc)

    return encode_jwt(
        schemas.Payload(
            sub=user_id,
            iat=now,
            exp=now + timedelta(seconds=config.auntification.expires_in),
        ).model_dump()
    )


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt(),
    ).decode()


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode(),
    )
