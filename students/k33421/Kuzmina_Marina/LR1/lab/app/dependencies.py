# Dependency for JWT authentication
from fastapi import HTTPException, status, Depends
from typing import Optional
import jwt

def authenticate(token: str) -> str:
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        return token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
