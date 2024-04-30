from datetime import datetime, timedelta

import jwt

from src.config import jwt_settings
from src.models import User
from .schemes import JWT, Payload
from ..auth import UserBase

__all__ = ['encode', 'decode', 'create_jwt']


def encode(
    payload: Payload | dict,
    *,
    private_key: str = jwt_settings.private_key,
    algorithm: str = jwt_settings.algorithm,
) -> JWT:
    if not isinstance(payload, Payload):
        payload = Payload.model_validate(payload)

    return JWT(
        access=jwt.encode(
            payload.model_dump(),
            private_key,
            algorithm
        )
    )


def decode(
    jwt_token: str | bytes | JWT,
    *,
    public_key: str = jwt_settings.public_key,
    algorithm: str = jwt_settings.algorithm,
) -> Payload:
    if isinstance(jwt_token, JWT):
        jwt_token = jwt_token.access

    return Payload.model_validate(
        jwt.decode(
            jwt_token,
            public_key,
            [algorithm]
        )
    )


def create_jwt(
    user: User | UserBase | dict
) -> JWT:
    if isinstance(user, dict):
        user = UserBase.model_validate(user)

    now = datetime.utcnow()
    exp = now + timedelta(minutes=jwt_settings.expire_minutes)

    payload = Payload(
        sub=str(user.id),
        exp=exp,
        iat=now,
        email=user.email,
        is_superuser=user.is_superuser,
    )

    return encode(payload)
