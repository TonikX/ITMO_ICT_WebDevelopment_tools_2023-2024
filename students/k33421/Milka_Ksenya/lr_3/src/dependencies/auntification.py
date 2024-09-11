import typing as tp

import jwt
from fastapi import Depends, HTTPException, security, status

from .. import schemas
from ..services.auntification import decode_jwt


def get_payload(
    credentials: tp.Annotated[security.HTTPAuthorizationCredentials, Depends(security.HTTPBearer())],
) -> schemas.Payload:
    try:
        print(credentials.credentials)
        payload = decode_jwt(credentials.credentials)
    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")

    return schemas.Payload.model_validate(payload)
