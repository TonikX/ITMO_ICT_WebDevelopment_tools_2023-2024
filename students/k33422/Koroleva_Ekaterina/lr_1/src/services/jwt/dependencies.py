from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError

from .schemes import Payload
from .utils import decode

__all__ = ['get_payload']

http_bearer = HTTPBearer()


def get_payload(
    jwt_token: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
) -> Payload:
    try:
        payload = decode(jwt_token.credentials)
    except InvalidTokenError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            'Invalid token'
        )

    return payload
