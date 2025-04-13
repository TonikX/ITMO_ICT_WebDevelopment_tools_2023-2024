from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.auth.auth import decode_token


# Class for token
class TokenBearer(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials

        token_data = decode_token(token)

        return token_data

    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)

        return token_data is not None

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")


# Class for access token
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
                )
