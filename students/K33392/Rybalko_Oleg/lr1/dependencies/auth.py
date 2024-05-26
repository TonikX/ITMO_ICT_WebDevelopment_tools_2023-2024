import os
from http import HTTPStatus

import jwt
from fastapi import HTTPException, Request


def verify_jwt(request: Request):
    try:
        return jwt.decode(request.headers.get("authorization", "").split()[-1], os.getenv("JWT_KEY"), ["HS256"])
    except (jwt.exceptions.PyJWTError, IndexError):
        raise HTTPException(HTTPStatus.UNAUTHORIZED)
